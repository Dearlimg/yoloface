# 项目流程图

## 一、整体流程图

```mermaid
flowchart TD
    Start([程序启动]) --> LoadConfig[加载配置文件 config.yaml]
    LoadConfig --> SetupLogger[设置日志系统]
    SetupLogger --> CreateApp[创建QApplication]
    CreateApp --> CreateWindow[创建MainWindow主窗口]
    CreateWindow --> InitUI[初始化UI界面]
    InitUI --> WaitUser[等待用户操作]
    
    WaitUser --> UserAction{用户操作}
    
    UserAction -->|选择算法| SelectAlgo[选择检测算法]
    UserAction -->|点击开始检测| StartDetect[开始检测]
    UserAction -->|点击停止| StopDetect[停止检测]
    UserAction -->|关闭窗口| End([程序结束])
    
    SelectAlgo --> WaitUser
    
    StartDetect --> CreateThread[创建VideoThread线程]
    CreateThread --> InitDetector[初始化检测器]
    InitDetector --> OpenCamera[打开摄像头]
    OpenCamera --> CameraOK{摄像头打开成功?}
    
    CameraOK -->|失败| ShowError[显示错误信息]
    CameraOK -->|成功| VideoLoop[进入视频处理循环]
    
    ShowError --> WaitUser
    
    VideoLoop --> ReadFrame[读取一帧图像]
    ReadFrame --> Preprocess[预处理图像]
    Preprocess --> Detect[调用检测器检测]
    Detect --> PostProcess[后处理检测结果]
    PostProcess --> DrawBox[绘制检测框]
    DrawBox --> CalcFPS[计算FPS]
    CalcFPS --> SendSignal[发送信号给界面]
    SendSignal --> UpdateUI[更新界面显示]
    UpdateUI --> Sleep[休眠33ms]
    Sleep --> CheckRunning{是否继续运行?}
    
    CheckRunning -->|是| VideoLoop
    CheckRunning -->|否| CloseCamera[关闭摄像头]
    
    CloseCamera --> WaitUser
    
    StopDetect --> StopThread[停止视频线程]
    StopThread --> ReleaseCamera[释放摄像头资源]
    ReleaseCamera --> WaitUser
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style VideoLoop fill:#87CEEB
    style Detect fill:#FFD700
```

## 二、检测器初始化流程图

```mermaid
flowchart TD
    Start([初始化检测器]) --> CheckType{检测器类型}
    
    CheckType -->|haar| InitHaar[初始化Haar检测器]
    CheckType -->|yolo11| InitYOLO[初始化YOLO11检测器]
    CheckType -->|fastestv2| InitFastest[初始化FastestV2检测器]
    CheckType -->|track| InitTracker[初始化跟踪器]
    
    InitHaar --> LoadCascade[加载Haar级联分类器]
    LoadCascade --> SetParams[设置检测参数]
    
    InitYOLO --> LoadYOLOModel[加载YOLO11模型]
    LoadYOLOModel --> SetYOLOParams[设置YOLO参数]
    
    InitFastest --> LoadONNX[加载ONNX模型]
    LoadONNX --> SetFastestParams[设置FastestV2参数]
    
    InitTracker --> LoadTrackerModel[加载YOLO11模型用于跟踪]
    LoadTrackerModel --> InitTrackingData[初始化跟踪数据]
    
    SetParams --> Success([初始化成功])
    SetYOLOParams --> Success
    SetFastestParams --> Success
    InitTrackingData --> Success
    
    LoadCascade -->|失败| Error([初始化失败])
    LoadYOLOModel -->|失败| Error
    LoadONNX -->|失败| Error
    
    style Start fill:#90EE90
    style Success fill:#87CEEB
    style Error fill:#FFB6C1
```

## 三、单帧检测流程图

```mermaid
flowchart TD
    Start([开始处理一帧]) --> ReadFrame[从摄像头读取帧]
    ReadFrame --> CheckFrame{读取成功?}
    
    CheckFrame -->|失败| End([结束])
    CheckFrame -->|成功| CheckDetector{检测器类型}
    
    CheckDetector -->|Haar/YOLO11/FastestV2| NormalDetect[普通检测模式]
    CheckDetector -->|Track| TrackDetect[跟踪模式]
    
    NormalDetect --> Preprocess[预处理图像]
    Preprocess --> RunDetector[运行检测器]
    RunDetector --> GetBoxes[获取检测框]
    GetBoxes --> DrawBoxes[绘制检测框]
    
    TrackDetect --> RunTracker[运行跟踪器]
    RunTracker --> MatchTracks[匹配跟踪]
    MatchTracks --> UpdateTracks[更新跟踪数据]
    UpdateTracks --> DrawTracks[绘制跟踪框和轨迹]
    
    DrawBoxes --> AddInfo[添加FPS和统计信息]
    DrawTracks --> AddInfo
    
    AddInfo --> EmitSignal[发送信号给界面]
    EmitSignal --> Sleep[休眠33ms]
    Sleep --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style RunDetector fill:#FFD700
    style RunTracker fill:#FFD700
```

## 四、Haar检测器详细流程

```mermaid
flowchart TD
    Start([Haar检测开始]) --> Gray[转换为灰度图]
    Gray --> Cascade[调用级联分类器]
    Cascade --> MultiScale[多尺度检测]
    MultiScale --> Filter[过滤检测结果]
    Filter --> Return([返回检测框列表])
    
    style Start fill:#90EE90
    style Return fill:#87CEEB
```

## 五、YOLO11检测器详细流程

