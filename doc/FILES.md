# 项目文件清单

## 核心程序文件

### 主程序
- `src/yoloface/app.py` - 应用入口，PyQt5图形界面主程序

### 检测模块（src/yoloface/detectors/）
- `haar_detector.py` - OpenCV Haar级联器人脸检测
- `yolo11_detector.py` - YOLO11人脸检测
- `fastestv2_detector.py` - Yolo-FastestV2轻量级检测
- `face_tracker.py` - 人脸跟踪功能

### GUI模块（src/yoloface/gui/）
- `main_window.py` - PyQt5主窗口实现

### 工具模块（src/yoloface/utils/）
- `logger.py` - 日志工具
- `video.py` - 视频处理工具
- `file_utils.py` - 文件工具

### 配置模块（src/yoloface/config/）
- `config.py` - 配置管理

### 工具脚本（scripts/）
- `exporter.py` - 模型导出工具（ONNX、NCNN、TensorRT）
- `check_imports.py` - 依赖检查脚本
- `download_haarcascades.py` - Haar级联分类器下载工具
- `install.sh` - 安装脚本
- `run_tests.py` - 测试运行脚本
- `legacy_compat.py` - 兼容性脚本

## 配置文件

- `config.yaml` - 项目配置文件
- `requirements.txt` - Python依赖列表
- `setup.py` - 安装脚本
- `pyproject.toml` - 项目元数据
- `Makefile` - Make命令
- `.gitignore` - Git忽略文件配置

## 文档文件

- `README.md` - 项目主说明文档（根目录）
- `doc/USAGE.md` - 详细使用说明
- `doc/PROJECT_SUMMARY.md` - 项目总结文档
- `doc/FILES.md` - 本文件清单
- `doc/STRUCTURE.md` - 项目结构说明
- `doc/ARCHITECTURE.md` - 系统架构图
- `doc/APP_CALL_LOGIC.md` - 调用逻辑说明
- `doc/PROJECT_FLOW_EXPLANATION.md` - 项目流程说明
- `doc/TEAM_DIVISION.md` - 成员分工
- `doc/TROUBLESHOOTING.md` - 故障排除指南
- `doc/REFACTORING.md` - 重构说明

## 目录结构

### src/yoloface/
- 源代码主包
- 包含所有核心功能模块

### tests/
- 单元测试目录
- `test_detectors.py` - 检测器测试

### scripts/
- 工具脚本目录
- `run_tests.py` - 测试运行脚本
- `legacy_compat.py` - 兼容性脚本

### haarcascades/
- Haar级联分类器文件目录
- `README.md` - 使用说明

### models/
- 模型文件存储目录
- `README.md` - 模型说明

### doc/
- 项目文档目录
- 包含所有Markdown文档和课程设计文档

## 文件统计

- Python源代码文件: 15+个
- 文档文件: 15+个
- 配置文件: 6个
- 脚本文件: 4个

## 代码行数统计（估算）

- `app.py`: ~60行
- `main_window.py`: ~320行
- `haar_detector.py`: ~125行
- `yolo11_detector.py`: ~120行
- `fastestv2_detector.py`: ~140行
- `face_tracker.py`: ~240行
- `config.py`: ~190行
- `logger.py`: ~80行
- `video.py`: ~150行
- `file_utils.py`: ~100行
- `exporter.py`: ~130行

**总计**: 约1500+行Python代码

## 功能模块

### ✅ 已实现功能

1. **检测算法**
   - [x] Haar级联器检测
   - [x] YOLO11检测
   - [x] Yolo-FastestV2检测
   - [x] 人脸跟踪

2. **用户界面**
   - [x] PyQt5图形界面
   - [x] 实时视频显示
   - [x] 算法切换
   - [x] 性能统计
   - [x] 运行日志

3. **工具功能**
   - [x] 模型导出
   - [x] 依赖检查
   - [x] 安装脚本

4. **文档**
   - [x] 项目说明
   - [x] 使用指南
   - [x] 项目总结

## 运行方式

### 主程序
```bash
python -m yoloface.app
```

### 测试
```bash
python -m pytest tests/
```

### 模型导出
```bash
python exporter.py --model models/yolo11n.pt --format onnx
```

## 注意事项

1. **模型文件**
   - YOLO11模型会在首次运行时自动下载
   - Yolo-FastestV2需要手动准备ONNX模型文件
   - 模型文件较大，已添加到.gitignore

2. **配置文件**
   - 所有配置在 `config.yaml` 中管理
   - 可以修改配置来调整系统行为

3. **文档**
   - 所有文档集中在 `doc/` 目录
   - 根目录的 `README.md` 提供快速入门
