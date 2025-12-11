# 性别识别功能说明

## 概述

系统已集成性别识别功能，可以在检测到人脸后自动识别性别（男/女）。

## 功能特性

- ✅ 支持基于深度学习的性别分类（使用预训练模型）
- ✅ 支持基于特征的简单分类（备用方案，无需模型）
- ✅ 支持Caffe和ONNX模型格式
- ✅ 自动集成到所有人脸检测算法中
- ✅ 可在配置文件中启用/禁用

## 使用方法

### 1. 基本使用

性别识别功能默认已启用，无需额外配置。运行程序后，检测到的人脸会自动显示性别信息：

```
男 0.85  # 表示识别为男性，置信度85%
女 0.92  # 表示识别为女性，置信度92%
```

### 2. 配置选项

在 `config.yaml` 中可以配置性别识别：

```yaml
detection:
  gender:
    enabled: true              # 是否启用性别识别
    model_path: null           # 性别分类模型路径（可选）
    prototxt_path: null       # Caffe模型的prototxt文件路径
    input_size: [227, 227]    # 模型输入尺寸
    mean_values: [104, 117, 123]  # 图像均值
    scale: 1.0                # 图像缩放因子
```

### 3. 使用预训练模型（推荐）

为了获得更好的识别准确率，建议使用预训练的性别分类模型。

#### 方案1：使用Caffe模型

1. **下载模型文件**：
   - 模型文件（.caffemodel）
   - 配置文件（.prototxt）

2. **放置模型文件**：
   ```
   models/
   ├── gender_net.caffemodel
   └── gender_deploy.prototxt
   ```

3. **配置路径**：
   ```yaml
   detection:
     gender:
       model_path: "models/gender_net.caffemodel"
       prototxt_path: "models/gender_deploy.prototxt"
   ```

#### 方案2：使用ONNX模型

1. **下载ONNX模型文件**

2. **放置模型文件**：
   ```
   models/
   └── gender_classifier.onnx
   ```

3. **配置路径**：
   ```yaml
   detection:
     gender:
       model_path: "models/gender_classifier.onnx"
   ```

### 4. 使用简单分类器（默认）

如果没有提供模型文件，系统会自动使用基于特征的简单分类器。这个分类器准确率较低，仅作为演示用途。

## 模型获取

### 快速下载（推荐）

运行下载脚本：
```bash
python3 scripts/download_gender_model.py
```

### 手动下载

#### 方案1：OpenCV官方模型

1. **下载文件**：
   ```bash
   # 创建模型目录
   mkdir -p models
   
   # 下载prototxt文件
   wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/gender_deploy.prototxt -O models/gender_deploy.prototxt
   
   # 下载模型文件（较大，约1-2MB）
   wget https://github.com/opencv/opencv_extra/raw/master/testdata/dnn/gender_net.caffemodel -O models/gender_net.caffemodel
   ```

2. **配置**：
   在 `config.yaml` 中设置：
   ```yaml
   detection:
     gender:
       model_path: "models/gender_net.caffemodel"
       prototxt_path: "models/gender_deploy.prototxt"
   ```

#### 方案2：其他开源模型

1. **GitHub搜索**：
   - 搜索 "gender classification caffe"
   - 搜索 "gender classification onnx"
   - 选择高星项目

2. **推荐项目**：
   - [OpenCV DNN Models](https://github.com/opencv/opencv/tree/master/samples/dnn)
   - [Age and Gender Classification](https://github.com/yu4u/age-gender-estimation)

#### 方案3：自己训练

- 使用自己的数据集训练性别分类模型
- 导出为Caffe或ONNX格式
- 确保输入输出格式匹配

### 模型要求

- **输入尺寸**：通常为 227x227 或 224x224
- **输入格式**：BGR图像，需要归一化
- **输出格式**：2个值（男性概率、女性概率）或1个值（男性概率）

## 代码示例

### 单独使用性别分类器

```python
from yoloface.detectors import GenderClassifier
import cv2

# 初始化分类器
classifier = GenderClassifier(
    model_path="models/gender_net.caffemodel",
    prototxt_path="models/gender_deploy.prototxt"
)

# 读取图像
image = cv2.imread("face.jpg")

# 预测性别
gender, confidence = classifier.predict(image)
print(f"性别: {gender.value}, 置信度: {confidence:.2f}")
```

### 在检测器中自动使用

性别识别已自动集成到所有检测器中，无需额外代码：

```python
from yoloface.detectors import HaarFaceDetector
import cv2

detector = HaarFaceDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    faces = detector.detect(frame)
    # 绘制时会自动进行性别识别
    frame = detector.draw_detections(frame, faces, show_gender=True)
    cv2.imshow("Result", frame)
```

## 性能优化

1. **使用GPU加速**：
   - 如果系统支持CUDA，模型会自动使用GPU加速
   - 否则使用CPU

2. **调整输入尺寸**：
   - 较小的输入尺寸可以提高速度，但可能降低准确率
   - 在 `config.yaml` 中调整 `input_size`

3. **禁用性别识别**：
   - 如果不需要性别识别，可以在配置中禁用：
     ```yaml
     detection:
       gender:
         enabled: false
     ```

## 常见问题

### Q1: 性别识别准确率不高？

**A**: 
- 使用预训练的深度学习模型可以提高准确率
- 确保人脸区域清晰、正面
- 调整模型输入尺寸和预处理参数

### Q2: 如何获取性别分类模型？

**A**: 
- 可以从OpenCV模型库、GitHub等获取
- 或使用自己的数据集训练
- 参考文档中的模型获取部分

### Q3: 可以自定义性别分类逻辑吗？

**A**: 
- 可以修改 `gender_classifier.py` 中的 `_simple_classify` 方法
- 或实现自己的分类器类

### Q4: 性别识别会影响检测速度吗？

**A**: 
- 会有一定影响，但通常很小
- 如果使用GPU加速，影响更小
- 可以在配置中禁用以提高速度

## 技术细节

### 模型输入预处理

1. 提取人脸区域
2. 调整大小到模型输入尺寸
3. 减去均值（如果配置了）
4. 应用缩放因子
5. 转换为blob格式

### 输出解析

- 如果输出是2个值：`[male_prob, female_prob]`
- 如果输出是1个值：假设是男性概率，女性概率 = 1 - 男性概率
- 概率归一化后选择最大值对应的性别

### 简单分类器原理

简单分类器基于以下特征：
- 面部亮度
- 边缘密度
- 启发式规则

**注意**：简单分类器准确率较低，仅作为演示用途。

## 更新日志

- **v1.0.0**: 初始版本，支持性别识别功能
  - 支持Caffe和ONNX模型
  - 集成到所有检测器
  - 提供简单分类器作为备用方案

