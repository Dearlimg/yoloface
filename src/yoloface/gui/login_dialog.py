"""
登录注册UI界面
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QStackedWidget, QWidget)

from ..utils.db_manager import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class LoginRegisterDialog(QDialog):
    """登录注册对话框"""

    login_success = pyqtSignal(str)  # 登录成功信号，传递用户名

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.db_manager = None
        self._db_initialized = False
        
        # 只初始化UI，不自动初始化数据库（避免崩溃）
        self.init_ui()
        
        # 不在初始化时自动连接数据库，只在用户操作时按需初始化

    def ensure_db_initialized(self):
        """确保数据存储已初始化（文件存储版本，更简单）"""
        if self._db_initialized:
            return True
        
        try:
            if not self.db_manager:
                logger.info("初始化数据管理器...")
                self.db_manager = DatabaseManager()
                logger.info("数据管理器创建成功")
            
            # 文件存储版本，连接总是成功
            if self.db_manager:
                try:
                    if self.db_manager.connect():
                        self.db_manager.create_user_table()
                        logger.info("数据存储初始化成功")
                        self._db_initialized = True
                        return True
                    else:
                        logger.warning("数据存储初始化失败")
                        return False
                except Exception as e:
                    logger.error(f"数据存储初始化异常: {type(e).__name__}: {e}")
                    return False
            else:
                return False
        except Exception as e:
            logger.error(f"数据存储初始化失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('登录/注册')
        self.setGeometry(100, 100, 400, 300)
        self.setModal(True)

        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                font-size: 12px;
            }
        """)

        # 创建堆栈窗口用于切换登录和注册界面
        self.stacked_widget = QStackedWidget()

        # 登录界面
        self.login_widget = self.create_login_widget()
        self.stacked_widget.addWidget(self.login_widget)

        # 注册界面
        self.register_widget = self.create_register_widget()
        self.stacked_widget.addWidget(self.register_widget)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # 默认显示登录界面
        self.stacked_widget.setCurrentIndex(0)

    def create_login_widget(self):
        """创建登录界面"""
        widget = QWidget()
        layout = QVBoxLayout()

        # 标题
        title = QLabel('用户登录')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # 用户名
        layout.addWidget(QLabel('用户名:'))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('请输入用户名')
        layout.addWidget(self.login_username)

        layout.addSpacing(10)

        # 密码
        layout.addWidget(QLabel('密码:'))
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('请输入密码')
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)

        layout.addSpacing(20)

        # 按钮布局
        button_layout = QHBoxLayout()

        login_btn = QPushButton('登录')
        login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(login_btn)

        to_register_btn = QPushButton('去注册')
        to_register_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        to_register_btn.clicked.connect(self.show_register)
        button_layout.addWidget(to_register_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_register_widget(self):
        """创建注册界面"""
        widget = QWidget()
        layout = QVBoxLayout()

        # 标题
        title = QLabel('用户注册')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # 用户名
        layout.addWidget(QLabel('用户名:'))
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText('请输入用户名（至少3个字符）')
        layout.addWidget(self.register_username)

        layout.addSpacing(10)

        # 密码
        layout.addWidget(QLabel('密码:'))
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('请输入密码（至少6个字符）')
        self.register_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.register_password)

        layout.addSpacing(10)

        # 确认密码
        layout.addWidget(QLabel('确认密码:'))
        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setPlaceholderText('请再次输入密码')
        self.register_password_confirm.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.register_password_confirm)

        layout.addSpacing(20)

        # 按钮布局
        button_layout = QHBoxLayout()

        register_btn = QPushButton('注册')
        register_btn.clicked.connect(self.handle_register)
        button_layout.addWidget(register_btn)

        to_login_btn = QPushButton('返回登录')
        to_login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        to_login_btn.clicked.connect(self.show_login)
        button_layout.addWidget(to_login_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def show_login(self):
        """显示登录界面"""
        self.stacked_widget.setCurrentIndex(0)
        self.clear_login_fields()

    def show_register(self):
        """显示注册界面"""
        self.stacked_widget.setCurrentIndex(1)
        self.clear_register_fields()

    def clear_login_fields(self):
        """清空登录字段"""
        self.login_username.clear()
        self.login_password.clear()

    def clear_register_fields(self):
        """清空注册字段"""
        self.register_username.clear()
        self.register_password.clear()
        self.register_password_confirm.clear()

    def handle_login(self):
        """处理登录"""
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空")
            return

        # 按需初始化数据库
        if not self.ensure_db_initialized():
            QMessageBox.warning(self, "警告", "数据存储未初始化，无法登录")
            return

        try:
            success, message = self.db_manager.login_user(username, password)

            if success:
                self.current_user = username
                QMessageBox.information(self, "成功", message)
                self.login_success.emit(username)
                self.accept()
            else:
                QMessageBox.warning(self, "失败", message)
        except Exception as e:
            logger.error(f"登录处理失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            QMessageBox.critical(self, "错误", f"登录过程出错: {e}")

    def handle_register(self):
        """处理注册"""
        username = self.register_username.text().strip()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()

        if not username or not password or not password_confirm:
            QMessageBox.warning(self, "警告", "所有字段都不能为空")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "警告", "两次输入的密码不一致")
            return

        # 按需初始化数据库
        if not self.ensure_db_initialized():
            QMessageBox.warning(self, "警告", "数据存储未初始化，无法注册")
            return

        try:
            success, message = self.db_manager.register_user(username, password)

            if success:
                QMessageBox.information(self, "成功", message + "，请返回登录")
                self.clear_register_fields()
                self.show_login()
            else:
                QMessageBox.warning(self, "失败", message)
        except Exception as e:
            logger.error(f"注册处理失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            QMessageBox.critical(self, "错误", f"注册过程出错: {e}")

    def closeEvent(self, event):
        """关闭事件"""
        try:
            if self.db_manager:
                self.db_manager.disconnect()
        except Exception as e:
            logger.error(f"关闭数据存储失败: {e}")
        event.accept()

