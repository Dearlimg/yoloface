"""
测试启动脚本
用于诊断启动问题
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

print("=" * 60)
print("测试启动 - 逐步检查")
print("=" * 60)

# 1. 检查Python版本
print("\n[1] 检查Python版本...")
print(f"Python版本: {sys.version}")

# 2. 检查基本导入
print("\n[2] 检查基本模块导入...")
try:
    import cv2
    print(f"✓ OpenCV版本: {cv2.__version__}")
except Exception as e:
    print(f"✗ OpenCV导入失败: {e}")

# 3. 检查PyQt5
print("\n[3] 检查PyQt5...")
try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    print("✓ PyQt5导入成功")
except Exception as e:
    print(f"✗ PyQt5导入失败: {e}")
    sys.exit(1)

# 4. 创建QApplication
print("\n[4] 创建QApplication...")
try:
    app = QApplication(sys.argv)
    print("✓ QApplication创建成功")
except Exception as e:
    print(f"✗ QApplication创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 检查配置加载
print("\n[5] 检查配置加载...")
try:
    from yoloface.config import load_config
    config_path = project_root / 'config.yaml'
    config = load_config(str(config_path) if config_path.exists() else None)
    print("✓ 配置加载成功")
except Exception as e:
    print(f"✗ 配置加载失败: {e}")
    import traceback
    traceback.print_exc()

# 6. 检查数据库管理器（不连接）
print("\n[6] 检查数据库管理器...")
try:
    from yoloface.utils.db_manager import DatabaseManager
    db_manager = DatabaseManager()
    print("✓ 数据库管理器创建成功")
except Exception as e:
    print(f"✗ 数据库管理器创建失败: {e}")
    import traceback
    traceback.print_exc()

# 7. 检查登录对话框（不显示）
print("\n[7] 检查登录对话框类...")
try:
    from yoloface.gui.login_dialog import LoginRegisterDialog
    print("✓ 登录对话框类导入成功")
except Exception as e:
    print(f"✗ 登录对话框类导入失败: {e}")
    import traceback
    traceback.print_exc()

# 8. 检查主窗口（不显示）
print("\n[8] 检查主窗口类...")
try:
    from yoloface.gui.main_window import MainWindow
    print("✓ 主窗口类导入成功")
except Exception as e:
    print(f"✗ 主窗口类导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("所有检查完成！")
print("=" * 60)
print("\n如果所有检查都通过，可以尝试运行:")
print("  python -m yoloface.app")
print("\n如果仍有问题，可以临时禁用登录功能:")
print("  在config.yaml中设置: app.require_login: false")

