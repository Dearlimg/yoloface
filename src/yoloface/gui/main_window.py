"""
主窗口GUI
"""

import sys
import cv2
import numpy as np
import time
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QComboBox,
    QTextEdit, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from ..detectors import HaarFaceDetector, YOLO11FaceDetector, YoloFastestV2Detector, FaceTracker
from ..utils.logger import get_logger
from ..utils.video import VideoCapture, FPSCounter, draw_info
from ..config import Config

logger = get_logger(__name__)


class VideoThread(QThread):
    """视频处理线程"""
    frame_ready = pyqtSignal(np.ndarray, int, float)  # frame, detection_count, fps
    
    def __init__(self, detector_type: str, config: Config):
        super().__init__()
        self.detector_type = detector_type
        self.config = config
        self.detector = None
        self.tracker = None
        self.running = False
        self.cap: Optional[VideoCapture] = None
        self.fps_counter = FPSCounter(
            config.get('performance.fps_update_interval', 30)
        )
        self.init_detector()
    
    def init_detector(self):
        """初始化检测器"""
        try:
            if self.detector_type == 'haar':
                self.detector = HaarFaceDetector()
            elif self.detector_type == 'yolo11':
                self.detector = YOLO11FaceDetector()
            elif self.detector_type == 'fastestv2':
                self.detector = YoloFastestV2Detector()
            elif self.detector_type == 'track':
                self.tracker = FaceTracker()
            logger.info(f"检测器初始化成功: {self.detector_type}")
        except Exception as e:
            logger.error(f"检测器初始化失败: {e}")
    
    def change_detector(self, detector_type: str):
        """切换检测器"""
        self.detector_type = detector_type
        self.init_detector()
    
    def start_capture(self) -> bool:
        """开始捕获"""
        try:
            camera_config = self.config.get('camera', {})
            self.cap = VideoCapture(
                index=camera_config.get('index', 0),
                width=camera_config.get('width', 640),
                height=camera_config.get('height', 480)
            )
            self.running = True
            return True
        except Exception as e:
            logger.error(f"无法打开摄像头: {e}")
            return False
    
    def stop_capture(self):
        """停止捕获"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def run(self):
        """运行线程"""
        if not self.start_capture():
            return
        
        self.fps_counter.reset()
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 检测
            if self.detector_type == 'track':
                tracks = self.tracker.detect_and_track(frame)
                # 性别识别已自动集成在draw_tracks中
                frame = self.tracker.draw_tracks(frame, tracks, show_gender=True)
                detection_count = len(tracks)
            elif self.detector_type in ['haar', 'yolo11', 'fastestv2']:
                faces = self.detector.detect(frame)
                # 性别识别已自动集成在draw_detections中
                frame = self.detector.draw_detections(frame, faces, show_gender=True)
                detection_count = len(faces)
            else:
                detection_count = 0
            
            # 计算FPS
            fps = self.fps_counter.update()
            
            # 添加信息
            algorithm_names = {
                'haar': 'Haar',
                'yolo11': 'YOLO11',
                'fastestv2': 'FastestV2',
                'track': 'Tracking'
            }
            frame = draw_info(
                frame, fps, detection_count,
                algorithm_names.get(self.detector_type, '')
            )
            
            # 发送帧
            self.frame_ready.emit(frame, detection_count, fps)
            
            self.msleep(33)  # ~30 FPS
        
        self.stop_capture()


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, config: Config, username: Optional[str] = None):
        super().__init__()
        self.config = config
        self.username = username
        self.video_thread: Optional[VideoThread] = None
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        gui_config = self.config.get('gui', {})
        title = gui_config.get('window_title', '基于EAIDK-310的人脸识别系统')
        if self.username:
            title += f' - 用户: {self.username}'
        self.setWindowTitle(title)
        self.setGeometry(100, 100,
                        gui_config.get('window_width', 1200),
                        gui_config.get('window_height', 800))
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 左侧：视频显示区域
        left_layout = QVBoxLayout()
        
        # 视频显示标签
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText('点击"开始检测"按钮开始')
        self.video_label.setStyleSheet("border: 2px solid gray; background-color: black; color: white;")
        left_layout.addWidget(self.video_label)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('开始检测')
        self.start_btn.clicked.connect(self.start_detection)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton('停止检测')
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        left_layout.addLayout(button_layout)
        
        # 右侧：控制面板
        right_layout = QVBoxLayout()
        
        # 算法选择
        algo_group = QGroupBox('检测算法选择')
        algo_layout = QVBoxLayout()
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(['Haar级联器', 'YOLO11', 'Yolo-FastestV2', '人脸跟踪'])
        self.algo_combo.currentIndexChanged.connect(self.change_algorithm)
        algo_layout.addWidget(QLabel('算法:'))
        algo_layout.addWidget(self.algo_combo)
        
        algo_group.setLayout(algo_layout)
        right_layout.addWidget(algo_group)
        
        # 统计信息
        stats_group = QGroupBox('统计信息')
        stats_layout = QVBoxLayout()
        
        self.fps_label = QLabel('FPS: 0.00')
        stats_layout.addWidget(self.fps_label)
        
        self.detection_label = QLabel('检测数量: 0')
        stats_layout.addWidget(self.detection_label)
        
        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)
        
        # 日志区域
        log_group = QGroupBox('运行日志')
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        right_layout.addWidget(log_group)
        
        # 添加布局
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
    
    def log(self, message: str):
        """添加日志"""
        self.log_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        logger.info(message)
    
    def change_algorithm(self, index: int):
        """切换算法"""
        algorithms = ['haar', 'yolo11', 'fastestv2', 'track']
        if self.video_thread and self.video_thread.running:
            self.video_thread.change_detector(algorithms[index])
            self.log(f"切换到算法: {self.algo_combo.currentText()}")
    
    def start_detection(self):
        """开始检测"""
        if self.video_thread and self.video_thread.running:
            return
        
        algorithm_map = {
            'Haar级联器': 'haar',
            'YOLO11': 'yolo11',
            'Yolo-FastestV2': 'fastestv2',
            '人脸跟踪': 'track'
        }
        algo_name = self.algo_combo.currentText()
        algo_type = algorithm_map[algo_name]
        
        self.video_thread = VideoThread(algo_type, self.config)
        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.algo_combo.setEnabled(False)
        
        self.log(f"开始检测，使用算法: {algo_name}")
        self.statusBar().showMessage(f'正在检测 - {algo_name}')
    
    def stop_detection(self):
        """停止检测"""
        if self.video_thread:
            self.video_thread.stop_capture()
            self.video_thread.wait()
            self.video_thread = None
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.algo_combo.setEnabled(True)
        
        self.video_label.clear()
        self.video_label.setText('检测已停止')
        self.fps_label.setText('FPS: 0.00')
        self.detection_label.setText('检测数量: 0')
        
        self.log("检测已停止")
        self.statusBar().showMessage('就绪')
    
    def update_frame(self, frame: np.ndarray, detection_count: int, fps: float):
        """更新视频帧"""
        # 转换颜色空间
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # 缩放图像以适应标签
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)
        
        # 更新统计信息
        self.fps_label.setText(f'FPS: {fps:.2f}')
        self.detection_label.setText(f'检测数量: {detection_count}')
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.video_thread and self.video_thread.running:
            self.stop_detection()
        event.accept()

