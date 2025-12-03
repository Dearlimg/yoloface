# 系统架构图

## 项目信息

**项目名称**: 基于EAIDK-310的人脸识别系统设计与实现  
**学院**: 人工智能学院、自动化学院  
**班级**: 智能2304  
**组长**: 高佳愿（23063122）  
**小组成员**: 张旭阳（23063120）、田雨稼（23063130）  
**时间**: 2025年12月1日-2025年12月12日

## 整体架构

```mermaid
graph TB
    subgraph "硬件层 Hardware Layer"
        EAIDK[EAIDK-310开发板<br/>ARM嵌入式平台]
        CAM[USB高清摄像头<br/>图像采集]
        LCD[LCD显示屏<br/>结果展示]
        POWER[5V电源适配器<br/>供电系统]
    end
    
    subgraph "应用层 Application Layer"
        GUI[GUI界面 MainWindow<br/>PyQt5]
        APP[应用入口 app.py]
    end
    
    subgraph "业务逻辑层 Business Logic Layer"
        VT[视频处理线程<br/>VideoThread]
        subgraph "人脸检测模块 Face Detection"
            MTCNN[MTCNN检测器<br/>多任务级联卷积网络]
            PNET[P-Net<br/>候选框生成]
            RNET[R-Net<br/>边界框回归]
            ONET[O-Net<br/>人脸关键点]
        end
        subgraph "预处理模块 Preprocessing"
            PREPROC[人脸预处理<br/>Preprocessor]
            GRAY[灰度归一化<br/>Gray Normalization]
            HIST[直方图均衡化<br/>Histogram Equalization]
            ALIGN[人脸对齐<br/>Face Alignment]
        end
        subgraph "特征提取与匹配模块 Recognition"
            FACENET[FaceNet模型<br/>特征提取]
            FEATURE[128维特征向量<br/>Feature Vector]
            MATCH[欧氏距离匹配<br/>Euclidean Distance]
            DB[人脸数据库<br/>Face Database]
        end
    end
    
    subgraph "工具层 Utility Layer"
        VIDEO[视频工具 VideoCapture<br/>FPSCounter]
        LOGGER[日志工具 Logger]
        FILE[文件工具 FileUtils]
    end
    
    subgraph "配置层 Configuration Layer"
        CONFIG[配置管理 Config<br/>config.yaml]
    end
    
    subgraph "数据层 Data Layer"
        MTCNN_MODEL[MTCNN预训练模型<br/>P-Net/R-Net/O-Net]
        FACENET_MODEL[FaceNet预训练模型<br/>TensorFlow Lite]
        FACE_DB[人脸特征数据库<br/>Face Database]
    end
    
    CAM -->|视频流| VIDEO
    EAIDK --> CAM
    EAIDK --> LCD
    POWER --> EAIDK
    
    APP --> GUI
    GUI --> VT
    VT --> MTCNN
    MTCNN --> PNET
    PNET --> RNET
    RNET --> ONET
    ONET --> PREPROC
    PREPROC --> GRAY
    PREPROC --> HIST
    PREPROC --> ALIGN
    ALIGN --> FACENET
    FACENET --> FEATURE
    FEATURE --> MATCH
    MATCH --> DB
    MATCH --> LCD
    VT --> VIDEO
    MTCNN --> MTCNN_MODEL
    FACENET --> FACENET_MODEL
    DB --> FACE_DB
    VT --> LOGGER
    APP --> CONFIG
    GUI --> CONFIG
    VT --> CONFIG
    MTCNN --> CONFIG
    PREPROC --> CONFIG
    FACENET --> CONFIG
    VIDEO --> FILE
    LOGGER --> FILE
    
    style EAIDK fill:#e1f5ff
    style CAM fill:#e1f5ff
    style LCD fill:#e1f5ff
    style GUI fill:#fff4e1
    style APP fill:#fff4e1
    style MTCNN fill:#e8f5e9
    style PNET fill:#c8e6c9
    style RNET fill:#c8e6c9
    style ONET fill:#c8e6c9
    style PREPROC fill:#fff9c4
    style FACENET fill:#e8f5e9
    style CONFIG fill:#f3e5f5
    style MTCNN_MODEL fill:#fce4ec
    style FACENET_MODEL fill:#fce4ec
    style FACE_DB fill:#fce4ec
```

## 模块详细架构

### 1. 应用入口层

```mermaid
graph LR
    APP[app.py<br/>应用入口] -->|加载配置| CONFIG[Config]
    APP -->|初始化日志| LOGGER[Logger]
    APP -->|创建应用| QAPP[QApplication]
    QAPP -->|创建窗口| GUI[MainWindow]
    
    style APP fill:#fff4e1
    style CONFIG fill:#f3e5f5
    style LOGGER fill:#e1f5ff
    style GUI fill:#fff4e1
```

### 2. GUI层架构

```mermaid
graph TB
    MW[MainWindow<br/>主窗口] -->|包含| VL[VideoLabel<br/>视频显示]
    MW -->|包含| CB[ControlButtons<br/>控制按钮]
    MW -->|包含| CP[ControlPanel<br/>控制面板]
    
    CP -->|算法选择| AC[AlgorithmCombo<br/>算法下拉框]
    CP -->|统计信息| SI[StatsInfo<br/>FPS/检测数量]
    CP -->|运行日志| LT[LogText<br/>日志显示]
    
    MW -->|创建| VT[VideoThread<br/>视频处理线程]
    VT -->|信号| MW
    
    style MW fill:#fff4e1
    style VT fill:#e8f5e9
```

