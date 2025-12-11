# 项目结构说明

## 目录结构

```
yoloface/
├── src/yoloface/          # 源代码（主要功能代码）
│   ├── detectors/         # 检测器模块
│   │   ├── haar_detector.py
│   │   ├── yolo11_detector.py
│   │   ├── fastestv2_detector.py
│   │   ├── face_tracker.py
│   │   └── gender_classifier.py
│   ├── utils/            # 工具模块
│   │   ├── video.py
│   │   ├── logger.py
│   │   ├── file_utils.py
│   │   └── text_utils.py
│   ├── config/           # 配置管理
│   │   └── config.py
│   ├── gui/              # GUI模块
│   │   └── main_window.py
│   ├── app.py            # 应用入口
│   └── cli.py            # 命令行接口
│
├── tests/                # 单元测试
│   └── test_detectors.py
│
├── scripts/               # 所有脚本和工具
│   ├── check_imports.py  # 依赖检查
│   ├── diagnose.py       # 环境诊断
│   ├── download_gender_model.py  # 模型下载
│   ├── test_gender.py    # 性别测试
│   └── ...              # 其他脚本（包括历史脚本）
│
├── doc/                  # 所有文档
│   ├── INDEX.md         # 文档索引
│   ├── QUICK_START.md   # 快速开始
│   ├── USAGE.md         # 使用说明
│   └── ...              # 其他文档
│
├── models/               # 模型文件
│   ├── yolo11n.pt
│   ├── gender_net/
│   └── age_net/
│
├── haarcascades/         # Haar级联文件
│
├── config.yaml           # 配置文件
├── requirements.txt      # Python依赖
├── setup.py              # 安装脚本
├── pyproject.toml        # 项目配置
├── Makefile              # Make命令
└── README.md             # 主README
```

## 文件分类

### 源代码 (`src/yoloface/`)
所有主要功能代码都在这里，这是项目的核心。

### 脚本 (`scripts/`)
- **主要脚本**：正在使用的工具脚本
- **历史脚本**：旧版本脚本，仅供参考

### 文档 (`doc/`)
所有项目文档，包括：
- 使用指南
- 架构文档
- 功能说明
- 开发文档

### 测试 (`tests/`)
单元测试代码。

### 模型 (`models/`)
预训练模型文件。

## 使用建议

1. **开发新功能**：在 `src/yoloface/` 中添加
2. **查看文档**：从 `doc/INDEX.md` 开始
3. **运行脚本**：使用 `scripts/` 中的工具
4. **运行测试**：使用 `tests/` 中的测试

