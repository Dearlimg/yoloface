"""
旧脚本兼容性模块
将旧的脚本导入重定向到新的模块结构
"""

import sys
from pathlib import Path

# 添加src目录到路径
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# 为了向后兼容，创建别名
from yoloface.detectors import (
    HaarFaceDetector,
    YOLO11FaceDetector,
    YoloFastestV2Detector,
    FaceTracker
)

# 导出到全局命名空间（用于旧脚本）
__all__ = [
    'HaarFaceDetector',
    'YOLO11FaceDetector',
    'YoloFastestV2Detector',
    'FaceTracker'
]

