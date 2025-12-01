# 基于EAIDK-310的人脸识别系统

## 项目简介

本项目是一个基于EAIDK-310开发板的人脸识别系统，实现了三种不同的人脸检测算法：
1. **OpenCV Haar级联器** - 传统机器学习方法
2. **YOLO11** - 最新的YOLO目标检测模型
3. **Yolo-FastestV2** - 轻量级快速检测模型

系统支持实时人脸检测、跟踪和识别，并提供了友好的PyQt5图形界面。

## 功能特性

- ✅ 实时摄像头人脸检测
- ✅ 三种检测算法切换
- ✅ 人脸跟踪功能
- ✅ 检测结果可视化
- ✅ 性能统计和误差分析
- ✅ 友好的GUI界面

## 环境要求

- Python 3.8+
- EAIDK-310开发板（或支持OpenCV的Linux系统）
- 摄像头设备

## 安装依赖

```bash
pip install -r requirements.txt
```

### 下载Haar级联分类器（可选）

如果需要使用本地的Haar级联分类器文件，可以运行以下命令：

```bash
python download_haarcascades.py
```

**注意**: 程序会自动使用OpenCV内置的级联分类器，所以这一步是可选的。本地文件可以提高加载速度。

## 使用方法

### 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或开发模式安装（推荐）
pip install -e .

# 或使用Makefile
make install
```

### 运行主程序

```bash
# 方式1: 作为模块运行（推荐）
python -m yoloface.app

# 方式2: 使用Makefile
make run

# 方式3: 如果已安装包
yoloface

# 方式4: 旧方式（仍然支持）
python app_main.py
```

### 测试不同检测算法

```bash
# 测试OpenCV Haar级联器
python cv_test.py

# 测试YOLO11
python yolo_test.py

# 测试YOLO11多进程版本
python yolo_test_multiprocess.py

# 测试人脸跟踪
python yolo_track.py

# 测试Yolo-FastestV2
python yolo_fastestv2_test.py
```

## 项目结构

项目采用工程化的模块结构，详见 [STRUCTURE.md](doc/STRUCTURE.md)

```
yoloface/
├── src/yoloface/           # 源代码包
│   ├── detectors/         # 检测器模块
│   ├── utils/             # 工具模块
│   ├── config/            # 配置管理
│   ├── gui/               # GUI模块
│   └── app.py             # 应用入口
├── tests/                  # 测试目录
├── scripts/                # 脚本目录
├── data/                   # 数据目录
│   ├── models/            # 模型文件
│   └── haarcascades/      # Haar级联分类器
├── doc/                    # 文档目录
│   ├── USAGE.md          # 使用说明
│   ├── STRUCTURE.md       # 项目结构
│   ├── PROJECT_SUMMARY.md # 项目总结
│   └── ...                # 其他文档
├── config.yaml            # 配置文件
├── requirements.txt       # Python依赖
├── setup.py               # 安装脚本
└── Makefile               # Make命令
```

**注意**: 项目已重构为更工程化的结构。旧脚本仍然可用，但推荐使用新的模块化结构。

## 算法说明

### 1. OpenCV Haar级联器
- 基于Haar特征的级联分类器
- 速度快，资源占用少
- 适合实时检测场景

### 2. YOLO11
- 最新的YOLO目标检测模型
- 检测精度高
- 支持多种输入尺寸

### 3. Yolo-FastestV2
- 轻量级快速检测模型
- 适合嵌入式设备
- 平衡精度和速度

## 文档

更多详细文档请查看 `doc/` 目录：

- [使用说明](doc/USAGE.md) - 详细的使用指南和常见问题
- [项目结构](doc/STRUCTURE.md) - 项目结构详细说明
- [项目总结](doc/PROJECT_SUMMARY.md) - 项目完成情况总结
- [重构说明](doc/REFACTORING.md) - 项目重构和改进说明
- [文件清单](doc/FILES.md) - 项目文件清单

## 开发说明

本项目为机器视觉课程设计项目，参考了 [MV-Design](https://github.com/ashkorehennessy/MV-Design) 项目的实现思路。

## 许可证

本项目仅用于学习和研究目的。

