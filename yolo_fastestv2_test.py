"""
Yolo-FastestV2人脸检测测试
使用Yolo-FastestV2轻量级模型进行人脸检测
"""

import cv2
import numpy as np
import time
import os


class YoloFastestV2Detector:
    """Yolo-FastestV2检测器"""
    
    def __init__(self, model_path='yolo_fastestv2/model.onnx', conf_threshold=0.25):
        """
        初始化Yolo-FastestV2模型
        
        Args:
            model_path: 模型文件路径（ONNX格式）
            conf_threshold: 置信度阈值
        """
        self.conf_threshold = conf_threshold
        self.net = None
        
        try:
            if os.path.exists(model_path):
                print(f"加载Yolo-FastestV2模型: {model_path}")
                self.net = cv2.dnn.readNetFromONNX(model_path)
                # 尝试使用GPU加速
                try:
                    self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                    self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                    print("使用CUDA加速")
                except:
                    self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
                    self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
                    print("使用CPU")
            else:
                print(f"模型文件不存在: {model_path}")
                print("提示: 请先下载或训练Yolo-FastestV2模型")
        except Exception as e:
            print(f"加载模型失败: {e}")
    
    def detect(self, frame):
        """
        检测人脸
        
        Args:
            frame: 输入图像帧
            
        Returns:
            faces: 检测到的人脸列表
        """
        if self.net is None:
            return []
        
        # 预处理
        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (416, 416), 
            swapRB=True, crop=False
        )
        
        self.net.setInput(blob)
        outputs = self.net.forward()
        
        # 解析输出（这里需要根据实际模型输出格式调整）
        faces = []
        h, w = frame.shape[:2]
        
        # Yolo-FastestV2输出格式通常是 [batch, num_detections, 85]
        # 85 = 4 (bbox) + 1 (objectness) + 80 (classes)
        # 对于人脸检测，可能只有1个类别
        
        # 这里是一个简化的解析示例，实际需要根据模型输出调整
        if len(outputs) > 0:
            output = outputs[0]
            if len(output.shape) == 3:
                output = output[0]  # 移除batch维度
            
            # 假设输出格式为 [num_detections, 6] (x, y, w, h, conf, cls)
            # 实际格式需要根据模型确定
            for detection in output:
                if len(detection) >= 6:
                    x, y, w_det, h_det, conf, cls = detection[:6]
                    if conf > self.conf_threshold:
                        # 转换为像素坐标
                        x1 = int((x - w_det/2) * w)
                        y1 = int((y - h_det/2) * h)
                        x2 = int((x + w_det/2) * w)
                        y2 = int((y + h_det/2) * h)
                        faces.append((x1, y1, x2, y2, conf, int(cls)))
        
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
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'Face {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame


def main():
    """主测试函数"""
    print("初始化Yolo-FastestV2检测器...")
    print("注意: 需要先准备Yolo-FastestV2的ONNX模型文件")
    
    detector = YoloFastestV2Detector()
    
    if detector.net is None:
        print("\n无法加载模型，使用OpenCV Haar级联器作为替代...")
        from cv_test import HaarFaceDetector
        detector = HaarFaceDetector()
        use_haar = True
    else:
        use_haar = False
    
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    print("开始检测，按 'q' 键退出...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 检测
        if use_haar:
            faces = detector.detect(frame)
            frame = detector.draw_detections(frame, faces)
        else:
            faces = detector.detect(frame)
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
        if use_haar:
            cv2.putText(frame, 'Using Haar (FastestV2 not available)', (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow('Yolo-FastestV2 Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("检测结束")


if __name__ == '__main__':
    main()

