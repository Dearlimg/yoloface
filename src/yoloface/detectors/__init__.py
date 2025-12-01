"""
检测器模块
"""

from .haar_detector import HaarFaceDetector
from .yolo11_detector import YOLO11FaceDetector
from .fastestv2_detector import YoloFastestV2Detector
from .face_tracker import FaceTracker

__all__ = [
    'HaarFaceDetector',
    'YOLO11FaceDetector',
    'YoloFastestV2Detector',
    'FaceTracker'
]

