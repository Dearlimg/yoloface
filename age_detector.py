"""
年龄识别模块
使用深度学习模型或启发式方法进行年龄估计
支持多种检测器的年龄识别功能
"""

from pathlib import Path

import cv2
import numpy as np


class AgeDetector:
    """年龄识别器 - 基于人脸特征的年龄分类"""

    # 年龄段定义
    AGE_RANGES = {
        'child': (0, 12),      # 儿童
        'teen': (13, 19),      # 青少年
        'young_adult': (20, 35),  # 年轻成人
        'adult': (36, 50),     # 中年
        'senior': (51, 100)    # 老年
    }

    AGE_LABELS = ['儿童(0-12)', '青少年(13-19)', '年轻成人(20-35)', '中年(36-50)', '老年(51+)']

    def __init__(self, model_type='simple'):
        """
        初始化年龄识别器

        Args:
            model_type: 模型类型 ('simple' 使用启发式方法, 'deep' 使用深度学习)
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
        print("初始化简单年龄识别模型（基于人脸特征启发式）")
        self.model_type = 'simple'

    def _init_deep_model(self):
        """初始化深度学习模型"""
        print("初始化深度学习年龄识别模型...")

        # 尝试加载预训练的年龄识别模型
        model_dir = Path('models/age_net')

        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
            print(f"模型目录已创建: {model_dir}")
            print("请下载年龄识别模型文件到 models/age_net 目录")
            print("可以从以下链接下载:")
            print("- age_net.caffemodel")
            print("- age_net.prototxt")
            self.model_type = 'simple'  # 降级到简单模型
            return

        proto_file = model_dir / 'age_net.prototxt'
        model_file = model_dir / 'age_net.caffemodel'

        if proto_file.exists() and model_file.exists():
            try:
                self.model = cv2.dnn.readNetFromCaffe(
                    str(proto_file),
                    str(model_file)
                )
                self.proto_file = proto_file
                self.model_file = model_file
                print("深度学习年龄识别模型加载成功")
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

    def detect_age(self, frame, face_box):
        """
        检测人脸的年龄

        Args:
            frame: 输入图像帧
            face_box: 人脸边界框 (x1, y1, x2, y2)

        Returns:
            age_label: 年龄段标签 ('儿童', '青少年', '年轻成人', '中年', '老年')
            age_range: 年龄范围 (min_age, max_age)
            confidence: 置信度 (0-1)
        """
        x1, y1, x2, y2 = face_box

        # 确保坐标有效
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        if x2 <= x1 or y2 <= y1:
            return 'Unknown', (0, 0), 0.0

        # 提取人脸区域
        face_roi = frame[y1:y2, x1:x2]

        if self.model_type == 'deep' and self.model is not None:
            return self._detect_age_deep(face_roi)
        else:
            return self._detect_age_simple(face_roi)

    def _detect_age_deep(self, face_roi):
        """
        使用深度学习模型检测年龄

        Args:
            face_roi: 人脸区域图像

        Returns:
            age_label: 年龄段标签
            age_range: 年龄范围
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
            age_idx = predictions[0].argmax()
            confidence = float(predictions[0][age_idx])

            age_label = self.AGE_LABELS[age_idx]
            age_range = list(self.AGE_RANGES.values())[age_idx]

            return age_label, age_range, confidence
        except Exception as e:
            print(f"深度学习年龄检测失败: {e}")
            return self._detect_age_simple(face_roi)

    def _detect_age_simple(self, face_roi):
        """
        使用启发式方法检测年龄
        基于人脸特征的简单启发式规则

        Args:
            face_roi: 人脸区域图像

        Returns:
            age_label: 年龄段标签
            age_range: 年龄范围
            confidence: 置信度
        """
        try:
            # 转换为灰度图
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            # 计算人脸特征
            h, w = gray.shape

            if h < 10 or w < 10:
                return 'Unknown', (0, 0), 0.5

            # 特征1: 皱纹检测 (年龄越大皱纹越多)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            wrinkle_score = np.sum(np.abs(laplacian)) / (h * w)

            # 特征2: 皮肤光滑度 (年龄越大皮肤越粗糙)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            smoothness = np.sum(np.abs(gray.astype(float) - blur.astype(float))) / (h * w)

            # 特征3: 对比度 (年龄越大对比度越高)
            contrast = gray.std()

            # 特征4: 亮度 (年龄越大皮肤越暗)
            brightness = gray.mean()

            # 特征5: 边缘密度 (年龄越大边缘越多)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (h * w)

            # 特征6: 颜色分布 (使用 HSV)
            hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)

            # 计算各年龄段的评分
            scores = {
                'child': 0.0,
                'teen': 0.0,
                'young_adult': 0.0,
                'adult': 0.0,
                'senior': 0.0
            }

            # 皱纹评分 (年龄越大皱纹越多)
            if wrinkle_score < 5:
                scores['child'] += 0.3
                scores['teen'] += 0.2
            elif wrinkle_score < 10:
                scores['teen'] += 0.3
                scores['young_adult'] += 0.2
            elif wrinkle_score < 15:
                scores['young_adult'] += 0.3
                scores['adult'] += 0.2
            elif wrinkle_score < 20:
                scores['adult'] += 0.3
                scores['senior'] += 0.2
            else:
                scores['senior'] += 0.3
                scores['adult'] += 0.1

            # 皮肤光滑度评分 (年龄越大皮肤越粗糙)
            if smoothness < 5:
                scores['child'] += 0.25
                scores['teen'] += 0.15
            elif smoothness < 10:
                scores['teen'] += 0.25
                scores['young_adult'] += 0.15
            elif smoothness < 15:
                scores['young_adult'] += 0.25
                scores['adult'] += 0.15
            elif smoothness < 20:
                scores['adult'] += 0.25
                scores['senior'] += 0.15
            else:
                scores['senior'] += 0.25
                scores['adult'] += 0.1

            # 对比度评分 (年龄越大对比度越高)
            if contrast < 20:
                scores['child'] += 0.2
            elif contrast < 30:
                scores['teen'] += 0.2
                scores['young_adult'] += 0.1
            elif contrast < 40:
                scores['young_adult'] += 0.2
                scores['adult'] += 0.1
            elif contrast < 50:
                scores['adult'] += 0.2
                scores['senior'] += 0.1
            else:
                scores['senior'] += 0.2
                scores['adult'] += 0.1

            # 亮度评分 (年龄越大皮肤越暗)
            if brightness > 130:
                scores['child'] += 0.15
                scores['teen'] += 0.1
            elif brightness > 110:
                scores['teen'] += 0.15
                scores['young_adult'] += 0.1
            elif brightness > 90:
                scores['young_adult'] += 0.15
                scores['adult'] += 0.1
            elif brightness > 70:
                scores['adult'] += 0.15
                scores['senior'] += 0.1
            else:
                scores['senior'] += 0.15
                scores['adult'] += 0.1

            # 边缘密度评分 (年龄越大边缘越多)
            if edge_density < 0.08:
                scores['child'] += 0.1
            elif edge_density < 0.12:
                scores['teen'] += 0.1
                scores['young_adult'] += 0.05
            elif edge_density < 0.16:
                scores['young_adult'] += 0.1
                scores['adult'] += 0.05
            elif edge_density < 0.20:
                scores['adult'] += 0.1
                scores['senior'] += 0.05
            else:
                scores['senior'] += 0.1
                scores['adult'] += 0.05

            # 找出评分最高的年龄段
            best_age_group = max(scores, key=scores.get)
            confidence = scores[best_age_group]

            # 归一化置信度
            total_score = sum(scores.values())
            if total_score > 0:
                confidence = min(confidence / total_score, 1.0)
            else:
                confidence = 0.5

            # 获取年龄范围
            age_range = self.AGE_RANGES[best_age_group]
            age_label = self.AGE_LABELS[list(self.AGE_RANGES.keys()).index(best_age_group)]

            return age_label, age_range, confidence

        except Exception as e:
            print(f"启发式年龄检测失败: {e}")
            return 'Unknown', (0, 0), 0.5

    def detect_ages_batch(self, frame, face_boxes):
        """
        批量检测多个人脸的年龄

        Args:
            frame: 输入图像帧
            face_boxes: 人脸边界框列表 [(x1, y1, x2, y2), ...]

        Returns:
            ages: 年龄列表 [(age_label, age_range, conf), ...]
        """
        ages = []
        for face_box in face_boxes:
            age_label, age_range, conf = self.detect_age(frame, face_box)
            ages.append((age_label, age_range, conf))
        return ages

    @staticmethod
    def get_age_color(age_label):
        """
        根据年龄段获取颜色

        Args:
            age_label: 年龄段标签

        Returns:
            color: BGR 颜色元组
        """
        color_map = {
            '儿童(0-12)': (0, 255, 255),      # 黄色
            '青少年(13-19)': (255, 0, 255),   # 紫色
            '年轻成人(20-35)': (0, 255, 0),   # 绿色
            '中年(36-50)': (0, 165, 255),     # 橙色
            '老年(51+)': (255, 0, 0),         # 蓝色
            'Unknown': (128, 128, 128)        # 灰色
        }
        return color_map.get(age_label, (128, 128, 128))


