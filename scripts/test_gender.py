#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试性别识别功能
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.yoloface.detectors import GenderClassifier, Gender

def test_gender_classifier():
    """测试性别分类器"""
    print("=" * 60)
    print("性别识别功能测试")
    print("=" * 60)
    
    # 初始化分类器
    print("\n1. 初始化性别分类器...")
    try:
        classifier = GenderClassifier()
        print(f"   ✅ 分类器初始化成功")
        print(f"   使用简单分类器: {classifier.use_simple_classifier}")
        print(f"   已启用: {classifier.enabled}")
    except Exception as e:
        print(f"   ❌ 初始化失败: {e}")
        return
    
    # 创建测试图像
    print("\n2. 创建测试图像...")
    test_images = []
    
    # 创建一个模拟的人脸图像（男性特征：较暗、边缘明显）
    male_face = np.random.randint(80, 120, (100, 100, 3), dtype=np.uint8)
    # 添加一些边缘
    cv2.rectangle(male_face, (20, 20), (80, 80), (60, 60, 60), 2)
    test_images.append(("模拟男性人脸", male_face))
    
    # 创建一个模拟的人脸图像（女性特征：较亮、边缘较少）
    female_face = np.random.randint(140, 180, (100, 100, 3), dtype=np.uint8)
    # 添加柔和的边缘
    cv2.circle(female_face, (50, 50), 30, (160, 160, 160), -1)
    test_images.append(("模拟女性人脸", female_face))
    
    print(f"   ✅ 创建了 {len(test_images)} 个测试图像")
    
    # 测试分类
    print("\n3. 测试性别分类...")
    for name, img in test_images:
        try:
            gender, conf = classifier.predict(img)
            print(f"   {name}: {gender.value} (置信度: {conf:.2f})")
            if gender == Gender.UNKNOWN:
                print(f"      ⚠️  返回了未知性别，这可能表示分类器有问题")
        except Exception as e:
            print(f"   {name}: ❌ 分类失败 - {e}")
    
    # 测试边界情况
    print("\n4. 测试边界情况...")
    
    # 空图像
    try:
        empty_img = np.array([])
        gender, conf = classifier.predict(empty_img)
        print(f"   空图像: {gender.value} (置信度: {conf:.2f})")
    except Exception as e:
        print(f"   空图像: 正确处理异常 - {type(e).__name__}")
    
    # 小图像
    try:
        small_img = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)
        gender, conf = classifier.predict(small_img)
        print(f"   小图像(10x10): {gender.value} (置信度: {conf:.2f})")
    except Exception as e:
        print(f"   小图像: 正确处理异常 - {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n提示:")
    print("- 如果所有测试都返回'未知'，说明简单分类器有问题")
    print("- 如果返回'男'或'女'，说明分类器工作正常")
    print("- 简单分类器准确率较低，建议使用预训练模型")

if __name__ == '__main__':
    test_gender_classifier()

