"""
快速测试年龄识别显示
验证英文标签是否正确显示
"""

import cv2

from cv_test import HaarFaceDetector


def test_age_display():
    """测试年龄识别显示"""
    print("=" * 50)
    print("年龄识别显示测试")
    print("=" * 50)

    # 初始化检测器
    detector = HaarFaceDetector()
    detector.enable_age_detection()

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("开始检测，按 'q' 键退出...")
    print("年龄标签应该显示为英文，例如: Child(0-12), Teen(13-19), Young(20-35), Adult(36-50), Senior(51+)")

    frame_count = 0
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

        # 显示帧数
        frame_count += 1
        cv2.putText(frame, f'Frame: {frame_count}', (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Age Detection Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("测试完成")

if __name__ == '__main__':
    test_age_display()

