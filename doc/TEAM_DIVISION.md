# 项目成员分工详情

## 项目信息
- **项目名称**: 基于EAIDK-310的人脸识别系统设计与实现
- **班级**: 智能2304
- **时间**: 2025年12月1日-2025年12月12日

## 成员分工

### 高佳愿（组长，23063122）
**职责**：
- 统筹项目进度，协调团队成员工作
- 负责系统架构设计与模块化组织
- 负责YOLO11模型部署及整体功能调试
- 负责项目配置管理（config.yaml）和日志系统设计
- 负责主程序入口（app.py）和应用集成
- 负责模型导出工具（exporter.py）开发，支持ONNX、NCNN、TensorRT格式

**主要贡献**：
- 设计并实现了模块化的项目架构（detectors、utils、config、gui）
- 实现了YOLO11检测器（yolo11_detector.py）
- 实现了系统配置管理模块（config/config.py）
- 实现了日志系统（utils/logger.py）
- 实现了模型导出工具，支持多种部署格式

---

### 张旭阳（组员，23063120）
**职责**：
- 负责Haar级联分类器人脸检测算法实现
- 负责Yolo-FastestV2轻量级检测算法实现
- 负责USB摄像头图像采集模块开发
- 负责视频处理工具模块开发（FPS计算、图像绘制等）

**主要贡献**：
- 实现了Haar级联分类器检测器（haar_detector.py）
- 实现了Yolo-FastestV2检测器（fastestv2_detector.py）
- 实现了视频捕获封装类（utils/video.py - VideoCapture）
- 实现了FPS计数器（utils/video.py - FPSCounter）
- 实现了图像信息绘制功能（utils/video.py - draw_info）

---

### 田雨稼（组员，23063130）
**职责**：
- 负责人脸跟踪算法开发（基于IoU匹配的多目标跟踪）
- 负责PyQt5 GUI界面设计及结果展示模块开发
- 负责测试用例编写及功能测试

**主要贡献**：
- 实现了人脸跟踪器（face_tracker.py），包括IoU计算、跟踪匹配、轨迹可视化
- 实现了PyQt5主窗口界面（gui/main_window.py）
- 实现了视频处理线程（VideoThread），支持多线程视频处理
- 实现了GUI结果展示功能（视频显示、统计信息、运行日志）
- 编写了检测器测试用例（tests/test_detectors.py）

---

## 技术实现对应关系

### 检测算法模块（src/yoloface/detectors/）
| 算法 | 实现文件 | 负责人 |
|------|---------|--------|
| Haar级联分类器 | haar_detector.py | 张旭阳 |
| YOLO11 | yolo11_detector.py | 高佳愿 |
| Yolo-FastestV2 | fastestv2_detector.py | 张旭阳 |
| 人脸跟踪 | face_tracker.py | 田雨稼 |

### 工具模块（src/yoloface/utils/）
| 模块 | 实现文件 | 负责人 |
|------|---------|--------|
| 视频捕获 | video.py (VideoCapture) | 张旭阳 |
| FPS计算 | video.py (FPSCounter) | 张旭阳 |
| 日志系统 | logger.py | 高佳愿 |
| 文件工具 | file_utils.py | 高佳愿 |

### GUI模块（src/yoloface/gui/）
| 模块 | 实现文件 | 负责人 |
|------|---------|--------|
| 主窗口界面 | main_window.py | 田雨稼 |
| 视频处理线程 | main_window.py (VideoThread) | 田雨稼 |

### 配置与架构
| 模块 | 实现文件 | 负责人 |
|------|---------|--------|
| 配置管理 | config/config.py | 高佳愿 |
| 应用入口 | app.py | 高佳愿 |
| 模型导出 | exporter.py | 高佳愿 |

### 测试模块
| 模块 | 实现文件 | 负责人 |
|------|---------|--------|
| 检测器测试 | tests/test_detectors.py | 田雨稼 |

---

## 项目文件对应关系

### 核心检测算法
- `src/yoloface/detectors/haar_detector.py` - 张旭阳
- `src/yoloface/detectors/yolo11_detector.py` - 高佳愿
- `src/yoloface/detectors/fastestv2_detector.py` - 张旭阳
- `src/yoloface/detectors/face_tracker.py` - 田雨稼

### 工具模块
- `src/yoloface/utils/video.py` - 张旭阳
- `src/yoloface/utils/logger.py` - 高佳愿
- `src/yoloface/utils/file_utils.py` - 高佳愿

### GUI界面
- `src/yoloface/gui/main_window.py` - 田雨稼

### 配置与入口
- `src/yoloface/config/config.py` - 高佳愿
- `src/yoloface/app.py` - 高佳愿
- `config.yaml` - 高佳愿

### 工具脚本
- `exporter.py` - 高佳愿（模型导出）

### 测试文件
- `tests/test_detectors.py` - 田雨稼

---

## 分工合理性说明

本分工方案基于项目实际代码实现，确保：
1. **职责清晰**：每个成员负责的模块明确，避免重复工作
2. **技术匹配**：分工与成员技术能力匹配
3. **进度可控**：模块化设计便于并行开发
4. **易于集成**：统一的接口设计便于模块集成

---

## 备注

- 本项目实际实现了**Haar级联分类器**、**YOLO11**、**Yolo-FastestV2**和**人脸跟踪**四种算法
- GUI界面使用**PyQt5**实现，支持实时视频显示、算法切换、性能统计等功能
- 视频采集使用**OpenCV VideoCapture**，支持USB摄像头
- 测试用例使用**pytest**框架编写

