"""
视频处理工具模块
"""

import cv2
import numpy as np
import time
from typing import Tuple, Optional


class VideoCapture:
    """视频捕获封装类"""
    
    def __init__(self, index: int = 0, width: int = 640, height: int = 480):
        """
        初始化视频捕获
        
        Args:
            index: 摄像头索引
            width: 视频宽度
            height: 视频高度
        """
        self.index = index
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        self._open()
    
    def _open(self):
        """打开摄像头"""
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise RuntimeError(f"无法打开摄像头 {self.index}")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        读取一帧
        
        Returns:
            (成功标志, 图像帧)
        """
        if self.cap is None:
            return False, None
        return self.cap.read()
    
    def release(self):
        """释放资源"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def is_opened(self) -> bool:
        """检查是否已打开"""
        return self.cap is not None and self.cap.isOpened()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class FPSCounter:
    """FPS计数器"""
    
    def __init__(self, update_interval: int = 30):
        """
        初始化FPS计数器
        
        Args:
            update_interval: 更新间隔（帧数）
        """
        self.update_interval = update_interval
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0
    
    def update(self) -> float:
        """
        更新FPS
        
        Returns:
            当前FPS值
        """
        self.frame_count += 1
        
        if self.frame_count % self.update_interval == 0:
            elapsed = time.time() - self.start_time
            self.fps = self.update_interval / elapsed if elapsed > 0 else 0.0
            self.start_time = time.time()
        
        return self.fps
    
    def reset(self):
        """重置计数器"""
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0


def draw_info(
    frame: np.ndarray,
    fps: float,
    detection_count: int,
    algorithm: str = "",
    position: Tuple[int, int] = (10, 30),
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    在图像上绘制信息
    
    Args:
        frame: 输入图像
        fps: FPS值
        detection_count: 检测数量
        algorithm: 算法名称
        position: 文字起始位置
        font_scale: 字体大小
        color: 文字颜色
        thickness: 文字粗细
        
    Returns:
        绘制了信息的图像
    """
    x, y = position
    line_height = 40
    
    # FPS
    cv2.putText(frame, f'FPS: {fps:.2f}', (x, y),
               cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
    
    # 检测数量
    cv2.putText(frame, f'Detections: {detection_count}', (x, y + line_height),
               cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
    
    # 算法名称
    if algorithm:
        cv2.putText(frame, f'Algorithm: {algorithm}', (x, y + line_height * 2),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.7, color, thickness)
    
    return frame

