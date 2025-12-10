"""
性别识别模块
使用深度学习模型进行性别识别（男/女）
支持多种检测器的性别识别功能
"""

from pathlib import Path

import cv2
import numpy as np


class GenderDetector:
    """性别识别器 - 基于人脸特征的性别分类"""

    def __init__(self, model_type='simple'):
        """
        初始化性别识别器

        Args:
            model_type: 模型类型 ('simple' 使用简单启发式方法, 'deep' 使用深度学习)
        """
        self.model_type = model_type
        self.model = None
        self.proto_file = None
        self.model_file = None

        if model_type == 'deep':
            self._init_deep_model()
        else:
            self._init_simple_model()

    def _init_simple_model(self):
        """初始化简单启发式模型"""
        print("初始化简单性别识别模型（基于人脸特征启发式）")
        self.model_type = 'simple'

    def _init_deep_model(self):
        """初始化深度学习模型"""
        print("初始化深度学习性别识别模型...")

        # 尝试加载预训练的性别识别模型
        # 这里使用 OpenCV 的 DNN 模块加载 Caffe 模型
        model_dir = Path('models/gender_net')

        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
            print(f"模型目录已创建: {model_dir}")
            print("请下载性别识别模型文件到 models/gender_net 目录")
            print("可以从以下链接下载:")
            print("- gender_net.caffemodel")
            print("- gender_net.prototxt")
            self.model_type = 'simple'  # 降级到简单模型
            return

        proto_file = model_dir / 'gender_net.prototxt'
        model_file = model_dir / 'gender_net.caffemodel'

        if proto_file.exists() and model_file.exists():
            try:
                self.model = cv2.dnn.readNetFromCaffe(
                    str(proto_file),
                    str(model_file)
                )
                self.proto_file = proto_file
                self.model_file = model_file
                print("深度学习性别识别模型加载成功")
            except Exception as e:
                print(f"加载深度学习模型失败: {e}")
                print("降级到简单启发式模型")
                self.model_type = 'simple'
        else:
            print(f"模型文件不存在")
            print(f"- Proto: {proto_file}")
            print(f"- Model: {model_file}")
            print("降级到简单启发式模型")
            self.model_type = 'simple'

    def detect_gender(self, frame, face_box):
        """
        检测人脸的性别

        Args:
            frame: 输入图像帧
            face_box: 人脸边界框 (x1, y1, x2, y2)

        Returns:
            gender: 性别标签 ('Male' 或 'Female')
            confidence: 置信度 (0-1)
        """
        x1, y1, x2, y2 = face_box

        # 确保坐标有效
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        if x2 <= x1 or y2 <= y1:
            return 'Unknown', 0.0

        # 提取人脸区域
        face_roi = frame[y1:y2, x1:x2]

        if self.model_type == 'deep' and self.model is not None:
            return self._detect_gender_deep(face_roi)
        else:
            return self._detect_gender_simple(face_roi)

    def _detect_gender_deep(self, face_roi):
        """
        使用深度学习模型检测性别

        Args:
            face_roi: 人脸区域图像

        Returns:
            gender: 性别标签
            confidence: 置信度
        """
        try:
            # 预处理
            blob = cv2.dnn.blobFromImage(
                face_roi,
                1.0,
                (227, 227),
                [104.0, 117.0, 123.0],
                swapRB=False
            )

            # 前向传播
            self.model.setInput(blob)
            predictions = self.model.forward()

            # 解析输出
            gender_list = ['Male', 'Female']
            gender_idx = predictions[0].argmax()
            confidence = float(predictions[0][gender_idx])

            return gender_list[gender_idx], confidence
        except Exception as e:
            print(f"深度学习性别检测失败: {e}")
            return self._detect_gender_simple(face_roi)

    def _detect_gender_simple(self, face_roi):
        """
        使用启发式方法检测性别
        基于人脸特征的改进启发式规则

        Args:
            face_roi: 人脸区域图像

        Returns:
            gender: 性别标签
            confidence: 置信度
        """
        try:
            # 转换为灰度图
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            # 计算人脸特征
            h, w = gray.shape

            if h < 10 or w < 10:
                return 'Unknown', 0.5

            # 特征1: 人脸宽高比 (男性通常更宽)
            aspect_ratio = w / h if h > 0 else 1.0

            # 特征2: 边缘检测 (男性通常有更多棱角和胡须)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (h * w)

            # 特征3: 皮肤颜色分析
            hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)

            # 皮肤颜色范围 (HSV) - 扩大范围以更好地检测
            lower_skin = np.array([0, 10, 60], dtype=np.uint8)
            upper_skin = np.array([25, 255, 255], dtype=np.uint8)

            skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
            skin_ratio = np.sum(skin_mask > 0) / (h * w)

            # 特征4: 对比度 (男性通常对比度更高，因为胡须)
            contrast = gray.std()

            # 特征5: 亮度 (男性皮肤通常更暗)
            brightness = gray.mean()

            # 特征6: 纹理复杂度 (男性通常有更复杂的纹理)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            texture_complexity = np.sum(np.abs(laplacian)) / (h * w)

            # 综合判断 - 改进的评分系统
            male_score = 0.0
            female_score = 0.0

            # 宽高比: 男性通常更宽
            if aspect_ratio > 1.0:
                male_score += 0.25
            else:
                female_score += 0.15

            # 边缘密度: 男性更多棱角和胡须
            if edge_density > 0.12:
                male_score += 0.3
            elif edge_density < 0.08:
                female_score += 0.25
            else:
                male_score += 0.15

            # 皮肤比例: 女性皮肤更均匀
            if skin_ratio > 0.5:
                female_score += 0.2
            elif skin_ratio < 0.3:
                male_score += 0.2

            # 对比度: 男性对比度更高
            if contrast > 35:
                male_score += 0.25
            elif contrast < 25:
                female_score += 0.2
            else:
                male_score += 0.1

            # 亮度: 男性皮肤通常更暗
            if brightness < 100:
                male_score += 0.15
            elif brightness > 130:
                female_score += 0.15

            # 纹理复杂度: 男性通常有更复杂的纹理
            if texture_complexity > 15:
                male_score += 0.2
            elif texture_complexity < 8:
                female_score += 0.15
            else:
                male_score += 0.1

            # 决策
            total_score = male_score + female_score
            if total_score == 0:
                return 'Unknown', 0.5

            if male_score > female_score:
                gender = 'Male'
                confidence = min(male_score / total_score, 1.0)
            else:
                gender = 'Female'
                confidence = min(female_score / total_score, 1.0)

            return gender, confidence

        except Exception as e:
            print(f"启发式性别检测失败: {e}")
            return 'Unknown', 0.5

    def detect_genders_batch(self, frame, face_boxes):
        """
        批量检测多个人脸的性别

        Args:
            frame: 输入图像帧
            face_boxes: 人脸边界框列表 [(x1, y1, x2, y2), ...]

        Returns:
            genders: 性别列表 [('Male', conf), ('Female', conf), ...]
        """
        genders = []
        for face_box in face_boxes:
            gender, conf = self.detect_gender(frame, face_box)
            genders.append((gender, conf))
        return genders


