"""
OpenCV Haar级联器人脸检测测试
使用OpenCV的Haar级联分类器进行人脸检测
支持性别识别功能
"""

import time

import cv2


class HaarFaceDetector:
    """Haar级联分类器人脸检测器"""

    def __init__(self, cascade_path='haarcascades/haarcascade_frontalface_default.xml', enable_gender=False):
        """
        初始化Haar级联分类器

        Args:
            cascade_path: Haar级联分类器文件路径
            enable_gender: 是否启用性别识别
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

    def detect_with_gender(self, frame):
        """
        检测人脸并识别性别

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x, y, w, h, gender, gender_conf)
        """
        faces = self.detect(frame)

        if self.gender_detector is None:
            # 如果没有性别识别器，返回原始结果
            return [(x, y, w, h, 'Unknown', 0.0) for x, y, w, h in faces]

        detections = []
        for x, y, w, h in faces:
            gender, conf = self.gender_detector.detect_gender(frame, (x, y, x + w, y + h))
            detections.append((x, y, w, h, gender, conf))

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
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return frame

    def draw_detections_with_gender(self, frame, detections):
        """
        在图像上绘制检测结果和性别信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表 (x, y, w, h, gender, gender_conf)

        Returns:
            frame: 绘制了检测框和性别信息的图像
        """
        for detection in detections:
            if len(detection) == 6:
                x, y, w, h, gender, gender_conf = detection
            else:
                x, y, w, h = detection
                gender, gender_conf = 'Unknown', 0.0

            # 根据性别选择颜色
            if gender == 'Male':
                color = (255, 0, 0)  # 蓝色表示男性
            elif gender == 'Female':
                color = (0, 0, 255)  # 红色表示女性
            else:
                color = (0, 255, 0)  # 绿色表示未知

            # 绘制边界框
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # 绘制标签
            label = f'{gender} {gender_conf:.2f}'
            cv2.putText(frame, label, (x, y - 10),
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
            detections: 检测结果列表，每个元素为 (x, y, w, h, age_label, age_range, age_conf)
        """
        faces = self.detect(frame)

        if self.age_detector is None:
            # 如果没有年龄识别器，返回原始结果
            return [(x, y, w, h, 'Unknown', (0, 0), 0.0) for x, y, w, h in faces]

        detections = []
        for x, y, w, h in faces:
            age_label, age_range, conf = self.age_detector.detect_age(frame, (x, y, x + w, y + h))
            detections.append((x, y, w, h, age_label, age_range, conf))

        return detections

    def draw_detections_with_age(self, frame, detections):
        """
        在图像上绘制检测结果和年龄信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表 (x, y, w, h, age_label, age_range, age_conf)

        Returns:
            frame: 绘制了检测框和年龄信息的图像
        """
        from age_detector import AgeDetector

        for detection in detections:
            if len(detection) == 7:
                x, y, w, h, age_label, age_range, age_conf = detection
            else:
                x, y, w, h = detection
                age_label, age_range, age_conf = 'Unknown', (0, 0), 0.0

            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # 绘制标签
            label = f'{age_label} {age_conf:.2f}'
            cv2.putText(frame, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

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

