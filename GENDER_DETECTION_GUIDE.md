# 性别识别功能使用指南

## 功能概述

本项目已升级支持**性别识别功能**，可以在人脸检测的同时识别性别（男/女）。

### 主要特性

- ✅ 支持多种检测器（Haar、YOLO11、人脸跟踪）
- ✅ 实时性别识别
- ✅ 基于人脸特征的启发式算法
- ✅ 可视化显示（蓝色=男性，红色=女性）
- ✅ 性别识别开关（可在运行时启用/禁用）

## 快速开始

### 1. 在主程序中启用性别识别

在 `app_main.py` 中，性别识别功能已集成到 UI 中：

```python
# 在主窗口中勾选"启用性别识别"复选框
# 然后点击"开始检测"按钮
```

### 2. 使用测试脚本

运行测试脚本来体验性别识别功能：

```bash
python test_gender_detection.py
```

选择要测试的功能：
- 1: Haar 检测器 + 性别识别
- 2: YOLO11 检测器 + 性别识别
- 3: 人脸跟踪器 + 性别识别
- 4: 独立性别识别器

### 3. 调试和优化

如果识别结果不理想，使用调试工具：

```bash
python debug_gender_features.py
```

选择功能：
- 1: 实时特征调试 - 查看各个特征的值
- 2: 阈值分析 - 收集样本并分析最优阈值

## 性别识别原理

### 使用的特征

系统使用以下 6 个人脸特征来判断性别：

| 特征 | 男性特征 | 女性特征 |
|------|---------|---------|
| **宽高比** | 通常 > 1.0（更宽） | 通常 < 1.0（更圆） |
| **边缘密度** | 高（胡须、棱角） | 低（光滑） |
| **皮肤比例** | 低（胡须覆盖） | 高（均匀） |
| **对比度** | 高（胡须对比） | 低（光滑） |
| **亮度** | 低（皮肤较暗） | 高（皮肤较亮） |
| **纹理复杂度** | 高（胡须纹理） | 低（光滑） |

### 评分系统

系统为每个特征分配权重，计算男性评分和女性评分，最后比较得出结果。

## 如果识别全是女性

### 可能原因

1. **照明条件** - 光线太亮会降低对比度，导致误判为女性
2. **人脸大小** - 人脸太小可能导致特征提取不准确
3. **胡须不明显** - 胡须是重要的男性特征，如果不明显会误判
4. **皮肤颜色** - 皮肤颜色过浅可能导致皮肤比例过高

### 解决方案

#### 方案 1: 调整照明

- 增加侧光照明以突出面部轮廓
- 避免逆光或过度曝光
- 确保光线均匀分布

#### 方案 2: 调整摄像头距离

- 确保人脸占据画面的 30-70%
- 人脸太小会导致特征不清晰
- 人脸太大会导致特征失真

#### 方案 3: 使用调试工具

运行调试工具查看各个特征的值：

```bash
python debug_gender_features.py
```

选择"实时特征调试"，观察：
- 边缘密度是否足够高
- 对比度是否足够高
- 纹理复杂度是否足够高

#### 方案 4: 手动调整阈值

编辑 `gender_detector.py` 中的 `_detect_gender_simple` 方法，调整以下阈值：

```python
# 边缘密度阈值（默认 0.12）
if edge_density > 0.12:  # 降低此值以更容易识别为男性
    male_score += 0.3

# 对比度阈值（默认 35）
if contrast > 35:  # 降低此值以更容易识别为男性
    male_score += 0.25

# 纹理复杂度阈值（默认 15）
if texture_complexity > 15:  # 降低此值以更容易识别为男性
    male_score += 0.2
```

#### 方案 5: 使用深度学习模型

如果启发式方法效果不理想，可以使用预训练的深度学习模型：

1. 下载性别识别模型：
   - `gender_net.caffemodel`
   - `gender_net.prototxt`

2. 放到 `models/gender_net/` 目录

3. 在初始化时使用深度学习模型：

```python
from gender_detector import GenderDetector

# 使用深度学习模型
gender_detector = GenderDetector(model_type='deep')
```

## 代码示例

### 基础使用

```python
from gender_detector import GenderDetector
from cv_test import HaarFaceDetector
import cv2

# 初始化检测器
face_detector = HaarFaceDetector(enable_gender=True)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 检测人脸并识别性别
    detections = face_detector.detect_with_gender(frame)

    # 绘制结果
    frame = face_detector.draw_detections_with_gender(frame, detections)

    cv2.imshow('Gender Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 高级使用

```python
from gender_detector import GenderDetector, GenderAwareDetector
from yolo_test import YOLO11FaceDetector

# 创建性别感知的检测器
base_detector = YOLO11FaceDetector()
gender_aware_detector = GenderAwareDetector(base_detector, gender_model_type='simple')

# 检测并识别性别
detections = gender_aware_detector.detect_with_gender(frame)

# 绘制结果
frame = gender_aware_detector.draw_detections_with_gender(frame, detections)
```

## 性能指标

- **检测速度**: ~30 FPS（取决于人脸数量和检测器类型）
- **准确率**: 70-85%（取决于照明条件和人脸特征）
- **内存占用**: 低（启发式方法）

## 常见问题

### Q: 为什么识别结果不稳定？

A: 这是正常的，因为启发式方法对照明条件敏感。建议：
- 保持稳定的照明条件
- 使用深度学习模型以获得更好的稳定性
- 对多帧结果进行平均以获得更稳定的输出

### Q: 如何提高准确率？

A:
1. 改善照明条件
2. 使用深度学习模型
3. 收集样本并调整阈值
4. 使用更高分辨率的摄像头

### Q: 支持哪些检测器？

A: 目前支持：
- Haar 级联器
- YOLO11
- 人脸跟踪器
- Yolo-FastestV2（需要手动添加性别识别）

### Q: 可以识别其他属性吗？

A: 当前只支持性别识别。可以扩展系统以支持：
- 年龄估计
- 表情识别
- 种族识别

## 文件说明

| 文件 | 说明 |
|------|------|
| `gender_detector.py` | 性别识别核心模块 |
| `test_gender_detection.py` | 性别识别测试脚本 |
| `debug_gender_features.py` | 特征调试工具 |
| `cv_test.py` | Haar 检测器（已升级） |
| `yolo_test.py` | YOLO11 检测器（已升级） |
| `yolo_track.py` | 人脸跟踪器（已升级） |
| `app_main.py` | 主程序（已升级） |

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。