class GenderAwareDetector:
    """性别感知的检测器包装类 - 为任何检测器添加性别识别功能"""

    def __init__(self, base_detector, gender_model_type='simple'):
        """
        初始化性别感知检测器

        Args:
            base_detector: 基础检测器对象 (HaarFaceDetector, YOLO11FaceDetector 等)
            gender_model_type: 性别识别模型类型
        """
        self.base_detector = base_detector
        self.gender_detector = GenderDetector(model_type=gender_model_type)

    def detect_with_gender(self, frame):
        """
        检测人脸并识别性别

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x1, y1, x2, y2, conf, cls, gender, gender_conf)
        """
        # 首先进行人脸检测
        faces = self.base_detector.detect(frame)

        # 为每个人脸检测性别
        detections_with_gender = []

        for face in faces:
            # 处理不同格式的检测结果
            if len(face) == 4:  # Haar 格式: (x, y, w, h)
                x, y, w, h = face
                x1, y1, x2, y2 = x, y, x + w, y + h
                conf, cls = 0.9, 0
            elif len(face) == 6:  # YOLO 格式: (x1, y1, x2, y2, conf, cls)
                x1, y1, x2, y2, conf, cls = face
            else:
                continue

            # 检测性别
            gender, gender_conf = self.gender_detector.detect_gender(frame, (x1, y1, x2, y2))

            detections_with_gender.append((x1, y1, x2, y2, conf, cls, gender, gender_conf))

        return detections_with_gender

    def draw_detections_with_gender(self, frame, detections):
        """
        绘制检测结果和性别信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表

        Returns:
            frame: 绘制了检测框和性别信息的图像
        """
        for detection in detections:
            if len(detection) == 8:
                x1, y1, x2, y2, conf, cls, gender, gender_conf = detection
            else:
                continue

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

    def detect(self, frame):
        """兼容基础检测器的 detect 方法"""
        return self.base_detector.detect(frame)

    def draw_detections(self, frame, faces):
        """兼容基础检测器的 draw_detections 方法"""
        return self.base_detector.draw_detections(frame, faces)


def main():
    """测试性别识别功能"""
    print("初始化性别识别器...")
    gender_detector = GenderDetector(model_type='simple')

    print("打开摄像头...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 导入人脸检测器
    from cv_test import HaarFaceDetector
    face_detector = HaarFaceDetector()

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸
        faces = face_detector.detect(frame)

        # 检测性别
        for (x, y, w, h) in faces:
            x1, y1, x2, y2 = x, y, x + w, y + h
            gender, conf = gender_detector.detect_gender(frame, (x1, y1, x2, y2))

            # 根据性别选择颜色
            if gender == 'Male':
                color = (255, 0, 0)  # 蓝色
            else:
                color = (0, 0, 255)  # 红色

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{gender} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("检测结束")


if __name__ == '__main__':
    main()

