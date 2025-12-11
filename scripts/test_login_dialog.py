"""
测试登录对话框（最小版本）
用于诊断崩溃问题
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

print("=" * 60)
print("测试登录对话框（最小版本）")
print("=" * 60)

try:
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
    from PyQt5.QtCore import Qt
    
    print("\n[1] PyQt5导入成功")
    
    app = QApplication(sys.argv)
    print("[2] QApplication创建成功")
    
    # 创建最简单的登录对话框
    class SimpleLoginDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("简单登录测试")
            self.setGeometry(100, 100, 300, 200)
            
            layout = QVBoxLayout()
            
            label = QLabel("这是一个简单的登录对话框测试")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            
            username_label = QLabel("用户名:")
            layout.addWidget(username_label)
            
            self.username = QLineEdit()
            self.username.setPlaceholderText("请输入用户名")
            layout.addWidget(self.username)
            
            password_label = QLabel("密码:")
            layout.addWidget(password_label)
            
            self.password = QLineEdit()
            self.password.setEchoMode(QLineEdit.Password)
            self.password.setPlaceholderText("请输入密码")
            layout.addWidget(self.password)
            
            button = QPushButton("登录")
            button.clicked.connect(self.accept)
            layout.addWidget(button)
            
            cancel_btn = QPushButton("取消")
            cancel_btn.clicked.connect(self.reject)
            layout.addWidget(cancel_btn)
            
            self.setLayout(layout)
    
    print("[3] 创建简单登录对话框...")
    dialog = SimpleLoginDialog()
    print("[4] 对话框创建成功")
    
    print("[5] 显示对话框...")
    result = dialog.exec_()
    print(f"[6] 对话框返回: {result}")
    
    if result == QDialog.Accepted:
        print(f"[7] 用户输入: {dialog.username.text()}")
    
    print("\n" + "=" * 60)
    print("简单对话框测试完成！")
    print("=" * 60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

