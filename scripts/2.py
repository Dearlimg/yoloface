import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # 优化摄像头打开方式，提升跨平台兼容性
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows下加CAP_DSHOW避免延迟/卡死
        # Linux系统可替换为：self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

        # 设置摄像头缓冲区大小，减少延迟
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            print("无法打开摄像头，请检查摄像头是否被占用或索引是否正确")
            sys.exit()

        # 定时器用于刷新摄像头图像
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 每 30 毫秒刷新一次（约30帧/秒）

    def initUI(self):
        # 设置窗口布局
        self.layout = QVBoxLayout()

        # 用于显示图像的 QLabel
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        # 退出按钮
        self.quit_button = QPushButton("退出", self)
        self.quit_button.clicked.connect(self.close_app)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)
        self.setWindowTitle("摄像头图像显示")
        self.resize(800, 600)

    def update_frame(self):
        # 修复核心笔误：正确读取摄像头帧
        ret, frame = self.cap.read()
        if not ret:
            print("无法读取摄像头帧，可能摄像头已断开")
            return

        # 转换为 RGB 格式（OpenCV默认BGR，PyQt5需要RGB）
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 转换为 QImage 适配PyQt5显示
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 缩放图像至QLabel大小，避免变形
        pixmap = QPixmap.fromImage(q_image).scaled(
            self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.video_label.setPixmap(pixmap)

    def close_app(self):
        # 释放摄像头并退出程序
        self.cap.release()
        self.timer.stop()
        self.close()

    def closeEvent(self, event):
        # 确保关闭窗口时释放摄像头资源
        self.cap.release()
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    camera_app = CameraApp()
    camera_app.show()
    sys.exit(app.exec_())