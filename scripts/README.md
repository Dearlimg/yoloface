# 脚本目录说明

本目录包含项目的所有脚本和工具。

## 🔧 主要脚本

### 环境检查
- **check_imports.py** - 检查所有模块导入是否正常
- **diagnose.py** - 开发板环境诊断脚本

### 模型和资源
- **download_gender_model.py** - 下载性别分类模型
- **download_haarcascades.py** - 下载Haar级联分类器文件

### 测试脚本
- **test_gender.py** - 测试性别识别功能
- **run_tests.py** - 运行测试套件

### 工具脚本
- **exporter.py** - 模型导出工具（ONNX、NCNN等）
- **legacy_compat.py** - 向后兼容脚本
- **install.sh** - 安装脚本（Linux/Mac）

## 📝 历史脚本（已废弃）

以下脚本保留用于参考，但不再维护：

- **1.py, 2.py** - 临时测试脚本
- **age_detector.py** - 年龄检测器（旧版本）
- **app_main.py** - 旧版应用入口
- **cv_test.py** - OpenCV测试脚本
- **db_manager.py** - 数据库管理（如果使用）
- **debug_gender_features.py** - 性别特征调试
- **demo_workflow.py** - 演示工作流
- **gender_detector.py** - 性别检测器（旧版本）
- **login_ui.py** - 登录UI（如果使用）
- **test_age_and_gender.py** - 年龄和性别测试
- **test_age_detection.py** - 年龄检测测试
- **test_age_display.py** - 年龄显示测试
- **test_db_connection.py** - 数据库连接测试
- **test_gender_detection.py** - 性别检测测试
- **yolo_test.py** - YOLO测试脚本
- **yolo_track.py** - YOLO跟踪脚本

## 🚀 使用说明

### 检查环境
```bash
python3 scripts/check_imports.py
python3 scripts/diagnose.py
```

### 下载模型
```bash
python3 scripts/download_gender_model.py
python3 scripts/download_haarcascades.py
```

### 运行测试
```bash
python3 scripts/test_gender.py
python3 scripts/run_tests.py
```

### 安装依赖
```bash
bash scripts/install.sh
```

## 📌 注意事项

1. 主要功能代码在 `src/yoloface/` 目录
2. 历史脚本仅供参考，不建议直接使用
3. 新功能请添加到 `src/yoloface/` 中，而不是创建新脚本