```mermaid
flowchart TD
    Start([YOLO11检测开始]) --> ModelInput[输入图像到模型]
    ModelInput --> Forward[模型前向传播]
    Forward --> GetResults[获取检测结果]
    GetResults --> ParseBoxes[解析边界框]
    ParseBoxes --> FilterConf[过滤置信度]
    FilterConf --> FilterIOU[NMS去重]
    FilterIOU --> Return([返回检测框列表])
    
    style Start fill:#90EE90
    style Forward fill:#FFD700
    style Return fill:#87CEEB
```

## 六、FastestV2检测器详细流程

```mermaid
flowchart TD
    Start([FastestV2检测开始]) --> CheckModel{模型已加载?}
    CheckModel -->|否| ReturnEmpty[返回空列表]
    CheckModel -->|是| Blob[创建blob]
    
    Blob --> Normalize[归一化到0-1]
    Normalize --> Resize[调整到416x416]
    Resize --> SetInput[设置模型输入]
    SetInput --> Forward[模型前向传播]
    Forward --> GetOutput[获取输出]
    GetOutput --> ParseOutput[解析输出格式]
    ParseOutput --> FilterConf[过滤置信度]
    FilterConf --> ConvertCoord[转换坐标]
    ConvertCoord --> Return([返回检测框列表])
    
    ReturnEmpty --> End([结束])
    Return --> End
    
    style Start fill:#90EE90
    style Forward fill:#FFD700
    style End fill:#87CEEB
```

## 七、人脸跟踪流程图

```mermaid
flowchart TD
    Start([跟踪开始]) --> Detect[检测当前帧人脸]
    Detect --> GetDetections[获取检测结果]
    GetDetections --> CheckHistory{有历史跟踪?}
    
    CheckHistory -->|否| NewTracks[创建新跟踪]
    CheckHistory -->|是| Match[匹配检测和跟踪]
    
    Match --> CalcIOU[计算IoU]
    CalcIOU --> FindBest[找到最佳匹配]
    FindBest --> UpdateTrack[更新跟踪]
    FindBest --> NewTrack[创建新跟踪]
    
    UpdateTrack --> AddHistory[添加到历史]
    NewTracks --> AddHistory
    NewTrack --> AddHistory
    
    AddHistory --> CleanLost[清理丢失的跟踪]
    CleanLost --> Draw[绘制跟踪框和轨迹]
    Draw --> Return([返回跟踪结果])
    
    style Start fill:#90EE90
    style Match fill:#FFD700
    style Return fill:#87CEEB
```

## 八、界面更新流程图

```mermaid
flowchart TD
    Start([收到frame_ready信号]) --> ConvertColor[转换BGR到RGB]
    ConvertColor --> CreateQImage[创建QImage对象]
    CreateQImage --> Scale[缩放图像适应窗口]
    Scale --> SetPixmap[设置到QLabel]
    SetPixmap --> UpdateFPS[更新FPS标签]
    UpdateFPS --> UpdateCount[更新检测数量标签]
    UpdateCount --> End([更新完成])
    
    style Start fill:#90EE90
    style End fill:#87CEEB
```

## 九、完整系统流程图（简化版）

```mermaid
flowchart LR
    A[程序启动] --> B[加载配置]
    B --> C[创建GUI]
    C --> D[用户选择算法]
    D --> E[点击开始检测]
    E --> F[打开摄像头]
    F --> G[循环处理]
    G --> H[读取帧]
    H --> I[检测人脸]
    I --> J[绘制结果]
    J --> K[更新界面]
    K --> L{继续?}
    L -->|是| G
    L -->|否| M[停止检测]
    M --> N[关闭摄像头]
    N --> D
    
    style A fill:#90EE90
    style I fill:#FFD700
    style M fill:#FFB6C1
```

## 十、数据流图

```mermaid
flowchart LR
    Camera[摄像头] -->|视频流| VideoThread[VideoThread线程]
    VideoThread -->|调用| Detector[检测器]
    Detector -->|返回| Detections[检测结果]
    Detections -->|绘制| Frame[处理后的帧]
    Frame -->|信号| MainWindow[主窗口]
    MainWindow -->|显示| Screen[屏幕]
    
    Config[配置文件] -->|参数| Detector
    Config -->|参数| VideoThread
    
    style Camera fill:#87CEEB
    style Detector fill:#FFD700
    style Screen fill:#90EE90
```

## 流程图说明

### 关键节点说明

1. **程序启动**：`app.py` 的 `main()` 函数
2. **配置加载**：从 `config.yaml` 读取配置
3. **检测器初始化**：根据选择的算法创建对应的检测器
4. **视频循环**：核心处理循环，每秒处理约30帧
5. **检测执行**：调用检测器进行人脸检测
6. **界面更新**：通过信号槽机制更新GUI

### 关键决策点

- **检测器类型选择**：决定使用哪种算法
- **摄像头状态**：检查摄像头是否成功打开
- **运行状态**：决定是否继续处理视频帧
- **匹配跟踪**：跟踪模式下的IoU匹配

### 性能优化点

- **多线程**：视频处理在独立线程，不阻塞GUI
- **FPS控制**：每帧休眠33ms，控制处理速度
- **信号槽机制**：异步更新界面，提高响应性

## 使用说明

这些流程图展示了项目从启动到检测的完整过程，包括：

1. **整体流程**：程序启动到结束的完整流程
2. **检测器初始化**：不同检测器的初始化过程
3. **单帧处理**：每一帧图像的处理流程
4. **各检测器详细流程**：Haar、YOLO11、FastestV2的具体实现
5. **跟踪流程**：人脸跟踪的完整过程
6. **界面更新**：GUI更新的流程
7. **数据流**：数据在系统中的流动

可以通过这些流程图快速理解项目的整体架构和执行逻辑。

