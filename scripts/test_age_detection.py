"""
年龄识别功能测试脚本
演示如何使用年龄识别功能
"""

import sys

import cv2

from age_detector import AgeDetector
from cv_test import HaarFaceDetector
from yolo_test import YOLO11FaceDetector
from yolo_track import FaceTracker


def test_haar_with_age():
    """测试 Haar 检测器 + 年龄识别"""
    print("=" * 50)
    print("测试 Haar 检测器 + 年龄识别")
    print("=" * 50)

    detector = HaarFaceDetector()
    detector.enable_age_detection()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并识别年龄
        detections = detector.detect_with_age(frame)

        # 绘制结果
        frame = detector.draw_detections_with_age(frame, detections)

        # 显示统计信息
        age_counts = {}
        for _, _, _, _, age_label, _, _ in detections:
            age_counts[age_label] = age_counts.get(age_label, 0) + 1

        y_offset = 30
        for age_label, count in sorted(age_counts.items()):
            cv2.putText(frame, f'{age_label}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 30

        cv2.imshow('Haar + Age Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_yolo11_with_age():
    """测试 YOLO11 检测器 + 年龄识别"""
    print("=" * 50)
    print("测试 YOLO11 检测器 + 年龄识别")
    print("=" * 50)

    detector = YOLO11FaceDetector()
    detector.enable_age_detection()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并识别年龄
        detections = detector.detect_with_age(frame)

        # 绘制结果
        frame = detector.draw_detections_with_age(frame, detections)

        # 显示统计信息
        age_counts = {}
        for _, _, _, _, _, _, age_label, _, _ in detections:
            age_counts[age_label] = age_counts.get(age_label, 0) + 1

        y_offset = 30
        for age_label, count in sorted(age_counts.items()):
            cv2.putText(frame, f'{age_label}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 30

        cv2.imshow('YOLO11 + Age Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_tracker_with_age():
    """测试人脸跟踪器 + 年龄识别"""
    print("=" * 50)
    print("测试人脸跟踪器 + 年龄识别")
    print("=" * 50)

    tracker = FaceTracker()
    tracker.enable_age_detection()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始跟踪，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测并跟踪
        tracks = tracker.detect_and_track(frame)

        # 绘制结果
        frame = tracker.draw_tracks(frame, tracks)

        # 显示统计信息
        age_counts = {}
        for _, track_data in tracks.items():
            if len(track_data) >= 9:
                age_label = track_data[6]
                age_counts[age_label] = age_counts.get(age_label, 0) + 1

        y_offset = 30
        for age_label, count in sorted(age_counts.items()):
            cv2.putText(frame, f'{age_label}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 30

        cv2.imshow('Face Tracking + Age Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_age_detector_only():
    """测试独立的年龄识别器"""
    print("=" * 50)
    print("测试独立的年龄识别器")
    print("=" * 50)

    age_detector = AgeDetector(model_type='simple')
    face_detector = HaarFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸
        faces = face_detector.detect(frame)

        # 为每个人脸检测年龄
        for x, y, w, h in faces:
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

        cv2.imshow('Age Detector Only', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def main():
    """主测试函数"""
    print("\n年龄识别功能测试")
    print("=" * 50)
    print("选择要测试的功能:")
    print("1. Haar 检测器 + 年龄识别")
    print("2. YOLO11 检测器 + 年龄识别")
    print("3. 人脸跟踪器 + 年龄识别")
    print("4. 独立年龄识别器")
    print("0. 退出")
    print("=" * 50)

    choice = input("请选择 (0-4): ").strip()

    if choice == '1':
        test_haar_with_age()
    elif choice == '2':
        test_yolo11_with_age()
    elif choice == '3':
        test_tracker_with_age()
    elif choice == '4':
        test_age_detector_only()
    elif choice == '0':
        print("退出")
        sys.exit(0)
    else:
        print("无效选择")


if __name__ == '__main__':
    main()