### 3. 检测器模块架构

```mermaid
graph TB
    subgraph "检测器接口"
        BASE[基础检测接口<br/>detect/draw_detections]
    end
    
    subgraph "具体实现"
        HAAR[HaarFaceDetector<br/>OpenCV Haar级联]
        YOLO11[YOLO11FaceDetector<br/>Ultralytics YOLO11]
        FASTEST[YoloFastestV2Detector<br/>ONNX Runtime]
        TRACKER[FaceTracker<br/>基于YOLO11的跟踪]
    end
    
    HAAR -->|实现| BASE
    YOLO11 -->|实现| BASE
    FASTEST -->|实现| BASE
    TRACKER -->|使用| YOLO11
    
    HAAR -->|使用| CV[OpenCV]
    YOLO11 -->|使用| UL[Ultralytics]
    FASTEST -->|使用| ONNX[ONNX Runtime]
    
    style BASE fill:#e8f5e9
    style HAAR fill:#c8e6c9
    style YOLO11 fill:#c8e6c9
    style FASTEST fill:#c8e6c9
    style TRACKER fill:#c8e6c9
```

### 4. 数据流架构

```mermaid
sequenceDiagram
    participant CAM as 摄像头
    participant VT as VideoThread
    participant DET as Detector
    participant GUI as MainWindow
    participant LOG as Logger
    
    CAM->>VT: 读取视频帧
    VT->>DET: 检测人脸
    DET->>DET: 处理图像
    DET->>VT: 返回检测结果
    VT->>VT: 绘制检测框
    VT->>VT: 计算FPS
    VT->>GUI: 发送帧信号(frame_ready)
    GUI->>GUI: 更新显示
    VT->>LOG: 记录日志
```

## 技术栈

### 前端/界面
- **PyQt5**: GUI框架
- **QThread**: 多线程处理
- **OpenCV**: 图像处理和显示

### 检测算法
- **OpenCV Haar Cascade**: 传统机器学习方法
- **YOLO11 (Ultralytics)**: 深度学习目标检测
- **Yolo-FastestV2 (ONNX)**: 轻量级快速检测
- **Face Tracking**: 基于YOLO11的人脸跟踪

### 工具库
- **OpenCV (cv2)**: 计算机视觉库
- **NumPy**: 数值计算
- **PyYAML**: 配置文件解析
- **logging**: 日志系统

### 硬件平台
- **EAIDK-310**: ARM开发板
- **USB摄像头**: 视频输入设备

## 目录结构映射

```
yoloface/
├── src/yoloface/
│   ├── app.py                    → 应用入口层
│   ├── gui/
│   │   └── main_window.py        → GUI层
│   ├── detectors/                → 业务逻辑层
│   │   ├── haar_detector.py
│   │   ├── yolo11_detector.py
│   │   ├── fastestv2_detector.py
│   │   └── face_tracker.py
│   ├── utils/                    → 工具层
│   │   ├── video.py
│   │   ├── logger.py
│   │   └── file_utils.py
│   └── config/                   → 配置层
│       └── config.py
├── models/                       → 数据层
│   └── yolo11n.pt
├── haarcascades/                 → 数据层
│   └── *.xml
└── config.yaml                   → 配置层
```

## 关键设计模式

### 1. 策略模式 (Strategy Pattern)
- **应用**: 多种检测算法的切换
- **实现**: 通过 `change_detector()` 方法动态切换检测器

### 2. 观察者模式 (Observer Pattern)
- **应用**: GUI更新视频帧
- **实现**: PyQt5的信号槽机制 (`frame_ready` 信号)

### 3. 单例模式 (Singleton Pattern)
- **应用**: 配置管理
- **实现**: `load_config()` 函数返回全局唯一配置实例

### 4. 工厂模式 (Factory Pattern)
- **应用**: 检测器创建
- **实现**: `init_detector()` 方法根据类型创建对应检测器

## 性能优化

1. **多线程处理**: 视频处理在独立线程中运行，避免阻塞GUI
2. **FPS控制**: 通过 `msleep(33)` 控制帧率约30 FPS
3. **资源管理**: 使用上下文管理器 (`with` 语句) 管理摄像头资源
4. **配置缓存**: 配置单例模式避免重复加载

## 扩展性

### 添加新检测器
1. 在 `detectors/` 目录创建新检测器类
2. 实现 `detect()` 和 `draw_detections()` 方法
3. 在 `detectors/__init__.py` 中导出
4. 在GUI中添加选项

### 添加新功能
1. 在 `utils/` 目录添加工具函数
2. 在相应模块中导入使用
3. 更新配置文件（如需要）

## 系统特性

- ✅ **模块化设计**: 各模块职责清晰，易于维护
- ✅ **配置驱动**: 通过YAML配置文件管理所有参数
- ✅ **日志系统**: 完整的日志记录和输出
- ✅ **多算法支持**: 支持三种检测算法和跟踪功能
- ✅ **实时处理**: 多线程架构保证实时性能
- ✅ **用户友好**: 直观的GUI界面和操作体验

