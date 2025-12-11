# 基于EAIDK-310的人脸识别系统

## 项目简介

西安邮电大学智能科学与技术专业大三机器视觉课程设计
本项目是一个基于EAIDK-310开发板的人脸识别系统，实现了多种人脸检测算法，并提供了友好的PyQt5图形界面。

## 功能特性

- ✅ 实时摄像头人脸检测
- ✅ 多种检测算法切换（Haar、YOLO11、Yolo-FastestV2）
- ✅ **性别识别功能**（男/女识别，支持预训练模型）
- ✅ 人脸跟踪功能
- ✅ 检测结果可视化
- ✅ 性能统计和误差分析
- ✅ 友好的GUI界面

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

```bash
# 方式1: 作为模块运行（推荐）
python -m yoloface.app

# 方式2: 使用Makefile
make run

# 方式3: 如果已安装包
yoloface
```

## 项目结构

```
yoloface/
├── src/yoloface/      # 源代码包
│   ├── detectors/    # 检测器模块
│   ├── utils/        # 工具模块
│   ├── config/       # 配置管理
│   ├── gui/          # GUI模块
│   └── app.py        # 应用入口
├── tests/            # 测试目录
├── scripts/          # 脚本目录
├── doc/              # 文档目录
├── config.yaml       # 配置文件
└── requirements.txt  # Python依赖
```

## 文档

详细文档请查看 `doc/` 目录，完整索引见 [文档索引](doc/INDEX.md)：

### 快速开始
- [快速开始](doc/QUICK_START.md) - 快速上手指南
- [安装说明](doc/SETUP_INSTRUCTIONS.md) - 详细安装步骤
- [使用说明](doc/USAGE.md) - 详细的使用指南

### 功能文档
- [性别识别](doc/GENDER_RECOGNITION.md) - 性别识别功能说明
- [准确率提升](doc/GENDER_ACCURACY_IMPROVEMENT.md) - 如何提高性别识别准确率
- [GUI环境配置](doc/GUI_SETUP.md) - 开发板GUI环境配置
- [设备兼容性](doc/DEVICE_COMPATIBILITY.md) - 开发板问题排查

### 架构文档
- [系统架构](doc/ARCHITECTURE.md) - 系统架构图
- [项目结构](doc/STRUCTURE.md) - 项目结构说明
- [流程图](doc/FLOWCHART.md) - 系统流程图

### 更多文档
- [文档索引](doc/INDEX.md) - 完整文档索引
- [项目总结](doc/PROJECT_SUMMARY.md) - 项目完成情况

## 开发说明

本项目为机器视觉课程设计项目。

## 许可证

本项目仅用于学习和研究目的。
