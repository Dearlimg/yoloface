# 开发板兼容性问题排查指南

## 概述

本文档列出了在EAIDK-310开发板（Python 3.6.3）上运行代码可能遇到的问题及解决方案。

## 潜在问题列表

### 1. Python 3.6.3 语法兼容性问题

#### 1.1 Path.read_text() 兼容性
**问题**: `setup.py` 中使用了 `Path.read_text()`，需要确认 Python 3.6.3 支持。

**解决方案**: 已使用兼容方式，如果出现问题，可以回退到 `open().read()`

#### 1.2 f-string 支持
**状态**: ✅ Python 3.6+ 支持 f-string，无需修改

#### 1.3 类型注解
**状态**: ✅ Python 3.6 支持类型注解，无需修改

### 2. 依赖库版本兼容性

#### 2.1 ultralytics 版本问题
**潜在问题**: ultralytics 8.0+ 可能不支持 Python 3.6.3

**检查方法**:
```bash
python3 -c "import ultralytics; print(ultralytics.__version__)"
```

**解决方案**:
- 如果 ultralytics 8.0+ 不支持 Python 3.6.3，需要降级到支持 3.6 的版本
- 或者使用 ultralytics 的早期版本（如 7.x）

#### 2.2 torch 版本问题
**状态**: ✅ torch 1.10.0+ 支持 Python 3.6.3

**检查方法**:
```bash
python3 -c "import torch; print(torch.__version__)"
```

#### 2.3 numpy 版本问题
**状态**: ✅ 已限制为 `>=1.14.5,<1.20.0`，兼容 Python 3.6.3

**检查方法**:
```bash
python3 -c "import numpy; print(numpy.__version__)"
```

#### 2.4 PyQt5 版本问题
**潜在问题**: PyQt5 5.15.0+ 在 Python 3.6.3 上可能有问题

**检查方法**:
```bash
python3 -c "from PyQt5.QtWidgets import QApplication; print('OK')"
```

**解决方案**: 如果出现问题，可以尝试降级到 PyQt5 5.12.x

### 3. OpenCV 系统版本兼容性

#### 3.1 OpenCV API 版本差异
**潜在问题**: 系统自带的 OpenCV 版本可能与代码中使用的 API 不匹配

**检查方法**:
```bash
python3 -c "import cv2; print(cv2.__version__)"
```

**常见问题**:
- `cv2.data.haarcascades` 路径可能不存在（旧版本 OpenCV）
- `cv2.dnn` 模块可能不可用（基础版本 OpenCV）
- `cv2.CAP_PROP_*` 常量可能不同

**解决方案**: 见下方代码修复

#### 3.2 Haar Cascade 路径问题
**问题**: 旧版本 OpenCV 可能没有 `cv2.data.haarcascades`

**解决方案**: 代码中已有多路径回退机制

### 4. 硬件相关问题

#### 4.1 摄像头访问权限
**问题**: 开发板上可能需要特殊权限访问摄像头

**检查方法**:
```bash
ls -l /dev/video*
```

**解决方案**:
```bash
# 添加用户到 video 组
sudo usermod -a -G video $USER
# 或使用 sudo 运行
```

#### 4.2 摄像头设备索引
**问题**: 开发板上的摄像头可能不是 `/dev/video0`

**解决方案**: 修改 `config.yaml` 中的 `camera.index`

#### 4.3 GPU/加速支持
**问题**: CUDA/OpenCL 可能不可用

**解决方案**: 代码会自动回退到 CPU 模式

### 5. 路径和文件系统问题

#### 5.1 路径分隔符
**状态**: ✅ 代码使用 `os.path.join()` 和 `pathlib.Path`，跨平台兼容

#### 5.2 文件权限
**问题**: 日志文件、模型文件可能需要写权限

**解决方案**:
```bash
# 确保有写权限
chmod -R 755 yoloface/
# 或使用用户目录
```

#### 5.3 模型文件路径
**问题**: 模型文件可能不在预期位置

**解决方案**: 代码中有多路径查找机制

### 6. 运行时错误

#### 6.1 导入错误
**常见错误**: `ModuleNotFoundError` 或 `ImportError`

**排查步骤**:
1. 运行 `python3 scripts/check_imports.py` 检查所有依赖
2. 确认 Python 版本: `python3 --version`
3. 确认 pip 安装的包: `pip3 list`

#### 6.2 运行时崩溃
**常见原因**:
- 内存不足（YOLO 模型较大）
- 摄像头无法打开
- GUI 显示问题（无 X11 或远程连接）

