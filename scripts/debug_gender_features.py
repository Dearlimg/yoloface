"""
性别识别特征调试脚本
用于查看和调整性别识别的各个特征值
"""

import cv2
import numpy as np

from cv_test import HaarFaceDetector


def debug_gender_features():
    """调试性别识别特征"""
    print("=" * 60)
    print("性别识别特征调试工具")
    print("=" * 60)
    print("按 'q' 退出，按 's' 保存当前帧的特征数据")
    print()

    face_detector = HaarFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 检测人脸
        faces = face_detector.detect(frame)

        # 为每个人脸分析特征
        for idx, (x, y, w, h) in enumerate(faces):
            x1, y1, x2, y2 = x, y, x + w, y + h
            face_roi = frame[y1:y2, x1:x2]

            # 计算特征
            features = calculate_gender_features(face_roi)

            # 绘制边界框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 绘制特征信息
            y_offset = y1 - 10
            for feature_name, feature_value in features.items():
                text = f"{feature_name}: {feature_value:.2f}"
                cv2.putText(frame, text, (x1, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                y_offset -= 20

            # 打印到控制台
            print(f"\n人脸 #{idx + 1} 特征:")
            print(f"  位置: ({x1}, {y1}) - ({x2}, {y2})")
            print(f"  大小: {w}x{h}")
            for feature_name, feature_value in features.items():
                print(f"  {feature_name}: {feature_value:.4f}")

        cv2.imshow('Gender Features Debug', frame)
        frame_count += 1

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f'gender_debug_frame_{frame_count}.jpg'
            cv2.imwrite(filename, frame)
            print(f"\n已保存: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("\n调试完成")


def calculate_gender_features(face_roi):
    """计算性别识别的各个特征"""
    features = {}

    try:
        # 转换为灰度图
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        if h < 10 or w < 10:
            return features

        # 特征1: 宽高比
        aspect_ratio = w / h
        features['宽高比'] = aspect_ratio

        # 特征2: 边缘密度
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (h * w)
        features['边缘密度'] = edge_density

        # 特征3: 皮肤比例
        hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 10, 60], dtype=np.uint8)
        upper_skin = np.array([25, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin_ratio = np.sum(skin_mask > 0) / (h * w)
        features['皮肤比例'] = skin_ratio

        # 特征4: 对比度
        contrast = gray.std()
        features['对比度'] = contrast

        # 特征5: 亮度
        brightness = gray.mean()
        features['亮度'] = brightness

        # 特征6: 纹理复杂度
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_complexity = np.sum(np.abs(laplacian)) / (h * w)
        features['纹理复杂度'] = texture_complexity

        # 计算评分
        male_score = 0.0
        female_score = 0.0

        if aspect_ratio > 1.0:
            male_score += 0.25
        else:
            female_score += 0.15

        if edge_density > 0.12:
            male_score += 0.3
        elif edge_density < 0.08:
            female_score += 0.25
        else:
            male_score += 0.15

        if skin_ratio > 0.5:
            female_score += 0.2
        elif skin_ratio < 0.3:
            male_score += 0.2

        if contrast > 35:
            male_score += 0.25
        elif contrast < 25:
            female_score += 0.2
        else:
            male_score += 0.1

        if brightness < 100:
            male_score += 0.15
        elif brightness > 130:
            female_score += 0.15

        if texture_complexity > 15:
            male_score += 0.2
        elif texture_complexity < 8:
            female_score += 0.15
        else:
            male_score += 0.1

        features['男性评分'] = male_score
        features['女性评分'] = female_score

        total = male_score + female_score
        if total > 0:
            features['男性概率'] = male_score / total
            features['女性概率'] = female_score / total
            gender = '男性' if male_score > female_score else '女性'
            features['预测性别'] = gender

    except Exception as e:
        print(f"计算特征失败: {e}")

    return features


def analyze_threshold():
    """分析和调整阈值"""
    print("\n" + "=" * 60)
    print("阈值分析工具")
    print("=" * 60)
    print("这个工具帮助你找到最优的特征阈值")
    print()

    face_detector = HaarFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    male_features = []
    female_features = []

    print("请先拍摄男性人脸（按 'm' 保存，按 'n' 切换到女性模式）")
    mode = 'male'

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = face_detector.detect(frame)

        for x, y, w, h in faces:
            x1, y1, x2, y2 = x, y, x + w, y + h
            face_roi = frame[y1:y2, x1:x2]
            features = calculate_gender_features(face_roi)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'Mode: {mode}', (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Threshold Analysis', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            mode = 'male'
            print("切换到男性模式")
        elif key == ord('n'):
            mode = 'female'
            print("切换到女性模式")
        elif key == ord('s'):
            if faces:
                x, y, w, h = faces[0]
                x1, y1, x2, y2 = x, y, x + w, y + h
                face_roi = frame[y1:y2, x1:x2]
                features = calculate_gender_features(face_roi)

                if mode == 'male':
                    male_features.append(features)
                    print(f"已保存男性样本 #{len(male_features)}")
                else:
                    female_features.append(features)
                    print(f"已保存女性样本 #{len(female_features)}")

    cap.release()
    cv2.destroyAllWindows()

    # 分析统计
    if male_features or female_features:
        print("\n" + "=" * 60)
        print("统计分析结果")
        print("=" * 60)

        if male_features:
            print(f"\n男性样本 ({len(male_features)} 个):")
            analyze_feature_stats(male_features)

        if female_features:
            print(f"\n女性样本 ({len(female_features)} 个):")
            analyze_feature_stats(female_features)


def analyze_feature_stats(features_list):
    """分析特征统计"""
    if not features_list:
        return

    # 获取所有特征名称
    feature_names = set()
    for features in features_list:
        feature_names.update(features.keys())

    for feature_name in sorted(feature_names):
        values = [f.get(feature_name, 0) for f in features_list if feature_name in f]
        if values:
            mean_val = np.mean(values)
            std_val = np.std(values)
            min_val = np.min(values)
            max_val = np.max(values)
            print(f"  {feature_name}:")
            print(f"    平均值: {mean_val:.4f}, 标准差: {std_val:.4f}")
            print(f"    范围: [{min_val:.4f}, {max_val:.4f}]")


def main():
    """主函数"""
    print("\n性别识别特征调试工具")
    print("=" * 60)
    print("选择功能:")
    print("1. 实时特征调试")
    print("2. 阈值分析")
    print("0. 退出")
    print("=" * 60)

    choice = input("请选择 (0-2): ").strip()

    if choice == '1':
        debug_gender_features()
    elif choice == '2':
        analyze_threshold()
    elif choice == '0':
        print("退出")
    else:
        print("无效选择")


if __name__ == '__main__':
    main()

