"""
测试PyQt5对话框
用于诊断对话框崩溃问题
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

print("=" * 60)
print("测试PyQt5对话框")
print("=" * 60)

try:
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
    from PyQt5.QtCore import Qt
    
    print("\n[1] PyQt5导入成功")
    
    app = QApplication(sys.argv)
    print("[2] QApplication创建成功")
    
    # 创建最简单的对话框
    dialog = QDialog()
    dialog.setWindowTitle("测试对话框")
    dialog.setGeometry(100, 100, 300, 200)
    
    layout = QVBoxLayout()
    label = QLabel("这是一个测试对话框")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)
    
    button = QPushButton("关闭")
    button.clicked.connect(dialog.accept)
    layout.addWidget(button)
    
    dialog.setLayout(layout)
    print("[3] 对话框创建成功")
    
    print("[4] 显示对话框...")
    result = dialog.exec_()
    print(f"[5] 对话框返回: {result}")
    
    print("\n" + "=" * 60)
    print("测试完成！如果这里也崩溃，说明是PyQt5的问题")
    print("=" * 60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

