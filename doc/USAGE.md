# 使用说明

## 快速开始

### 1. 安装依赖

```bash
# 方法1: 使用安装脚本（推荐）
./scripts/install.sh

# 方法2: 手动安装
pip install -r requirements.txt
```

### 2. 运行主程序

```bash
# 方式1: 作为模块运行（推荐）
python -m yoloface.app

# 方式2: 使用Makefile
make run

# 方式3: 如果已安装包
yoloface
```

主程序会打开一个PyQt5图形界面，你可以：
- 选择不同的检测算法（Haar级联器、YOLO11、Yolo-FastestV2、人脸跟踪）
- 点击"开始检测"按钮开始实时检测
- 查看FPS和检测数量统计
- 查看运行日志

## 模型导出

如果需要将模型部署到EAIDK-310开发板，可以使用导出工具：

```bash
# 导出为ONNX格式
python scripts/exporter.py --model models/yolo11n.pt --format onnx

# 导出为NCNN格式（用于EAIDK-310）
python exporter.py --model models/yolo11n.pt --format ncnn

# 导出所有格式
python exporter.py --model models/yolo11n.pt --format all --imgsz 640
```

## 常见问题

### 1. 摄像头无法打开
- 检查摄像头是否已连接
- 在Linux系统上，可能需要权限：`sudo chmod 666 /dev/video0`
- 尝试更改摄像头索引（在代码中将`cv2.VideoCapture(0)`改为其他数字）

### 2. YOLO11模型下载失败
- 检查网络连接
- 手动下载模型文件到`models/`目录
- 访问 https://github.com/ultralytics/ultralytics 获取模型

### 3. PyQt5界面无法显示
- 确保已安装PyQt5: `pip install PyQt5`
- 在某些Linux系统上可能需要安装额外的依赖：
  ```bash
  sudo apt-get install python3-pyqt5
  ```

### 4. 检测性能较低
- 降低输入图像分辨率
- 使用更轻量的模型（如YOLO11n）
- 使用多进程版本：`yolo_test_multiprocess.py`
- 考虑使用Haar级联器（速度最快但精度较低）

### 5. 在EAIDK-310上部署
- 使用NCNN格式的模型
- 参考EAIDK-310的官方文档进行部署
- 可能需要交叉编译和优化

## 性能优化建议

1. **选择合适的模型**
   - 实时性要求高：使用Haar级联器或Yolo-FastestV2
   - 精度要求高：使用YOLO11

2. **调整检测参数**
   - 降低置信度阈值可以提高召回率
   - 调整输入图像尺寸可以平衡速度和精度

3. **使用多进程**
   - 在多核CPU上使用多进程版本可以提高吞吐量

4. **硬件加速**
   - 如果支持CUDA，YOLO11会自动使用GPU加速
   - EAIDK-310可以使用NCNN进行硬件加速

## 开发说明

### 项目结构
```
yoloface/
├── src/yoloface/app.py      # 应用入口
├── cv_test.py              # Haar级联器测试
├── yolo_test.py            # YOLO11测试
├── yolo_test_multiprocess.py  # YOLO11多进程测试
├── yolo_track.py           # 人脸跟踪测试
├── yolo_fastestv2_test.py  # Yolo-FastestV2测试
├── scripts/                # 脚本目录
│   ├── exporter.py         # 模型导出工具
│   ├── check_imports.py    # 依赖检查
│   └── download_haarcascades.py  # Haar级联分类器下载
├── requirements.txt        # 依赖列表
├── haarcascades/           # Haar级联分类器
├── models/                 # 模型文件
└── yolo_fastestv2/         # Yolo-FastestV2模型
```

### 扩展开发

1. **添加新的检测算法**
   - 创建新的检测器类，实现`detect()`和`draw_detections()`方法
   - 在`src/yoloface/gui/main_window.py`中添加相应的选项

2. **自定义模型训练**
   - 使用Ultralytics YOLO进行自定义训练
   - 参考官方文档：https://docs.ultralytics.com/

3. **添加人脸识别功能**
   - 集成人脸特征提取（如FaceNet）
   - 添加人脸数据库和匹配功能

## 参考资料

- [Ultralytics YOLO文档](https://docs.ultralytics.com/)
- [OpenCV文档](https://docs.opencv.org/)
- [PyQt5文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [EAIDK-310开发文档](https://developer.rock-chips.com/)

