# 项目结构说明

## 新的工程化项目结构

项目已重构为更工程化的结构，遵循Python项目最佳实践。

```
yoloface/
├── src/                          # 源代码目录
│   └── yoloface/                 # 主包
│       ├── __init__.py          # 包初始化
│       ├── app.py               # 应用入口
│       ├── detectors/            # 检测器模块
│       │   ├── __init__.py
│       │   ├── haar_detector.py
│       │   ├── yolo11_detector.py
│       │   ├── fastestv2_detector.py
│       │   └── face_tracker.py
│       ├── utils/                # 工具模块
│       │   ├── __init__.py
│       │   ├── logger.py        # 日志工具
│       │   ├── video.py         # 视频处理工具
│       │   └── file_utils.py    # 文件工具
│       ├── config/               # 配置模块
│       │   ├── __init__.py
│       │   └── config.py        # 配置管理
│       └── gui/                  # GUI模块
│           ├── __init__.py
│           └── main_window.py    # 主窗口
│
├── tests/                        # 测试目录
│   ├── __init__.py
│   └── test_detectors.py        # 检测器测试
│
├── scripts/                      # 脚本目录
│   ├── run_tests.py             # 测试脚本
│   └── legacy_compat.py         # 兼容性脚本
│
├── data/                         # 数据目录
│   ├── models/                  # 模型文件
│   ├── haarcascades/            # Haar级联分类器
│   └── output/                  # 输出文件
│
├── logs/                         # 日志目录
│
├── config.yaml                   # 配置文件
├── requirements.txt              # Python依赖
├── setup.py                      # 安装脚本
├── pyproject.toml               # 项目元数据
├── Makefile                      # Make命令
├── README.md                     # 项目说明
├── USAGE.md                      # 使用说明
└── STRUCTURE.md                  # 本文件
```

## 主要改进

### 1. 模块化结构
- **detectors/**: 所有检测器独立模块化
- **utils/**: 通用工具函数
- **config/**: 配置管理
- **gui/**: GUI相关代码

### 2. 配置管理
- 使用YAML配置文件
- 统一的配置管理类
- 支持默认配置和自定义配置

### 3. 日志系统
- 统一的日志管理
- 支持文件和控制台输出
- 可配置日志级别

### 4. 包管理
- `setup.py` 和 `pyproject.toml` 支持
- 可以安装为Python包
- 支持开发模式安装

### 5. 测试框架
- pytest测试框架
- 单元测试示例
- 测试脚本

### 6. 工具脚本
- Makefile提供常用命令
- 测试脚本
- 兼容性脚本

## 使用新结构

### 安装为包

```bash
# 开发模式安装
pip install -e .

# 或使用Makefile
make install-dev
```

### 运行主程序

```bash
# 方式1: 作为模块运行
python -m yoloface.app

# 方式2: 使用Makefile
make run

# 方式3: 如果安装了包
yoloface
```

### 使用模块

```python
# 导入检测器
from yoloface.detectors import HaarFaceDetector, YOLO11FaceDetector

# 导入工具
from yoloface.utils import setup_logger, VideoCapture

# 导入配置
from yoloface.config import load_config
```

### 运行测试

```bash
# 方式1: 使用pytest
pytest tests/ -v

# 方式2: 使用Makefile
make test

# 方式3: 使用脚本
python scripts/run_tests.py
```

## 向后兼容

为了保持向后兼容，旧的脚本仍然可以工作：

```python
# 旧的方式（仍然支持）
from cv_test import HaarFaceDetector
from yolo_test import YOLO11FaceDetector

# 新的方式（推荐）
from yoloface.detectors import HaarFaceDetector, YOLO11FaceDetector
```

## 配置文件

配置文件 `config.yaml` 包含所有可配置项：

- 摄像头设置
- 检测算法参数
- GUI设置
- 日志设置
- 性能参数

修改配置文件后，程序会自动加载新配置。

## 开发指南

### 添加新检测器

1. 在 `src/yoloface/detectors/` 创建新文件
2. 实现检测器类（参考现有检测器）
3. 在 `detectors/__init__.py` 中导出
4. 在GUI中添加选项

### 添加新工具函数

1. 在 `src/yoloface/utils/` 创建新文件或添加到现有文件
2. 在 `utils/__init__.py` 中导出
3. 编写测试

### 修改配置

1. 修改 `config.yaml`
2. 或在代码中使用 `Config` 类动态修改

## 最佳实践

1. **使用日志**: 使用 `get_logger()` 而不是 `print()`
2. **使用配置**: 从配置文件读取参数，而不是硬编码
3. **模块化**: 将功能拆分到独立模块
4. **类型提示**: 使用类型提示提高代码可读性
5. **文档字符串**: 为所有公共函数和类添加文档字符串

