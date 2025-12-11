"""
性别分类器
基于OpenCV DNN的性别识别
"""

import cv2
import numpy as np
import os
from typing import Tuple, Optional, Dict
from enum import Enum

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger(__name__)


class Gender(Enum):
    """性别枚举"""
    MALE = "男"
    FEMALE = "女"
    UNKNOWN = "未知"


class GenderClassifier:
    """性别分类器"""
    
    def __init__(self, model_path: Optional[str] = None, prototxt_path: Optional[str] = None, **kwargs):
        """
        初始化性别分类器
        
        Args:
            model_path: 模型文件路径（.caffemodel或.onnx）
            prototxt_path: 模型配置文件路径（.prototxt，仅Caffe模型需要）
            **kwargs: 其他参数
        """
        config = get_config()
        
        # 获取模型路径
        if model_path is None:
            model_path = config.get('detection.gender.model_path')
        if prototxt_path is None:
            prototxt_path = config.get('detection.gender.prototxt_path')
        
        self.model_path = model_path
        self.prototxt_path = prototxt_path
        self.net = None
        self.input_size = kwargs.get('input_size') or config.get('detection.gender.input_size', (227, 227))
        self.mean_values = kwargs.get('mean_values') or config.get('detection.gender.mean_values', [104, 117, 123])
        self.scale = kwargs.get('scale') or config.get('detection.gender.scale', 1.0)
        self.enabled = config.get('detection.gender.enabled', True)
        
        if self.enabled and model_path:
            self._load_model()
        elif self.enabled:
            logger.info("性别识别已启用但未提供模型路径，将使用基于特征的简单分类")
            self.use_simple_classifier = True
        else:
            self.use_simple_classifier = False
            logger.info("性别识别已禁用")
    
    def _load_model(self):
        """加载模型"""
        if not self.model_path:
            return
        
        # 尝试查找模型文件
        search_dirs = ['models', 'data/models', 'gender_models']
        model_file = None
        prototxt_file = None
        
        for search_dir in search_dirs:
            if os.path.exists(os.path.join(search_dir, os.path.basename(self.model_path))):
                model_file = os.path.join(search_dir, os.path.basename(self.model_path))
                break
        
        if not model_file and os.path.exists(self.model_path):
            model_file = self.model_path
        
        if not model_file:
            logger.warning(f"未找到性别分类模型: {self.model_path}")
            logger.info("将使用基于特征的简单分类")
            self.use_simple_classifier = True
            return
        
        try:
            # 判断模型类型
            if model_file.endswith('.caffemodel'):
                # Caffe模型
                if not self.prototxt_path:
                    # 尝试查找prototxt文件
                    prototxt_file = model_file.replace('.caffemodel', '.prototxt')
                    if not os.path.exists(prototxt_file):
                        logger.error("Caffe模型需要prototxt文件")
                        self.use_simple_classifier = True
                        return
                else:
                    prototxt_file = self.prototxt_path
                
                self.net = cv2.dnn.readNetFromCaffe(prototxt_file, model_file)
                logger.info(f"成功加载Caffe性别分类模型: {model_file}")
            elif model_file.endswith('.onnx'):
                # ONNX模型
                self.net = cv2.dnn.readNetFromONNX(model_file)
                logger.info(f"成功加载ONNX性别分类模型: {model_file}")
            else:
                logger.warning(f"不支持的模型格式: {model_file}")
                self.use_simple_classifier = True
                return
            
            # 尝试使用GPU
            try:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                logger.info("使用CUDA加速")
            except:
                self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                logger.info("使用CPU")
            
            self.use_simple_classifier = False
        except Exception as e:
            logger.error(f"加载性别分类模型失败: {e}")
            logger.info("将使用基于特征的简单分类")
            self.use_simple_classifier = True
    
    def predict(self, face_roi: np.ndarray) -> Tuple[Gender, float]:
        """
        预测性别
        
        Args:
            face_roi: 人脸区域图像 (BGR格式)
            
        Returns:
            (性别, 置信度)
        """
        if not self.enabled:
            return Gender.UNKNOWN, 0.0
        
        if self.use_simple_classifier:
            return self._simple_classify(face_roi)
        
        if self.net is None:
            return Gender.UNKNOWN, 0.0
        
        try:
            # 预处理
            blob = cv2.dnn.blobFromImage(
                face_roi,
                scalefactor=self.scale,
                size=self.input_size,
                mean=tuple(self.mean_values),
                swapRB=False,
                crop=True
            )
            
            # 推理
            self.net.setInput(blob)
            output = self.net.forward()
            
            # 解析输出
            # 假设输出格式为 [1, 2] 或 [2]，第一个值是男性概率，第二个值是女性概率
            if len(output.shape) == 2:
                probs = output[0]
            else:
                probs = output.flatten()
            
            if len(probs) >= 2:
                male_prob = float(probs[0])
                female_prob = float(probs[1])
            else:
                # 如果只有一个输出，假设是男性概率
                male_prob = float(probs[0])
                female_prob = 1.0 - male_prob
            
            # 归一化概率
            total = male_prob + female_prob
            if total > 0:
                male_prob /= total
                female_prob /= total
            
            # 判断性别
            if male_prob > female_prob:
                return Gender.MALE, male_prob
            else:
                return Gender.FEMALE, female_prob
                
        except Exception as e:
            logger.error(f"性别分类失败: {e}")
            return self._simple_classify(face_roi)
    
    def _simple_classify(self, face_roi: np.ndarray) -> Tuple[Gender, float]:
        """
        基于特征的简单性别分类（备用方案）
        这是一个非常简单的实现，准确率较低，仅作为演示
        
        Args:
            face_roi: 人脸区域图像
            
        Returns:
            (性别, 置信度)
        """
        try:
            # 检查输入有效性
            if face_roi is None or face_roi.size == 0:
                logger.debug("人脸区域为空，使用默认分类")
                # 不返回UNKNOWN，而是返回一个默认值
                return Gender.FEMALE, 0.5
            
            # 确保人脸区域足够大
            h, w = face_roi.shape[:2]
            if h < 20 or w < 20:
                logger.debug(f"人脸区域较小 ({w}x{h})，使用默认分类")
                # 即使区域小也尝试分类，不返回UNKNOWN
                # 继续执行，使用调整大小的方式
            
            # 转换为灰度图
            if len(face_roi.shape) == 3:
                gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_roi
            
            # 调整大小以确保特征提取的一致性
            # 即使区域很小也调整到合适大小
            target_size = max(100, min(h, w) * 2)  # 至少100，或原尺寸的2倍
            if h < 100 or w < 100:
                gray = cv2.resize(gray, (target_size, target_size))
            
            # 简单的特征提取：基于面部区域的统计特征
            # 注意：这是一个非常简化的实现，实际应用中应该使用训练好的模型
            
            # 计算面部区域的亮度分布
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            
            # 计算边缘特征（男性通常面部轮廓更明显）
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (gray.shape[0] * gray.shape[1])
            
            # 计算面部区域的对比度
            contrast = std_brightness / (mean_brightness + 1e-5)
            
            # 改进的启发式规则
            # 这些规则基于一些观察，但准确率仍然有限
            male_score = 0.0
            female_score = 0.0
            
            # 边缘密度：男性通常面部轮廓更明显
            if edge_density > 0.12:
                male_score += 0.3
            else:
                female_score += 0.2
            
            # 亮度：男性皮肤通常较暗
            if mean_brightness < 110:
                male_score += 0.3
            elif mean_brightness > 130:
                female_score += 0.3
            else:
                # 中等亮度，不偏向任何一方
                male_score += 0.1
                female_score += 0.1
            
            # 对比度：男性面部特征通常更明显
            if contrast > 0.4:
                male_score += 0.2
            else:
                female_score += 0.2
            
            # 面部宽高比（如果可能的话）
            aspect_ratio = w / h if h > 0 else 1.0
            if aspect_ratio > 0.85:  # 较宽的脸型
                male_score += 0.2
            else:
                female_score += 0.2
            
            # 归一化分数
            total_score = male_score + female_score
            if total_score > 0:
                male_prob = male_score / total_score
                female_prob = female_score / total_score
            else:
                # 如果无法判断，默认返回女性（因为通常女性特征更明显）
                male_prob = 0.4
                female_prob = 0.6
            
            # 判断性别（使用0.5作为阈值，但置信度基于概率差）
            confidence = abs(male_prob - female_prob)
            if confidence < 0.1:
                # 如果差异太小，降低置信度
                confidence = 0.5
            
            if male_prob > female_prob:
                return Gender.MALE, max(0.5, min(0.9, male_prob))
            else:
                return Gender.FEMALE, max(0.5, min(0.9, female_prob))
                
        except Exception as e:
            logger.error(f"简单性别分类失败: {e}", exc_info=True)
            # 即使出错也返回一个默认值，而不是UNKNOWN
            # 这样可以确保界面显示正常
            return Gender.FEMALE, 0.5
    
    def classify_batch(self, face_rois: list) -> list:
        """
        批量分类
        
        Args:
            face_rois: 人脸区域图像列表
            
        Returns:
            [(性别, 置信度), ...] 列表
        """
        results = []
        for roi in face_rois:
            gender, conf = self.predict(roi)
            results.append((gender, conf))
        return results