**排查步骤**:
1. 检查内存: `free -h`
2. 检查摄像头: `v4l2-ctl --list-devices`
3. 检查显示: `echo $DISPLAY`

## 快速诊断脚本

创建 `scripts/diagnose.py` 用于快速诊断问题：

```python
#!/usr/bin/env python3
"""开发板环境诊断脚本"""

import sys
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 6, 3):
        print("❌ Python版本过低，需要 3.6.3+")
        return False
    print("✅ Python版本符合要求")
    return True

def check_opencv():
    """检查OpenCV"""
    try:
        import cv2
        print(f"✅ OpenCV版本: {cv2.__version__}")
        
        # 检查关键API
        if hasattr(cv2, 'data'):
            print("✅ cv2.data 可用")
        else:
            print("⚠️  cv2.data 不可用（旧版本OpenCV）")
            
        if hasattr(cv2, 'dnn'):
            print("✅ cv2.dnn 可用")
        else:
            print("⚠️  cv2.dnn 不可用（基础版OpenCV）")
            
        return True
    except ImportError as e:
        print(f"❌ OpenCV导入失败: {e}")
        return False

def check_dependencies():
    """检查依赖库"""
    deps = {
        'numpy': 'numpy',
        'PyQt5': 'PyQt5.QtWidgets',
        'torch': 'torch',
        'ultralytics': 'ultralytics',
        'yaml': 'yaml',
    }
    
    results = {}
    for name, module in deps.items():
        try:
            __import__(module)
            results[name] = True
            print(f"✅ {name} 可用")
        except ImportError as e:
            results[name] = False
            print(f"❌ {name} 不可用: {e}")
    
    return all(results.values())

def check_camera():
    """检查摄像头"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ 摄像头可以打开")
            cap.release()
            return True
        else:
            print("⚠️  摄像头无法打开（可能被占用或无权限）")
            cap.release()
            return False
    except Exception as e:
        print(f"⚠️  摄像头检查失败: {e}")
        return False

def check_paths():
    """检查路径"""
    import os
    from pathlib import Path
    
    paths_to_check = [
        'config.yaml',
        'models',
        'haarcascades',
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"✅ {path} 存在")
        else:
            print(f"⚠️  {path} 不存在")

if __name__ == '__main__':
    print("=" * 50)
    print("开发板环境诊断")
    print("=" * 50)
    
    all_ok = True
    all_ok &= check_python_version()
    print()
    all_ok &= check_opencv()
    print()
    all_ok &= check_dependencies()
    print()
    check_camera()
    print()
    check_paths()
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ 基本环境检查通过")
    else:
        print("❌ 发现一些问题，请查看上述输出")
    print("=" * 50)

```

## 常见错误及解决方案

### 错误1: `AttributeError: module 'cv2' has no attribute 'data'`
**原因**: OpenCV 版本过旧（< 3.4）

**解决方案**: 修改 `haar_detector.py`，使用硬编码路径

### 错误2: `ModuleNotFoundError: No module named 'ultralytics'`
**原因**: ultralytics 未安装或版本不兼容

**解决方案**: 
```bash
# 尝试安装兼容版本
pip3 install "ultralytics<8.0.0"
# 或
pip3 install ultralytics==7.0.0
```

### 错误3: `ImportError: cannot import name 'QApplication' from 'PyQt5.QtWidgets'`
**原因**: PyQt5 版本问题或未正确安装

**解决方案**:
```bash
pip3 install --upgrade PyQt5
# 或降级
pip3 install "PyQt5<5.15.0"
```

### 错误4: `RuntimeError: 无法打开摄像头 0`
**原因**: 摄像头权限或设备索引问题

**解决方案**:
1. 检查设备: `ls -l /dev/video*`
2. 修改 `config.yaml` 中的 `camera.index`
3. 使用 sudo 运行（临时方案）

### 错误5: `torch.cuda.is_available() returns False`
**原因**: 开发板可能没有 CUDA 支持

**解决方案**: 这是正常的，代码会自动使用 CPU

## 建议的部署步骤

1. **环境检查**
   ```bash
   python3 scripts/diagnose.py
   ```

2. **安装依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **检查导入**
   ```bash
   python3 scripts/check_imports.py
   ```

4. **测试运行**
   ```bash
   python3 -m yoloface.app
   ```

5. **如果遇到问题，查看日志**
   ```bash
   tail -f logs/app.log
   ```

## 联系支持

如果遇到本文档未覆盖的问题，请：
1. 运行诊断脚本并保存输出
2. 查看日志文件 `logs/app.log`
3. 记录完整的错误信息
4. 提供开发板系统信息: `uname -a` 和 `cat /etc/os-release`



