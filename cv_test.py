"""
OpenCV Haar级联器人脸检测测试
使用OpenCV的Haar级联分类器进行人脸检测
"""

import cv2
import numpy as np
import time


class HaarFaceDetector:
    """Haar级联分类器人脸检测器"""
    
    def __init__(self, cascade_path='haarcascades/haarcascade_frontalface_default.xml'):
        """
        初始化Haar级联分类器
        
        Args:
            cascade_path: Haar级联分类器文件路径
        """
        try:
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            if self.face_cascade.empty():
                raise ValueError(f"无法加载级联分类器: {cascade_path}")
        except Exception as e:
            print(f"初始化Haar级联分类器失败: {e}")
            # 尝试使用OpenCV内置的级联分类器
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
    
    def detect(self, frame):
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
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def draw_detections(self, frame, faces):
        """
        在图像上绘制检测结果
        
        Args:
            frame: 输入图像帧
            faces: 检测到的人脸列表
            
        Returns:
            frame: 绘制了检测框的图像
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return frame


def main():
    """主测试函数"""
    print("初始化Haar级联分类器人脸检测器...")
    detector = HaarFaceDetector()
    
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    print("开始检测，按 'q' 键退出...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头画面")
            break
        
        # 检测人脸
        faces = detector.detect(frame)
        
        # 绘制检测结果
        frame = detector.draw_detections(frame, faces)
        
        # 计算FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = 30 / elapsed
            start_time = time.time()
        
        # 显示信息
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Faces: {len(faces)}', (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Haar Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("检测结束")


if __name__ == '__main__':
    main()

