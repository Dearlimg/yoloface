"""
同时测试年龄识别和性别识别功能
"""

import cv2

from cv_test import HaarFaceDetector
from yolo_test import YOLO11FaceDetector


def test_haar_with_age_and_gender():
    """测试 Haar 检测器 + 年龄识别 + 性别识别"""
    print("=" * 50)
    print("测试 Haar 检测器 + 年龄识别 + 性别识别")
    print("=" * 50)

    detector = HaarFaceDetector(enable_gender=True)
    detector.enable_age_detection()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")
    print("显示格式: 年龄标签 置信度 (上方) / 性别 置信度 (下方)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并同时识别年龄和性别
        detections = detector.detect_with_age_and_gender(frame)

        # 绘制结果
        frame = detector.draw_detections_with_age_and_gender(frame, detections)

        # 显示统计信息
        age_counts = {}
        gender_counts = {}
        for _, _, _, _, age_label, _, _, gender, _ in detections:
            age_counts[age_label] = age_counts.get(age_label, 0) + 1
            gender_counts[gender] = gender_counts.get(gender, 0) + 1

        y_offset = 30
        cv2.putText(frame, 'Age Distribution:', (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_offset += 25
        for age_label, count in sorted(age_counts.items()):
            cv2.putText(frame, f'  {age_label}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            y_offset += 20

        y_offset += 10
        cv2.putText(frame, 'Gender Distribution:', (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_offset += 25
        for gender, count in sorted(gender_counts.items()):
            cv2.putText(frame, f'  {gender}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            y_offset += 20

        cv2.imshow('Haar + Age + Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def test_yolo11_with_age_and_gender():
    """测试 YOLO11 检测器 + 年龄识别 + 性别识别"""
    print("=" * 50)
    print("测试 YOLO11 检测器 + 年龄识别 + 性别识别")
    print("=" * 50)

    detector = YOLO11FaceDetector(enable_gender=True)
    detector.enable_age_detection()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")
    print("显示格式: 年龄标签 置信度 (上方) / 性别 置信度 (下方)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸并同时识别年龄和性别
        detections = detector.detect_with_age_and_gender(frame)

        # 绘制结果
        frame = detector.draw_detections_with_age_and_gender(frame, detections)

        # 显示统计信息
        age_counts = {}
        gender_counts = {}
        for _, _, _, _, _, _, age_label, _, _, gender, _ in detections:
            age_counts[age_label] = age_counts.get(age_label, 0) + 1
            gender_counts[gender] = gender_counts.get(gender, 0) + 1

        y_offset = 30
        cv2.putText(frame, 'Age Distribution:', (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_offset += 25
        for age_label, count in sorted(age_counts.items()):
            cv2.putText(frame, f'  {age_label}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            y_offset += 20

        y_offset += 10
        cv2.putText(frame, 'Gender Distribution:', (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_offset += 25
        for gender, count in sorted(gender_counts.items()):
            cv2.putText(frame, f'  {gender}: {count}', (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            y_offset += 20

        cv2.imshow('YOLO11 + Age + Gender Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")


def main():
    """主测试函数"""
    print("\n同时启用年龄识别和性别识别功能测试")
    print("=" * 50)
    print("选择要测试的功能:")
    print("1. Haar 检测器 + 年龄识别 + 性别识别")
    print("2. YOLO11 检测器 + 年龄识别 + 性别识别")
    print("0. 退出")
    print("=" * 50)

    choice = input("请选择 (0-2): ").strip()

    if choice == '1':
        test_haar_with_age_and_gender()
    elif choice == '2':
        test_yolo11_with_age_and_gender()
    elif choice == '0':
        print("退出")
    else:
        print("无效选择")


if __name__ == '__main__':
    main()

