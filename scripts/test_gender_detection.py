"""
性别识别功能测试脚本
演示如何使用性别识别功能
"""

import sys

import cv2

from cv_test import HaarFaceDetector
from gender_detector import GenderDetector
from yolo_test import YOLO11FaceDetector
from yolo_track import FaceTracker


def test_haar_with_gender():
    """测试 Haar 检测器 + 性别识别"""
    print("=" * 50)
    print("测试 Haar 检测器 + 性别识别")
    print("=" * 50)

    detector = HaarFaceDetector(enable_gender=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并识别性别
        detections = detector.detect_with_gender(frame)

        # 绘制结果
        frame = detector.draw_detections_with_gender(frame, detections)

        # 显示统计信息
        male_count = sum(1 for _, _, _, _, _, gender, _ in detections if gender == 'Male')
        female_count = sum(1 for _, _, _, _, _, gender, _ in detections if gender == 'Female')

        cv2.putText(frame, f'Male: {male_count}, Female: {female_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Haar + Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_yolo11_with_gender():
    """测试 YOLO11 检测器 + 性别识别"""
    print("=" * 50)
    print("测试 YOLO11 检测器 + 性别识别")
    print("=" * 50)

    detector = YOLO11FaceDetector(enable_gender=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并识别性别
        detections = detector.detect_with_gender(frame)

        # 绘制结果
        frame = detector.draw_detections_with_gender(frame, detections)

        # 显示统计信息
        male_count = sum(1 for _, _, _, _, _, _, gender, _ in detections if gender == 'Male')
        female_count = sum(1 for _, _, _, _, _, _, gender, _ in detections if gender == 'Female')

        cv2.putText(frame, f'Male: {male_count}, Female: {female_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('YOLO11 + Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_tracker_with_gender():
    """测试人脸跟踪器 + 性别识别"""
    print("=" * 50)
    print("测试人脸跟踪器 + 性别识别")
    print("=" * 50)

    tracker = FaceTracker(enable_gender=True)
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
        male_count = sum(1 for _, track_data in tracks.items()
                        if len(track_data) == 8 and track_data[6] == 'Male')
        female_count = sum(1 for _, track_data in tracks.items()
                          if len(track_data) == 8 and track_data[6] == 'Female')

        cv2.putText(frame, f'Male: {male_count}, Female: {female_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Face Tracking + Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_gender_detector_only():
    """测试独立的性别识别器"""
    print("=" * 50)
    print("测试独立的性别识别器")
    print("=" * 50)

    gender_detector = GenderDetector(model_type='simple')
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

        # 为每个人脸检测性别
        for x, y, w, h in faces:
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

        cv2.imshow('Gender Detector Only', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def main():
    """主测试函数"""
    print("\n性别识别功能测试")
    print("=" * 50)
    print("选择要测试的功能:")
    print("1. Haar 检测器 + 性别识别")
    print("2. YOLO11 检测器 + 性别识别")
    print("3. 人脸跟踪器 + 性别识别")
    print("4. 独立性别识别器")
    print("0. 退出")
    print("=" * 50)

    choice = input("请选择 (0-4): ").strip()

    if choice == '1':
        test_haar_with_gender()
    elif choice == '2':
        test_yolo11_with_gender()
    elif choice == '3':
        test_tracker_with_gender()
    elif choice == '4':
        test_gender_detector_only()
    elif choice == '0':
        print("退出")
        sys.exit(0)
    else:
        print("无效选择")


if __name__ == '__main__':
    main()

