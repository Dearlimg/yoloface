"""
主应用程序入口
集成登录注册功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from yoloface.gui.main_window import MainWindow
from yoloface.utils.logger import setup_logger, get_logger
from yoloface.config import load_config


def main():
    """主函数"""
    # 加载配置
    config_path = project_root / 'config.yaml'
    config = load_config(str(config_path) if config_path.exists() else None)
    
    # 设置日志
    log_config = config.get('logging', {})
    logger = setup_logger(
        name='yoloface',
        level=log_config.get('level', 'INFO'),
        log_file=log_config.get('file'),
        console=log_config.get('console', True),
        format_str=log_config.get('format')
    )
    
    logger.info("启动人脸识别系统")
    
    # 导入PyQt5
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        logger.error("PyQt5未安装，请运行: pip install PyQt5")
        sys.exit(1)
    except Exception as e:
        logger.error(f"PyQt5导入失败: {e}")
        sys.exit(1)
    
    # 创建应用（必须在导入其他PyQt5组件之前）
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("YoloFace")
        app.setApplicationVersion("1.0.0")
    except Exception as e:
        logger.error(f"创建QApplication失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    
    # 检查是否需要登录
    enable_login = config.get('app.require_login', True)
    username = None
    
    if enable_login:
        try:
            logger.info("尝试加载登录模块...")
            from yoloface.gui.login_dialog import LoginRegisterDialog
            from PyQt5.QtWidgets import QDialog
            
            logger.info("创建登录对话框...")
            # 创建登录注册对话框（不立即初始化数据库）
            login_dialog = None
            try:
                login_dialog = LoginRegisterDialog()
                logger.info("登录对话框创建成功")
            except Exception as e:
                logger.error(f"创建登录对话框失败: {e}")
                import traceback
                logger.error(traceback.format_exc())
                # 如果创建失败，询问是否继续
                try:
                    from PyQt5.QtWidgets import QMessageBox
                    reply = QMessageBox.question(
                        None,
                        "对话框错误",
                        f"登录对话框创建失败: {e}\n\n是否跳过登录继续运行？",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        sys.exit(1)
                    # 跳过登录
                    login_dialog = None
                except:
                    logger.warning("无法显示错误对话框，跳过登录继续运行")
                    login_dialog = None
            
            result = QDialog.Rejected
            if login_dialog:
                logger.info("显示登录对话框...")
                # 显示对话框（阻塞直到关闭）
                try:
                    result = login_dialog.exec_()
                    logger.info(f"登录对话框返回: {result}")
                except Exception as e:
                    logger.error(f"显示登录对话框失败: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    # 如果对话框显示失败，询问是否继续
                    try:
                        from PyQt5.QtWidgets import QMessageBox
                        reply = QMessageBox.question(
                            None,
                            "对话框错误",
                            f"登录对话框显示失败: {e}\n\n是否跳过登录继续运行？",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        if reply == QMessageBox.No:
                            sys.exit(1)
                        result = QDialog.Rejected
                    except:
                        logger.warning("无法显示错误对话框，跳过登录继续运行")
                        result = QDialog.Rejected
            
            if result == QDialog.Accepted:
                # 登录成功
                username = login_dialog.current_user
                logger.info(f"用户登录成功: {username}")
            else:
                # 用户取消登录
                logger.info("用户取消登录")
                sys.exit(0)
        except ImportError as e:
            logger.warning(f"无法加载登录模块: {e}，跳过登录")
            logger.warning("提示: 如果不需要登录功能，可在config.yaml中设置 app.require_login: false")
        except Exception as e:
            logger.error(f"登录过程出错: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # 询问是否继续
            try:
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    None, 
                    "登录失败", 
                    f"登录功能出错: {e}\n\n是否跳过登录继续运行？",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    sys.exit(1)
            except Exception as dialog_error:
                # 如果连对话框都显示不了，直接跳过
                logger.warning(f"无法显示错误对话框: {dialog_error}，跳过登录继续运行")
    
    # 创建主窗口（传入用户名）
    window = MainWindow(config, username=username)
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

