"""
YOLO11人脸检测测试
使用Ultralytics YOLO11进行人脸检测
"""

import cv2
import numpy as np
import time
from ultralytics import YOLO


class YOLO11FaceDetector:
    """YOLO11人脸检测器"""
    
    def __init__(self, model_path='models/yolo11n.pt', conf_threshold=0.25):
        """
        初始化YOLO11模型
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
        """
        try:
            print(f"加载YOLO11模型: {model_path}")
            self.model = YOLO(model_path)
            self.conf_threshold = conf_threshold
            print("YOLO11模型加载成功")
        except Exception as e:
            print(f"加载YOLO11模型失败: {e}")
            print("尝试使用预训练模型...")
            self.model = YOLO('yolo11n.pt')  # 使用Ultralytics提供的预训练模型
            self.conf_threshold = conf_threshold
    
    def detect(self, frame):
        """
        检测人脸
        
        Args:
            frame: 输入图像帧
            
        Returns:
            faces: 检测到的人脸列表，格式为 [(x1, y1, x2, y2, conf, cls), ...]
        """
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
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
    
    def draw_detections(self, frame, faces):
        """
        在图像上绘制检测结果
        
        Args:
            frame: 输入图像帧
            faces: 检测到的人脸列表
            
        Returns:
            frame: 绘制了检测框的图像
        """
        for (x1, y1, x2, y2, conf, cls) in faces:
            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 绘制标签和置信度
            label = f'Person {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame


def main():
    """主测试函数"""
    print("初始化YOLO11人脸检测器...")
    detector = YOLO11FaceDetector()
    
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
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
        cv2.putText(frame, f'Detections: {len(faces)}', (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('YOLO11 Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("检测结束")


if __name__ == '__main__':
    main()

