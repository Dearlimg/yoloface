"""
YOLO11人脸检测器
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

from ..utils.logger import get_logger
from ..utils.file_utils import get_model_path
from ..config import get_config

logger = get_logger(__name__)

# 导入文本绘制工具
try:
    from ..utils.text_utils import put_chinese_text
    USE_CHINESE_TEXT = True
except ImportError:
    USE_CHINESE_TEXT = False

# 导入Gender枚举用于检查
try:
    from .gender_classifier import Gender
except ImportError:
    Gender = None

# 延迟导入性别分类器
_gender_classifier = None

def _get_gender_classifier():
    """获取性别分类器实例（单例）"""
    global _gender_classifier
    if _gender_classifier is None:
        try:
            from .gender_classifier import GenderClassifier
            _gender_classifier = GenderClassifier()
        except Exception as e:
            logger.warning(f"无法加载性别分类器: {e}")
            _gender_classifier = None
    return _gender_classifier


class YOLO11FaceDetector:
    """YOLO11人脸检测器"""
    
    def __init__(self, model_path: Optional[str] = None, conf_threshold: Optional[float] = None, **kwargs):
        """
        初始化YOLO11模型
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
            **kwargs: 其他参数
        """
        if not YOLO_AVAILABLE:
            raise ImportError("ultralytics未安装，请运行: pip install ultralytics")
        
        config = get_config()
        
        # 获取模型路径
        if model_path is None:
            model_path = config.get('detection.yolo11.model_path', 'yolo11n.pt')
        
        # 获取置信度阈值
        if conf_threshold is None:
            conf_threshold = config.get('detection.yolo11.conf_threshold', 0.25)
        
        self.conf_threshold = conf_threshold
        self.iou_threshold = kwargs.get('iou_threshold') or config.get('detection.yolo11.iou_threshold', 0.45)
        self.imgsz = kwargs.get('imgsz') or config.get('detection.yolo11.imgsz', 640)
        
        try:
            # 尝试获取完整路径
            full_path = get_model_path(model_path)
            logger.info(f"加载YOLO11模型: {full_path}")
            self.model = YOLO(full_path)
            logger.info("YOLO11模型加载成功")
        except Exception as e:
            logger.error(f"加载YOLO11模型失败: {e}")
            logger.info("尝试使用预训练模型...")
            self.model = YOLO('yolo11n.pt')  # 使用Ultralytics提供的预训练模型
    
    def detect(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float, int]]:
        """
        检测人脸
        
        Args:
            frame: 输入图像帧
            
        Returns:
            faces: 检测到的人脸列表，格式为 [(x1, y1, x2, y2, conf, cls), ...]
        """
        results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold, verbose=False)
        faces = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 只检测person类别（类别0），或者如果模型专门训练了人脸检测
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # 获取边界框坐标
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                faces.append((int(x1), int(y1), int(x2), int(y2), conf, cls))
        
        return faces
    
    def draw_detections(
        self,
        frame: np.ndarray,
        faces: List[Tuple[int, int, int, int, float, int]],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
        show_gender: bool = True
    ) -> np.ndarray:
        """
        在图像上绘制检测结果
        
        Args:
            frame: 输入图像帧
            faces: 检测到的人脸列表
            color: 绘制颜色
            thickness: 线条粗细
            show_gender: 是否显示性别
            
        Returns:
            frame: 绘制了检测框的图像
        """
        gender_classifier = _get_gender_classifier() if show_gender else None
        
        for (x1, y1, x2, y2, conf, cls) in faces:
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # 性别识别
            label = f'Person {conf:.2f}'
            if gender_classifier:
                try:
                    # 提取人体区域（确保坐标有效）
                    x1_safe = max(0, x1)
                    y1_safe = max(0, y1)
                    x2_safe = min(frame.shape[1], x2)
                    y2_safe = min(frame.shape[0], y2)
                    
                    if x2_safe > x1_safe and y2_safe > y1_safe:
                        person_roi = frame[y1_safe:y2_safe, x1_safe:x2_safe]
                        if person_roi.size > 0 and person_roi.shape[0] > 30 and person_roi.shape[1] > 30:
                            # YOLO11检测的是整个人体，需要提取人脸区域
                            # 人脸通常在人体区域的上1/3部分
                            face_region_height = int(person_roi.shape[0] * 0.4)  # 上40%区域
                            face_roi = person_roi[0:face_region_height, :]
                            
                            # 如果提取的区域太小，使用整个人体区域的上半部分
                            if face_roi.shape[0] < 30 or face_roi.shape[1] < 30:
                                face_roi = person_roi[0:int(person_roi.shape[0] * 0.5), :]
                            
                            if face_roi.size > 0 and face_roi.shape[0] > 20 and face_roi.shape[1] > 20:
                                gender, gender_conf = gender_classifier.predict(face_roi)
                                # 确保不返回UNKNOWN
                                if gender.value != "未知" and gender != Gender.UNKNOWN:
                                    label = f'{gender.value} {gender_conf:.2f}'
                                else:
                                    # 如果返回未知，使用默认标签
                                    label = f'Person {conf:.2f}'
                except Exception as e:
                    logger.debug(f"性别识别失败: {e}")
            
            # 绘制标签（支持中文）
            if USE_CHINESE_TEXT:
                frame = put_chinese_text(frame, label, (x1, y1 - 10), 
                                        font_scale=0.6, color=color, thickness=thickness)
            else:
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, thickness)
        
        return frame

