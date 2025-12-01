# 故障排除指南

## 常见问题

### 1. 错误: `Can't open file: 'haarcascades/haarcascade_frontalface_default.xml' in read mode`

这个错误表示程序无法找到Haar级联分类器文件。

#### 解决方案

程序已经升级为自动处理这个问题。它会按以下顺序尝试加载级联分类器：

1. **本地文件** - 如果 `haarcascades/haarcascade_frontalface_default.xml` 存在
2. **项目目录** - 相对于脚本所在目录
3. **当前工作目录** - 相对于程序运行的目录
4. **OpenCV内置** - 使用OpenCV自带的级联分类器（推荐）

#### 如果仍然出现错误

**方案A: 下载本地Haar级联分类器文件**

```bash
python download_haarcascades.py
```

这会将以下文件下载到 `haarcascades/` 目录：
- `haarcascade_frontalface_default.xml` - 正面人脸检测（默认）
- `haarcascade_frontalface_alt.xml` - 正面人脸检测（替代）
- `haarcascade_frontalface_alt2.xml` - 正面人脸检测（替代2）
- `haarcascade_profileface.xml` - 侧面人脸检测

**方案B: 手动下载**

从 [OpenCV GitHub](https://github.com/opencv/opencv/tree/master/data/haarcascades) 下载所需的XML文件，放到 `haarcascades/` 目录。

**方案C: 使用OpenCV内置文件**

程序会自动使用OpenCV内置的级联分类器，无需任何额外操作。

### 2. 程序启动缓慢

如果程序启动时很慢，可能是在尝试加载多个路径。

#### 解决方案

运行下载脚本来获取本地文件：

```bash
python download_haarcascades.py
```

这样程序就能快速找到文件，而不需要尝试多个路径。

### 3. 检测效果不好

如果人脸检测效果不理想，可以尝试以下方法：

#### 调整检测参数

编辑 `config.yaml` 文件中的Haar检测参数：

```yaml
detection:
  haar:
    scale_factor: 1.1      # 图像缩放因子（1.05-1.4）
    min_neighbors: 5       # 最小邻居数（3-6）
    min_size: [30, 30]     # 最小检测尺寸
```

#### 尝试不同的级联分类器

程序支持多种级联分类器：

```python
from cv_test import HaarFaceDetector

# 使用替代级联分类器
detector = HaarFaceDetector('haarcascades/haarcascade_frontalface_alt.xml')
```

#### 切换到其他检测算法

如果Haar检测效果不好，可以尝试YOLO11或Yolo-FastestV2：

```bash
# 在GUI中选择不同的算法
python app_main.py
```

### 4. 导入错误

如果出现导入错误，确保：

1. 已安装所有依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 使用正确的Python版本（3.8+）：
   ```bash
   python --version
   ```

3. 在项目根目录运行程序：
   ```bash
   cd /path/to/yoloface
   python app_main.py
   ```

### 5. 摄像头无法打开

如果程序无法打开摄像头：

1. 检查摄像头是否连接
2. 检查摄像头权限（macOS需要授予权限）
3. 尝试使用其他摄像头索引：

```python
# 在 app_main.py 中修改
self.cap = cv2.VideoCapture(1)  # 尝试第二个摄像头
```

## 日志和调试

### 查看详细日志

程序会输出详细的日志信息，包括：
- 级联分类器加载状态
- 检测性能指标
- 错误信息

### 启用调试模式

编辑 `config.yaml`：

```yaml
logging:
  level: DEBUG
```

## 获取帮助

如果问题仍未解决，请：

1. 检查 `config.yaml` 配置
2. 查看程序输出的错误信息
3. 确保所有依赖都已正确安装
4. 尝试在项目根目录运行程序

## 相关文件

- `cv_test.py` - Haar级联器检测器实现
- `src/yoloface/detectors/haar_detector.py` - 模块化Haar检测器
- `download_haarcascades.py` - 下载级联分类器脚本
- `haarcascades/` - 级联分类器文件目录

