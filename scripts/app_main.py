"""
基于EAIDK-310的人脸识别系统主程序
使用PyQt5创建GUI界面
"""

import sys
import time

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox,
                             QTextEdit, QGroupBox)

from age_detector import AgeDetector
from cv_test import HaarFaceDetector
from gender_detector import GenderDetector
from login_ui import LoginRegisterDialog
from yolo_fastestv2_test import YoloFastestV2Detector
from yolo_test import YOLO11FaceDetector
from yolo_track import FaceTracker


class VideoThread(QThread):
    """视频处理线程"""
    frame_ready = pyqtSignal(np.ndarray, int, float)  # frame, detection_count, fps
    
    def __init__(self, detector_type='haar', enable_gender=False, enable_age=False):
        super().__init__()
        self.detector_type = detector_type
        self.detector = None
        self.tracker = None
        self.running = False
        self.cap = None
        self.enable_gender = enable_gender
        self.gender_detector = None
        self.enable_age = enable_age
        self.age_detector = None
        self.init_detector()
    
    def init_detector(self):
        """初始化检测器"""
        try:
            if self.detector_type == 'haar':
                self.detector = HaarFaceDetector(enable_gender=self.enable_gender)
                if self.enable_age:
                    self.detector.enable_age_detection()
            elif self.detector_type == 'yolo11':
                self.detector = YOLO11FaceDetector(enable_gender=self.enable_gender)
                if self.enable_age:
                    self.detector.enable_age_detection()
            elif self.detector_type == 'fastestv2':
                self.detector = YoloFastestV2Detector()
                if self.enable_gender:
                    self.gender_detector = GenderDetector(model_type='simple')
                if self.enable_age:
                    self.age_detector = AgeDetector(model_type='simple')
            elif self.detector_type == 'track':
                self.tracker = FaceTracker(enable_gender=self.enable_gender)
                if self.enable_age:
                    self.tracker.enable_age_detection()
            print(f"检测器初始化成功: {self.detector_type}")
            if self.enable_gender:
                print("性别识别已启用")
            if self.enable_age:
                print("年龄识别已启用")
        except Exception as e:
            print(f"检测器初始化失败: {e}")
    
    def change_detector(self, detector_type):
        """切换检测器"""
        self.detector_type = detector_type
        self.init_detector()
    
    def start_capture(self):
        """开始捕获"""
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                return False
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.running = True
        return True
    
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
        
        frame_count = 0
        start_time = time.time()
        fps = 0
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 检测
            if self.detector_type == 'track':
                tracks = self.tracker.detect_and_track(frame)
                frame = self.tracker.draw_tracks(frame, tracks)
                detection_count = len(tracks)
            elif self.detector_type in ['haar', 'yolo11']:
                if self.enable_age and self.enable_gender and hasattr(self.detector, 'detect_with_age_and_gender'):
                    # 同时启用年龄和性别识别
                    detections = self.detector.detect_with_age_and_gender(frame)
                    frame = self.detector.draw_detections_with_age_and_gender(frame, detections)
                elif self.enable_age and hasattr(self.detector, 'detect_with_age'):
                    # 仅启用年龄识别
                    detections = self.detector.detect_with_age(frame)
                    frame = self.detector.draw_detections_with_age(frame, detections)
                elif self.enable_gender and hasattr(self.detector, 'detect_with_gender'):
                    # 仅启用性别识别
                    detections = self.detector.detect_with_gender(frame)
                    frame = self.detector.draw_detections_with_gender(frame, detections)
                else:
                    # 基础检测
                    faces = self.detector.detect(frame)
                    frame = self.detector.draw_detections(frame, faces)
                    detections = faces
                detection_count = len(detections)
            elif self.detector_type == 'fastestv2':
                faces = self.detector.detect(frame)
                if self.enable_age and self.enable_gender and self.age_detector and self.gender_detector:
                    # 同时启用年龄和性别识别
                    detections_with_age_and_gender = []
                    for x1, y1, x2, y2, conf, cls in faces:
                        age_label, age_range, age_conf = self.age_detector.detect_age(frame, (x1, y1, x2, y2))
                        gender, gender_conf = self.gender_detector.detect_gender(frame, (x1, y1, x2, y2))
                        detections_with_age_and_gender.append((x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf))
                    frame = self._draw_detections_with_age_and_gender(frame, detections_with_age_and_gender)
                elif self.enable_age and self.age_detector:
                    # 仅启用年龄识别
                    detections_with_age = []
                    for x1, y1, x2, y2, conf, cls in faces:
                        age_label, age_range, age_conf = self.age_detector.detect_age(frame, (x1, y1, x2, y2))
                        detections_with_age.append((x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf))
                    frame = self._draw_detections_with_age(frame, detections_with_age)
                elif self.enable_gender and self.gender_detector:
                    # 仅启用性别识别
                    detections_with_gender = []
                    for x1, y1, x2, y2, conf, cls in faces:
                        gender, gender_conf = self.gender_detector.detect_gender(frame, (x1, y1, x2, y2))
                        detections_with_gender.append((x1, y1, x2, y2, conf, cls, gender, gender_conf))
                    frame = self._draw_detections_with_gender(frame, detections_with_gender)
                else:
                    frame = self.detector.draw_detections(frame, faces)
                detection_count = len(faces)
            else:
                detection_count = 0
            
            # 计算FPS
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = 30 / elapsed
                start_time = time.time()
            
            # 添加信息文本
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Detections: {detection_count}', (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 显示启用的功能
            y_offset = 110
            if self.enable_gender:
                cv2.putText(frame, 'Gender Detection: ON', (10, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                y_offset += 30
            if self.enable_age:
                cv2.putText(frame, 'Age Detection: ON', (10, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # 发送帧
            self.frame_ready.emit(frame, detection_count, fps)
            
            self.msleep(33)  # ~30 FPS
        
        self.stop_capture()

    def _draw_detections_with_gender(self, frame, detections):
        """绘制带性别信息的检测结果"""
        for x1, y1, x2, y2, conf, cls, gender, gender_conf in detections:
            # 根据性别选择颜色
            if gender == 'Male':
                color = (255, 0, 0)  # 蓝色表示男性
            elif gender == 'Female':
                color = (0, 0, 255)  # 红色表示女性
            else:
                color = (0, 255, 0)  # 绿色表示未知

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{gender} {gender_conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame

    def _draw_detections_with_age(self, frame, detections):
        """绘制带年龄信息的检测结果"""
        from age_detector import AgeDetector

        for x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf in detections:
            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{age_label} {age_conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame

    def _draw_detections_with_age_and_gender(self, frame, detections):
        """绘制带年龄和性别信息的检测结果"""
        from age_detector import AgeDetector

        for x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf in detections:
            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制年龄标签
            age_label_text = f'{age_label} {age_conf:.2f}'
            cv2.putText(frame, age_label_text, (x1, y1 - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # 绘制性别标签
            gender_label_text = f'{gender} {gender_conf:.2f}'
            cv2.putText(frame, gender_label_text, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, username=None):
        super().__init__()
        self.video_thread = None
        self.current_user = username
        self.enable_gender = False  # 性别识别开关
        self.enable_age = False     # 年龄识别开关
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        title = '基于EAIDK-310的人脸识别系统'
        if self.current_user:
            title += f' - 用户: {self.current_user}'
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1200, 800)
        
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
        
        # 性别识别开关
        from PyQt5.QtWidgets import QCheckBox
        self.gender_checkbox = QCheckBox('启用性别识别')
        self.gender_checkbox.stateChanged.connect(self.toggle_gender_detection)
        algo_layout.addWidget(self.gender_checkbox)

        # 年龄识别开关
        self.age_checkbox = QCheckBox('启用年龄识别')
        self.age_checkbox.stateChanged.connect(self.toggle_age_detection)
        algo_layout.addWidget(self.age_checkbox)

        algo_group.setLayout(algo_layout)
        right_layout.addWidget(algo_group)
        
        # 统计信息
        #111
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
    
    def log(self, message):
        """添加日志"""
        self.log_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def change_algorithm(self, index):
        """切换算法"""
        algorithms = ['haar', 'yolo11', 'fastestv2', 'track']
        if self.video_thread and self.video_thread.running:
            self.video_thread.change_detector(algorithms[index])
            self.log(f"切换到算法: {self.algo_combo.currentText()}")
    
    def toggle_gender_detection(self, state):
        """切换性别识别"""
        from PyQt5.QtCore import Qt
        self.enable_gender = state == Qt.Checked
        if self.video_thread and self.video_thread.running:
            self.video_thread.enable_gender = self.enable_gender
            status = "已启用" if self.enable_gender else "已禁用"
            self.log(f"性别识别{status}")
        else:
            status = "已启用" if self.enable_gender else "已禁用"
            self.log(f"性别识别{status}（下次检测时生效）")

    def toggle_age_detection(self, state):
        """切换年龄识别"""
        from PyQt5.QtCore import Qt
        self.enable_age = state == Qt.Checked
        if self.video_thread and self.video_thread.running:
            self.video_thread.enable_age = self.enable_age
            status = "已启用" if self.enable_age else "已禁用"
            self.log(f"年龄识别{status}")
        else:
            status = "已启用" if self.enable_age else "已禁用"
            self.log(f"年龄识别{status}（下次检测时生效）")

    def start_detection(self):
        """开始检测"""
        if self.video_thread and self.video_thread.running:
            return
        
        algorithm_map = {'Haar级联器': 'haar', 'YOLO11': 'yolo11', 
                        'Yolo-FastestV2': 'fastestv2', '人脸跟踪': 'track'}
        algo_name = self.algo_combo.currentText()
        algo_type = algorithm_map[algo_name]
        
        self.video_thread = VideoThread(algo_type, enable_gender=self.enable_gender, enable_age=self.enable_age)
        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.algo_combo.setEnabled(False)
        self.gender_checkbox.setEnabled(False)
        self.age_checkbox.setEnabled(False)
        
        features = []
        if self.enable_gender:
            features.append("性别识别")
        if self.enable_age:
            features.append("年龄识别")
        features_status = f" ({', '.join(features)}已启用)" if features else ""
        self.log(f"开始检测，使用算法: {algo_name}{features_status}")
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
        self.gender_checkbox.setEnabled(True)
        self.age_checkbox.setEnabled(True)
        
        self.video_label.clear()
        self.video_label.setText('检测已停止')
        self.fps_label.setText('FPS: 0.00')
        self.detection_label.setText('检测数量: 0')
        
        self.log("检测已停止")
        self.statusBar().showMessage('就绪')
    
    def update_frame(self, frame, detection_count, fps):
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


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 显示登录注册对话框
    login_dialog = LoginRegisterDialog()
    if login_dialog.exec_() == LoginRegisterDialog.Accepted:
        # 登录成功，显示主窗口
        username = login_dialog.current_user
        window = MainWindow(username)
        window.show()
        sys.exit(app.exec_())
    else:
        # 用户取消登录
        sys.exit(0)


if __name__ == '__main__':
    main()

