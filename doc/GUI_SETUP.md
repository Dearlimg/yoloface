# 开发板GUI环境配置指南

## 概述

本系统需要GUI界面（PyQt5）才能运行。在开发板上配置GUI环境需要以下步骤。

## 方案一：本地显示（推荐）

如果开发板连接了显示器，直接运行即可。

### 1. 安装PyQt5

```bash
# 使用pip安装
pip3 install PyQt5

# 或者使用系统包管理器（如果可用）
# Ubuntu/Debian:
sudo apt-get install python3-pyqt5

# CentOS/RHEL:
sudo yum install python3-qt5
```

### 2. 设置显示环境

```bash
# 检查DISPLAY环境变量
echo $DISPLAY

# 如果为空，设置DISPLAY（通常为:0.0）
export DISPLAY=:0.0

# 或者添加到 ~/.bashrc
echo 'export DISPLAY=:0.0' >> ~/.bashrc
source ~/.bashrc
```

### 3. 运行程序

```bash
python3 -m yoloface.app
```

## 方案二：SSH X11转发

如果通过SSH远程连接开发板，可以使用X11转发。

### 1. 在本地机器上

```bash
# 使用X11转发连接
ssh -X username@开发板IP

# 或者使用信任的X11转发（如果遇到权限问题）
ssh -Y username@开发板IP
```

### 2. 在开发板上

```bash
# 确保X11转发已启用
echo $DISPLAY  # 应该显示类似 localhost:10.0

# 安装PyQt5
pip3 install PyQt5

# 运行程序
python3 -m yoloface.app
```

### 3. 常见问题

**问题**: `QXcbConnection: Could not connect to display`

**解决方案**:
```bash
# 检查X11转发
xauth list

# 如果为空，重新连接并确保使用 -X 或 -Y 参数
```

## 方案三：VNC远程桌面

使用VNC可以在没有物理显示器的开发板上运行GUI程序。

### 1. 在开发板上安装VNC服务器

```bash
# Ubuntu/Debian
sudo apt-get install tigervnc-standalone-server tigervnc-common

# CentOS/RHEL
sudo yum install tigervnc-server
```

### 2. 配置VNC服务器

```bash
# 设置VNC密码
vncpasswd

# 启动VNC服务器（分辨率1920x1080，深度24）
vncserver :1 -geometry 1920x1080 -depth 24
```

### 4. 在本地连接VNC

```bash
# 使用VNC客户端连接
# 地址: 开发板IP:5901 (5900 + 显示编号)
```

### 5. 在VNC会话中运行

```bash
# 设置DISPLAY
export DISPLAY=:1

# 运行程序
python3 -m yoloface.app
```

## 方案四：Xvfb虚拟显示（无头模式）

如果只需要运行程序而不需要看到界面，可以使用Xvfb创建虚拟显示。

### 1. 安装Xvfb

```bash
# Ubuntu/Debian
sudo apt-get install xvfb

# CentOS/RHEL
sudo yum install xorg-x11-server-Xvfb
```

### 2. 使用Xvfb运行

```bash
# 启动虚拟显示并运行程序
xvfb-run -a python3 -m yoloface.app
```

**注意**: 这种方式程序会运行，但你看不到界面。如果需要看到界面，请使用VNC。

## 方案五：使用Wayland（如果开发板支持）

某些现代Linux发行版使用Wayland而不是X11。

### 1. 检查显示协议

```bash
echo $XDG_SESSION_TYPE
# 输出: wayland 或 x11
```

### 2. 如果是Wayland

```bash
# 设置环境变量
export QT_QPA_PLATFORM=wayland

# 或者使用XWayland
export QT_QPA_PLATFORM=xcb
```

## 验证GUI环境

运行诊断脚本检查GUI环境：

```bash
python3 scripts/diagnose.py
```

或者手动测试：

```bash
python3 -c "from PyQt5.QtWidgets import QApplication; print('PyQt5可用')"
```

## 常见问题排查

### 问题1: `ImportError: No module named 'PyQt5'`

**解决方案**:
```bash
pip3 install PyQt5
# 如果pip安装失败，尝试使用系统包管理器
```

### 问题2: `QXcbConnection: Could not connect to display`

**原因**: DISPLAY环境变量未设置或X11连接失败

**解决方案**:
```bash
# 检查DISPLAY
echo $DISPLAY

# 设置DISPLAY
export DISPLAY=:0.0

# 如果通过SSH，确保使用 -X 或 -Y 参数
```

### 问题3: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`

**原因**: Qt平台插件缺失

**解决方案**:
```bash
# 安装Qt平台插件
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# 或者设置插件路径
export QT_PLUGIN_PATH=/usr/lib/qt5/plugins
```

### 问题4: 权限错误

**解决方案**:
```bash
# 添加用户到video组（摄像头权限）
sudo usermod -a -G video $USER

# 重新登录或使用newgrp
newgrp video
```

### 问题5: 字体问题

如果界面显示乱码或字体异常：

```bash
# 安装中文字体
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei

# 设置字体环境变量
export QT_QPA_FONTDIR=/usr/share/fonts
```

## 开发板特定配置

### EAIDK-310开发板

EAIDK-310通常运行Linux系统，可能需要：

1. **安装Qt依赖**:
```bash
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

2. **设置显示**:
```bash
# 如果使用HDMI输出
export DISPLAY=:0.0

# 如果使用VNC
export DISPLAY=:1
```

3. **摄像头权限**:
```bash
sudo chmod 666 /dev/video0
# 或添加用户到video组
sudo usermod -a -G video $USER
```

## 性能优化

在开发板上运行GUI可能较慢，可以：

1. **降低分辨率**:
   修改 `config.yaml` 中的摄像头分辨率

2. **减少帧率**:
   修改 `config.yaml` 中的 `performance.fps_update_interval`

3. **使用轻量级算法**:
   优先使用Haar或FastestV2算法，而不是YOLO11

## 测试GUI

运行简单的PyQt5测试：

```python
#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('GUI测试')
label = QLabel('GUI工作正常！', window)
label.move(50, 50)
window.resize(300, 100)
window.show()
sys.exit(app.exec_())
```

如果这个测试程序能正常显示窗口，说明GUI环境配置成功。

## 总结

1. **本地显示**: 最简单，直接连接显示器
2. **SSH X11转发**: 适合远程开发
3. **VNC**: 适合需要完整桌面环境
4. **Xvfb**: 适合无头服务器运行（看不到界面）

根据你的使用场景选择合适的方案。



