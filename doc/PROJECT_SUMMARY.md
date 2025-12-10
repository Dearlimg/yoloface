# 项目总结

## 项目概述

本项目是一个基于EAIDK-310开发板的人脸识别系统，实现了多种人脸检测算法，并提供了友好的图形界面。

## 实现的功能

### ✅ 已完成功能

1. **多种检测算法**
   - ✅ OpenCV Haar级联器（传统机器学习方法）
   - ✅ YOLO11（最新的YOLO目标检测模型）
   - ✅ Yolo-FastestV2（轻量级快速检测模型）
   - ✅ 人脸跟踪功能（基于IoU匹配）

2. **图形界面**
   - ✅ PyQt5主界面
   - ✅ 实时视频显示
   - ✅ 算法切换功能
   - ✅ 性能统计（FPS、检测数量）
   - ✅ 运行日志

3. **测试模块**
   - ✅ Haar级联器独立测试
   - ✅ YOLO11独立测试
   - ✅ YOLO11多进程测试
   - ✅ 人脸跟踪测试
   - ✅ Yolo-FastestV2测试

4. **工具和文档**
   - ✅ 模型导出工具（ONNX、NCNN、TensorRT）
   - ✅ 安装脚本
   - ✅ 使用说明文档
   - ✅ README文档

## 项目结构

```
yoloface/
├── src/yoloface/                  # 源代码包
│   ├── app.py                     # 应用入口
│   ├── detectors/                 # 检测器模块
│   ├── utils/                     # 工具模块
│   ├── config/                    # 配置管理
│   └── gui/                       # GUI模块
├── tests/                         # 测试目录
├── doc/                           # 文档目录
│   ├── USAGE.md                   # 使用说明
│   ├── PROJECT_SUMMARY.md        # 项目总结（本文件）
│   ├── STRUCTURE.md               # 项目结构
│   └── ...                        # 其他文档
├── scripts/                       # 脚本目录
│   ├── exporter.py                # 模型导出工具
│   ├── check_imports.py           # 依赖检查
│   ├── download_haarcascades.py   # Haar级联分类器下载
│   └── install.sh                 # 安装脚本
├── requirements.txt               # Python依赖
├── config.yaml                    # 配置文件
├── setup.py                       # 安装脚本
├── Makefile                       # Make命令
├── models/                        # 模型文件目录
│   └── README.md
└── haarcascades/                  # Haar级联分类器目录
    └── README.md
```

## 技术栈

- **编程语言**: Python 3.8+
- **计算机视觉**: OpenCV, Ultralytics YOLO
- **GUI框架**: PyQt5
- **深度学习**: PyTorch, YOLO11
- **模型部署**: ONNX, NCNN（用于EAIDK-310）

## 核心模块说明

### 1. Haar级联器检测
- 使用OpenCV的Haar级联分类器
- 速度快，资源占用少
- 适合实时检测场景
- 实现位置：`src/yoloface/detectors/haar_detector.py`

### 2. YOLO11检测
- 使用Ultralytics YOLO11模型
- 检测精度高
- 支持多种输入尺寸
- 自动下载预训练模型
- 实现位置：`src/yoloface/detectors/yolo11_detector.py`

### 3. Yolo-FastestV2检测
- 轻量级快速检测模型
- 适合嵌入式设备
- 需要ONNX格式模型
- 实现位置：`src/yoloface/detectors/fastestv2_detector.py`

### 4. 人脸跟踪
- 基于IoU匹配的跟踪算法
- 为每个目标分配唯一ID
- 显示跟踪轨迹
- 支持多目标跟踪
- 实现位置：`src/yoloface/detectors/face_tracker.py`

### 5. 主程序 (`src/yoloface/app.py`)
- PyQt5图形界面
- 集成所有检测算法
- 实时视频显示
- 性能统计和日志

### 6. 模型导出 (`exporter.py`)
- 支持导出为ONNX格式
- 支持导出为NCNN格式（EAIDK-310）
- 支持导出为TensorRT格式

## 使用流程

1. **安装依赖**
   ```bash
   ./scripts/install.sh
   # 或
   pip install -r requirements.txt
   ```

2. **运行主程序**
   ```bash
   python -m yoloface.app
   ```

3. **选择算法并开始检测**
   - 在GUI中选择检测算法
   - 点击"开始检测"按钮
   - 查看实时检测结果

4. **导出模型（可选）**
   ```bash
   python scripts/exporter.py --model models/yolo11n.pt --format ncnn
   ```

## 课程设计要求对照

根据课程设计要求，本项目实现了以下内容：

### ✅ 设计要求1：硬件和平台
- 支持摄像头图像采集
- 代码可在EAIDK-310平台运行
- 支持多种检测算法

### ✅ 设计要求2：软件算法
- 实现了基于机器学习的人脸检测算法
- 支持YOLO11深度学习模型
- 支持传统Haar级联器
- 支持轻量级Yolo-FastestV2

### ✅ 设计要求3：检测和追踪
- 实现了人脸检测功能
- 实现了人脸跟踪功能
- 支持实时检测和显示
- 可以分析检测结果

### ✅ 设计要求4：GUI界面
- 使用PyQt5创建了友好的图形界面
- 可以实时演示检测结果
- 支持算法切换
- 显示性能统计

### ✅ 设计要求5：报告
- 提供了完整的项目文档
- README、使用说明、项目总结等

## 性能特点

1. **Haar级联器**
   - 速度：最快（>30 FPS）
   - 精度：中等
   - 资源占用：最少

2. **YOLO11**
   - 速度：中等（10-20 FPS，取决于硬件）
   - 精度：最高
   - 资源占用：较高

3. **Yolo-FastestV2**
   - 速度：快（20-30 FPS）
   - 精度：较高
   - 资源占用：中等

4. **人脸跟踪**
   - 速度：取决于底层检测算法
   - 功能：多目标跟踪、轨迹显示

## 后续改进方向

1. **功能扩展**
   - [ ] 添加人脸识别功能（不仅仅是检测）
   - [ ] 添加人脸数据库管理
   - [ ] 添加检测结果保存功能
   - [ ] 添加视频录制功能

2. **性能优化**
   - [ ] 优化模型推理速度
   - [ ] 添加模型量化支持
   - [ ] 优化多进程处理

3. **部署优化**
   - [ ] 完善EAIDK-310部署文档
   - [ ] 添加交叉编译脚本
   - [ ] 优化NCNN模型

4. **用户体验**
   - [ ] 添加配置界面
   - [ ] 添加检测参数调整
   - [ ] 改进界面布局

## 参考资源

- 参考项目: [MV-Design](https://github.com/ashkorehennessy/MV-Design)
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- OpenCV文档: https://docs.opencv.org/
- PyQt5文档: https://www.riverbankcomputing.com/static/Docs/PyQt5/

## 许可证

本项目仅用于学习和研究目的。

## 作者

根据课程设计要求完成

## 日期

2025年

