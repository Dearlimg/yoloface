"""
YOLO11人脸检测测试
使用Ultralytics YOLO11进行人脸检测
支持性别识别功能
"""

import time

import cv2
from ultralytics import YOLO


class YOLO11FaceDetector:
    """YOLO11人脸检测器"""
    
    def __init__(self, model_path='models/yolo11n.pt', conf_threshold=0.25, enable_gender=False):
        """
        初始化YOLO11模型
        
        Args:
            model_path: YOLO11模型文件路径
            conf_threshold: 置信度阈值
            enable_gender: 是否启用性别识别
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
    
        # 初始化性别识别器
        self.gender_detector = None
        if enable_gender:
            try:
                from gender_detector import GenderDetector
                self.gender_detector = GenderDetector(model_type='simple')
            except Exception as e:
                print(f"初始化性别识别器失败: {e}")

        # 初始化年龄识别器
        self.age_detector = None
        self.enable_age = False

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
    
    def detect_with_gender(self, frame):
        """
        检测人脸并识别性别

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x1, y1, x2, y2, conf, cls, gender, gender_conf)
        """
        faces = self.detect(frame)

        if self.gender_detector is None:
            # 如果没有性别识别器，返回原始结果
            return [(x1, y1, x2, y2, conf, cls, 'Unknown', 0.0) for x1, y1, x2, y2, conf, cls in faces]

        detections = []
        for x1, y1, x2, y2, conf, cls in faces:
            gender, gender_conf = self.gender_detector.detect_gender(frame, (x1, y1, x2, y2))
            detections.append((x1, y1, x2, y2, conf, cls, gender, gender_conf))

        return detections

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

    def draw_detections_with_gender(self, frame, detections):
        """
        在图像上绘制检测结果和性别信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表 (x1, y1, x2, y2, conf, cls, gender, gender_conf)

        Returns:
            frame: 绘制了检测框和性别信息的图像
        """
        for detection in detections:
            if len(detection) == 8:
                x1, y1, x2, y2, conf, cls, gender, gender_conf = detection
            else:
                x1, y1, x2, y2, conf, cls = detection
                gender, gender_conf = 'Unknown', 0.0

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

    def enable_age_detection(self):
        """启用年龄识别"""
        try:
            from age_detector import AgeDetector
            self.age_detector = AgeDetector(model_type='simple')
            self.enable_age = True
            print("年龄识别已启用")
        except Exception as e:
            print(f"启用年龄识别失败: {e}")

    def detect_with_age(self, frame):
        """
        检测人脸并识别年龄

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf)
        """
        faces = self.detect(frame)

        if self.age_detector is None:
            # 如果没有年龄识别器，返回原始结果
            return [(x1, y1, x2, y2, conf, cls, 'Unknown', (0, 0), 0.0) for x1, y1, x2, y2, conf, cls in faces]

        detections = []
        for x1, y1, x2, y2, conf, cls in faces:
            age_label, age_range, age_conf = self.age_detector.detect_age(frame, (x1, y1, x2, y2))
            detections.append((x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf))

        return detections

    def detect_with_age_and_gender(self, frame):
        """
        检测人脸并同时识别年龄和性别

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf)
        """
        faces = self.detect(frame)

        detections = []
        for x1, y1, x2, y2, conf, cls in faces:
            # 检测年龄
            if self.age_detector is not None:
                age_label, age_range, age_conf = self.age_detector.detect_age(frame, (x1, y1, x2, y2))
            else:
                age_label, age_range, age_conf = 'Unknown', (0, 0), 0.0

            # 检测性别
            if self.gender_detector is not None:
                gender, gender_conf = self.gender_detector.detect_gender(frame, (x1, y1, x2, y2))
            else:
                gender, gender_conf = 'Unknown', 0.0

            detections.append((x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf))

        return detections

    def draw_detections_with_age(self, frame, detections):
        """
        在图像上绘制检测结果和年龄信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表 (x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf)

        Returns:
            frame: 绘制了检测框和年龄信息的图像
        """
        from age_detector import AgeDetector

        for detection in detections:
            if len(detection) == 9:
                x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf = detection
            else:
                x1, y1, x2, y2, conf, cls = detection
                age_label, age_range, age_conf = 'Unknown', (0, 0), 0.0

            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{age_label} {age_conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return frame

    def draw_detections_with_age_and_gender(self, frame, detections):
        """
        在图像上绘制检测结果、年龄和性别信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表 (x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf)

        Returns:
            frame: 绘制了检测框、年龄和性别信息的图像
        """
        from age_detector import AgeDetector

        for detection in detections:
            if len(detection) == 11:
                x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf, gender, gender_conf = detection
            else:
                continue

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

