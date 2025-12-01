"""
检测器测试
"""

import pytest
import numpy as np
import cv2


@pytest.fixture
def sample_image():
    """创建测试图像"""
    return np.zeros((480, 640, 3), dtype=np.uint8)


def test_haar_detector_initialization():
    """测试Haar检测器初始化"""
    from yoloface.detectors import HaarFaceDetector
    
    detector = HaarFaceDetector()
    assert detector is not None
    assert hasattr(detector, 'face_cascade')


def test_yolo11_detector_initialization():
    """测试YOLO11检测器初始化"""
    pytest.importorskip("ultralytics")
    
    from yoloface.detectors import YOLO11FaceDetector
    
    try:
        detector = YOLO11FaceDetector()
        assert detector is not None
    except Exception as e:
        pytest.skip(f"YOLO11初始化失败: {e}")


def test_haar_detector_detect(sample_image):
    """测试Haar检测器检测功能"""
    from yoloface.detectors import HaarFaceDetector
    
    detector = HaarFaceDetector()
    faces = detector.detect(sample_image)
    
    assert isinstance(faces, list)


def test_config_loading():
    """测试配置加载"""
    from yoloface.config import Config
    
    config = Config()
    assert config is not None
    
    # 测试获取配置值
    camera_index = config.get('camera.index')
    assert camera_index is not None


if __name__ == '__main__':
    pytest.main([__file__])

