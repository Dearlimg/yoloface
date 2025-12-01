"""
主应用程序入口
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
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("YoloFace")
    app.setApplicationVersion("1.0.0")
    
    # 创建主窗口
    window = MainWindow(config)
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

