# 项目文件清单

## 核心程序文件

### 主程序
- `app_main.py` - PyQt5图形界面主程序，集成所有检测算法

### 检测模块
- `cv_test.py` - OpenCV Haar级联器人脸检测
- `yolo_test.py` - YOLO11人脸检测
- `yolo_test_multiprocess.py` - YOLO11多进程检测
- `yolo_track.py` - 人脸跟踪功能
- `yolo_fastestv2_test.py` - Yolo-FastestV2轻量级检测

### 工具脚本
- `exporter.py` - 模型导出工具（ONNX、NCNN、TensorRT）
- `check_imports.py` - 依赖检查脚本
- `install.sh` - 安装脚本

## 配置文件

- `requirements.txt` - Python依赖列表
- `.gitignore` - Git忽略文件配置
- `go.mod` - Go模块配置（项目最初是Go项目，保留）

## 文档文件

- `README.md` - 项目主说明文档（根目录）
- `doc/USAGE.md` - 详细使用说明
- `doc/PROJECT_SUMMARY.md` - 项目总结文档
- `doc/FILES.md` - 本文件清单
- `doc/STRUCTURE.md` - 项目结构说明
- `doc/REFACTORING.md` - 重构说明
- `doc/TROUBLESHOOTING.md` - 故障排除指南

## 目录结构

### haarcascades/
- Haar级联分类器文件目录
- `README.md` - 使用说明

### models/
- 模型文件存储目录
- `README.md` - 模型说明

### yolo_fastestv2/
- Yolo-FastestV2模型文件目录

### doc/
- 课程设计相关文档
- `aim.md` - 课程设计要求

## 文件统计

- Python文件: 8个
- 文档文件: 5个
- 配置文件: 3个
- 脚本文件: 2个
- 目录: 3个

## 代码行数统计（估算）

- `app_main.py`: ~300行
- `cv_test.py`: ~100行
- `yolo_test.py`: ~120行
- `yolo_test_multiprocess.py`: ~150行
- `yolo_track.py`: ~200行
- `yolo_fastestv2_test.py`: ~150行
- `exporter.py`: ~120行
- `check_imports.py`: ~80行

**总计**: 约1200+行Python代码

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

## 使用流程

1. **首次使用**
   ```bash
   # 安装依赖
   ./install.sh
   # 或
   pip install -r requirements.txt
   
   # 检查依赖
   python check_imports.py
   ```

2. **运行程序**
   ```bash
   # 主程序
   python app_main.py
   
   # 或单独测试
   python cv_test.py
   python yolo_test.py
   python yolo_track.py
   ```

3. **导出模型（可选）**
   ```bash
   python exporter.py --model models/yolo11n.pt --format ncnn
   ```

## 注意事项

1. **模型文件**
   - YOLO11模型会在首次运行时自动下载
   - Yolo-FastestV2需要手动准备模型文件
   - 模型文件较大，已添加到.gitignore

2. **摄像头**
   - 确保摄像头已连接
   - Linux系统可能需要权限设置

3. **性能**
   - 首次运行YOLO11需要下载模型，可能需要一些时间
   - 建议使用GPU加速（如果可用）

4. **EAIDK-310部署**
   - 使用NCNN格式的模型
   - 参考EAIDK-310官方文档进行部署

## 项目完成度

- ✅ 核心功能: 100%
- ✅ 用户界面: 100%
- ✅ 文档: 100%
- ✅ 工具脚本: 100%

**总体完成度: 100%**

## 参考资源

- 参考项目: https://github.com/ashkorehennessy/MV-Design
- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- OpenCV: https://opencv.org/
- PyQt5: https://www.riverbankcomputing.com/software/pyqt/

