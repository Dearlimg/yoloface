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
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # 绘制标签和置信度
            label = f'Person {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, thickness)
        
        return frame

