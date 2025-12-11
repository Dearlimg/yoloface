#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发板环境诊断脚本
用于快速检查开发板环境是否满足运行要求
"""

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
            if hasattr(cv2.data, 'haarcascades'):
                print("✅ cv2.data.haarcascades 可用")
        else:
            print("⚠️  cv2.data 不可用（旧版本OpenCV）")
            
        if hasattr(cv2, 'dnn'):
            print("✅ cv2.dnn 可用")
        else:
            print("⚠️  cv2.dnn 不可用（基础版OpenCV）")
            
        # 检查常用常量
        if hasattr(cv2, 'CAP_PROP_FRAME_WIDTH'):
            print("✅ cv2.CAP_PROP_* 常量可用")
        else:
            print("⚠️  cv2.CAP_PROP_* 常量不可用")
            
        return True
    except ImportError as e:
        print(f"❌ OpenCV导入失败: {e}")
        return False

def check_dependencies():
    """检查依赖库"""
    deps = {
        'numpy': ('numpy', 'numpy'),
        'PyQt5': ('PyQt5', 'PyQt5.QtWidgets'),
        'torch': ('torch', 'torch'),
        'ultralytics': ('ultralytics', 'ultralytics'),
        'yaml': ('PyYAML', 'yaml'),
        'Pillow': ('Pillow', 'PIL'),
    }
    
    results = {}
    for name, (pkg_name, module) in deps.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            results[name] = True
            print(f"✅ {name} 可用 (版本: {version})")
        except ImportError as e:
            results[name] = False
            print(f"❌ {name} 不可用: {e}")
            if name == 'PyQt5':
                print(f"   请运行: pip3 install {pkg_name}")
                print(f"   或使用系统包管理器: sudo apt-get install python3-pyqt5")
            else:
                print(f"   请运行: pip3 install {pkg_name}")
    
    return all(results.values())

def check_gui_environment():
    """检查GUI环境"""
    print("\n检查GUI环境...")
    
    # 检查PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 可以导入")
    except ImportError as e:
        print(f"❌ PyQt5 导入失败: {e}")
        print("   请安装: pip3 install PyQt5")
        return False
    
    # 检查DISPLAY
    display = os.environ.get('DISPLAY')
    if display:
        print(f"✅ DISPLAY环境变量: {display}")
    else:
        print("⚠️  DISPLAY环境变量未设置")
        print("   提示: 设置 export DISPLAY=:0.0")
        print("   或使用SSH X11转发: ssh -X user@host")
        return False
    
    # 尝试创建QApplication（不显示窗口）
    try:
        import sys
        from PyQt5.QtWidgets import QApplication
        # 使用offscreen模式测试
        app = QApplication(sys.argv if hasattr(sys, 'argv') else [])
        print("✅ 可以创建QApplication")
        app.quit()
        return True
    except Exception as e:
        print(f"❌ 无法创建QApplication: {e}")
        print("   可能原因:")
        print("   1. X11服务器未运行")
        print("   2. 权限问题")
        print("   3. Qt平台插件缺失")
        return False

def check_camera():
    """检查摄像头"""
    try:
        import cv2
        print("\n检查摄像头设备...")
        
        # 检查设备文件
        video_devices = []
        for i in range(10):
            dev_path = f'/dev/video{i}'
            if os.path.exists(dev_path):
                video_devices.append(dev_path)
        
        if video_devices:
            print(f"✅ 发现视频设备: {', '.join(video_devices)}")
        else:
            print("⚠️  未发现 /dev/video* 设备")
        
        # 尝试打开摄像头
        print("\n尝试打开摄像头...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"✅ 摄像头可以打开 (分辨率: {width}x{height})")
            cap.release()
            return True
        else:
            print("⚠️  摄像头无法打开（可能被占用或无权限）")
            print("   提示: 尝试使用 sudo 运行，或检查摄像头权限")
            cap.release()
            return False
    except Exception as e:
        print(f"⚠️  摄像头检查失败: {e}")
        return False

def check_paths():
    """检查路径"""
    import os
    from pathlib import Path
    
    print("\n检查项目路径...")
    paths_to_check = [
        ('config.yaml', '配置文件'),
        ('models', '模型目录'),
        ('haarcascades', 'Haar级联目录'),
    ]
    
    all_exist = True
    for path, desc in paths_to_check:
        if os.path.exists(path):
            print(f"✅ {path} 存在 ({desc})")
        else:
            print(f"⚠️  {path} 不存在 ({desc})")
            all_exist = False
    
    return all_exist

def check_file_permissions():
    """检查文件权限"""
    print("\n检查文件权限...")
    try:
        test_file = 'test_write_permission.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✅ 当前目录有写权限")
        return True
    except Exception as e:
        print(f"❌ 当前目录无写权限: {e}")
        print("   提示: 日志文件可能无法创建")
        return False

def check_system_info():
    """检查系统信息"""
    print("\n系统信息:")
    try:
        import platform
        print(f"  系统: {platform.system()}")
        print(f"  架构: {platform.machine()}")
        print(f"  处理器: {platform.processor()}")
    except:
        pass
    
    try:
        import subprocess
        result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  内核: {result.stdout.strip()}")
    except:
        pass

if __name__ == '__main__':
    print("=" * 60)
    print("开发板环境诊断")
    print("=" * 60)
    
    all_ok = True
    all_ok &= check_python_version()
    print()
    all_ok &= check_opencv()
    print()
    all_ok &= check_dependencies()
    gui_ok = check_gui_environment()
    check_camera()
    check_paths()
    check_file_permissions()
    check_system_info()
    
    if not gui_ok:
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 基本环境检查通过，可以尝试运行程序")
        print("\n运行程序:")
        print("  python3 -m yoloface.app")
    else:
        print("❌ 发现一些问题，请查看上述输出并修复")
        print("\n建议:")
        print("1. 安装缺失的依赖: pip3 install -r requirements.txt")
        if not gui_ok:
            print("2. 配置GUI环境: 查看 doc/GUI_SETUP.md")
        print("3. 检查摄像头权限和设备")
        print("4. 查看详细文档:")
        print("   - doc/DEVICE_COMPATIBILITY.md")
        print("   - doc/GUI_SETUP.md")
    print("=" * 60)

