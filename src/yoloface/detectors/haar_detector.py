"""
Haar级联分类器人脸检测器
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger(__name__)


class HaarFaceDetector:
    """Haar级联分类器人脸检测器"""
    
    def __init__(self, cascade_path: Optional[str] = None, **kwargs):
        """
        初始化Haar级联分类器
        
        Args:
            cascade_path: Haar级联分类器文件路径，如果为None则使用配置或默认
            **kwargs: 其他参数（scale_factor, min_neighbors, min_size）
        """
        config = get_config()
        
        # 获取级联分类器路径
        if cascade_path is None:
            cascade_path = config.get('detection.haar.cascade_path')
        
        # 加载级联分类器
        try:
            if cascade_path:
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if self.face_cascade.empty():
                    raise ValueError(f"无法加载级联分类器: {cascade_path}")
                logger.info(f"加载级联分类器: {cascade_path}")
            else:
                # 使用OpenCV内置的级联分类器
                default_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(default_path)
                logger.info("使用OpenCV内置级联分类器")
        except Exception as e:
            logger.warning(f"初始化级联分类器失败: {e}，使用默认分类器")
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        
        # 检测参数
        self.scale_factor = kwargs.get('scale_factor') or config.get('detection.haar.scale_factor', 1.1)
        self.min_neighbors = kwargs.get('min_neighbors') or config.get('detection.haar.min_neighbors', 5)
        self.min_size = kwargs.get('min_size') or config.get('detection.haar.min_size', (30, 30))
    
    def detect(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        检测人脸
        
        Args:
            frame: 输入图像帧
            
        Returns:
            faces: 检测到的人脸列表，格式为 [(x, y, w, h), ...]
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces.tolist() if len(faces) > 0 else []
    
    def draw_detections(
        self,
        frame: np.ndarray,
        faces: List[Tuple[int, int, int, int]],
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
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
            cv2.putText(frame, 'Face', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, thickness)
        return frame

