"""
检测器模块
"""

from .haar_detector import HaarFaceDetector
from .yolo11_detector import YOLO11FaceDetector
from .fastestv2_detector import YoloFastestV2Detector
from .face_tracker import FaceTracker
from .gender_classifier import GenderClassifier, Gender

__all__ = [
    'HaarFaceDetector',
    'YOLO11FaceDetector',
    'YoloFastestV2Detector',
    'FaceTracker',
    'GenderClassifier',
    'Gender'
]

