"""
Yolo-FastestV2轻量级检测器
"""

import cv2
import numpy as np
import os
from typing import List, Tuple, Optional

from ..utils.logger import get_logger
from ..utils.file_utils import find_file
from ..config import get_config

logger = get_logger(__name__)


class YoloFastestV2Detector:
    """Yolo-FastestV2检测器"""
    
    def __init__(self, model_path: Optional[str] = None, conf_threshold: Optional[float] = None, **kwargs):
        """
        初始化Yolo-FastestV2模型
        
        Args:
            model_path: 模型文件路径（ONNX格式）
            conf_threshold: 置信度阈值
            **kwargs: 其他参数
        """
        config = get_config()
        
        if model_path is None:
            model_path = config.get('detection.fastestv2.model_path', 'yolo_fastestv2/model.onnx')
        
        if conf_threshold is None:
            conf_threshold = config.get('detection.fastestv2.conf_threshold', 0.25)
        
        self.conf_threshold = conf_threshold
        self.imgsz = kwargs.get('imgsz') or config.get('detection.fastestv2.imgsz', 416)
        self.net = None
        
        # 查找模型文件
        search_dirs = ['yolo_fastestv2', 'data/models', 'models']
        found_path = find_file(os.path.basename(model_path), search_dirs)
        if found_path:
            model_path = found_path
        
        try:
            if os.path.exists(model_path):
                logger.info(f"加载Yolo-FastestV2模型: {model_path}")
                self.net = cv2.dnn.readNetFromONNX(model_path)
                # 尝试使用GPU加速
                try:
                    self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                    self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                    logger.info("使用CUDA加速")
                except:
                    self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                    self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                    logger.info("使用CPU")
            else:
                logger.warning(f"模型文件不存在: {model_path}")
                logger.info("提示: 请先下载或训练Yolo-FastestV2模型")
        except Exception as e:
            logger.error(f"加载模型失败: {e}")
    
    def detect(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float, int]]:
        """
        检测人脸
        
        Args:
            frame: 输入图像帧
            
        Returns:
            faces: 检测到的人脸列表
        """
        if self.net is None:
            return []
        
        # 预处理
        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (self.imgsz, self.imgsz),
            swapRB=True, crop=False
        )
        
        self.net.setInput(blob)
        outputs = self.net.forward()
        
        # 解析输出
        faces = []
        h, w = frame.shape[:2]
        
        if len(outputs) > 0:
            output = outputs[0]
            if len(output.shape) == 3:
                output = output[0]  # 移除batch维度
            
            # 假设输出格式为 [num_detections, 6] (x, y, w, h, conf, cls)
            for detection in output:
                if len(detection) >= 6:
                    x, y, w_det, h_det, conf, cls = detection[:6]
                    if conf > self.conf_threshold:
                        # 转换为像素坐标
                        x1 = int((x - w_det/2) * w)
                        y1 = int((y - h_det/2) * h)
                        x2 = int((x + w_det/2) * w)
                        y2 = int((y + h_det/2) * h)
                        faces.append((x1, y1, x2, y2, conf, int(cls)))
        
        return faces
    
    def draw_detections(
        self,
        frame: np.ndarray,
        faces: List[Tuple[int, int, int, int, float, int]],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """
        在图像上绘制检测结果
        
        Args:
            frame: 输入图像帧
            faces: 检测到的人脸列表
            color: 绘制颜色
            thickness: 线条粗细
            
        Returns:
            frame: 绘制了检测框的图像
        """
        for (x1, y1, x2, y2, conf, cls) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            label = f'Face {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, thickness)
        return frame