class AgeAwareDetector:
    """年龄感知的检测器包装类 - 为任何检测器添加年龄识别功能"""

    def __init__(self, base_detector, age_model_type='simple'):
        """
        初始化年龄感知检测器

        Args:
            base_detector: 基础检测器对象
            age_model_type: 年龄识别模型类型
        """
        self.base_detector = base_detector
        self.age_detector = AgeDetector(model_type=age_model_type)

    def detect_with_age(self, frame):
        """
        检测人脸并识别年龄

        Args:
            frame: 输入图像帧

        Returns:
            detections: 检测结果列表，每个元素为 (x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf)
        """
        # 首先进行人脸检测
        faces = self.base_detector.detect(frame)

        # 为每个人脸检测年龄
        detections_with_age = []

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

            # 检测年龄
            age_label, age_range, age_conf = self.age_detector.detect_age(frame, (x1, y1, x2, y2))

            detections_with_age.append((x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf))

        return detections_with_age

    def draw_detections_with_age(self, frame, detections):
        """
        绘制检测结果和年龄信息

        Args:
            frame: 输入图像帧
            detections: 检测结果列表

        Returns:
            frame: 绘制了检测框和年龄信息的图像
        """
        for detection in detections:
            if len(detection) == 9:
                x1, y1, x2, y2, conf, cls, age_label, age_range, age_conf = detection
            else:
                continue

            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{age_label} {age_conf:.2f}'
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
    """测试年龄识别功能"""
    print("初始化年龄识别器...")
    age_detector = AgeDetector(model_type='simple')

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

        # 检测年龄
        for (x, y, w, h) in faces:
            x1, y1, x2, y2 = x, y, x + w, y + h
            age_label, age_range, conf = age_detector.detect_age(frame, (x1, y1, x2, y2))

            # 根据年龄段选择颜色
            color = AgeDetector.get_age_color(age_label)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f'{age_label} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Age Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("检测结束")


if __name__ == '__main__':
    main()

