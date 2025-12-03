# 脚本目录

本目录包含项目的所有工具脚本。

## 脚本列表

### 1. `exporter.py` - 模型导出工具
将PyTorch模型导出为ONNX、NCNN、TensorRT等格式，用于EAIDK-310部署。

**使用方法**：
```bash
# 导出为ONNX
python scripts/exporter.py --model models/yolo11n.pt --format onnx

# 导出为NCNN（用于EAIDK-310）
python scripts/exporter.py --model models/yolo11n.pt --format ncnn

# 导出为TensorRT
python scripts/exporter.py --model models/yolo11n.pt --format tensorrt

# 导出所有格式
python scripts/exporter.py --model models/yolo11n.pt --format all
```

### 2. `check_imports.py` - 依赖检查脚本
检查所有模块导入是否正常，用于验证项目依赖是否正确安装。

**使用方法**：
```bash
python scripts/check_imports.py
```

### 3. `download_haarcascades.py` - Haar级联分类器下载工具
下载OpenCV Haar级联分类器文件到本地。

**使用方法**：
```bash
python scripts/download_haarcascades.py
```

**注意**：程序会自动使用OpenCV内置的级联分类器，所以这一步是可选的。本地文件可以提高加载速度。

### 4. `install.sh` - 安装脚本
自动化安装项目依赖和设置环境。

**使用方法**：
```bash
./scripts/install.sh
```

或在Windows上：
```bash
bash scripts/install.sh
```

### 5. `run_tests.py` - 测试运行脚本
运行项目的单元测试。

**使用方法**：
```bash
python scripts/run_tests.py
```

### 6. `legacy_compat.py` - 兼容性脚本
用于向后兼容的脚本（如果存在）。

## 注意事项

- 所有脚本都假设在项目根目录下运行
- 某些脚本可能需要特定的依赖（如exporter.py需要PyTorch和Ultralytics）
- 脚本路径使用相对路径，确保在项目根目录执行

