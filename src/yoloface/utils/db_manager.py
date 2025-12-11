"""
数据库管理模块
处理MySQL数据库连接和用户认证
"""

import hashlib
from typing import Tuple, Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger(__name__)

# 安全地导入MySQL驱动，避免崩溃
MYSQL_CONNECTOR_AVAILABLE = False
mysql = None
Error = Exception

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_CONNECTOR_AVAILABLE = True
    logger.info("使用 mysql.connector 作为MySQL驱动")
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb as mysql
        from MySQLdb import Error
        logger.info("使用 pymysql 作为MySQL驱动")
    except ImportError:
        logger.warning("未安装MySQL驱动，数据库功能将不可用")
        logger.warning("请运行: pip install mysql-connector-python 或 pip install pymysql")
    except Exception as e:
        logger.warning(f"MySQL驱动导入异常: {e}")


class DatabaseManager:
    """数据库管理类"""

    def __init__(self, host: Optional[str] = None, port: int = 3306, 
                 user: Optional[str] = None, password: Optional[str] = None, 
                 database: Optional[str] = None):
        """
        初始化数据库连接

        Args:
            host: 数据库主机地址
            port: 数据库端口
            user: 数据库用户名
            password: 数据库密码
            database: 数据库名称
        """
        # 安全地获取配置，避免崩溃
        try:
            config = get_config()
            db_config = config.get('database', {})
        except Exception as e:
            logger.warning(f"获取配置失败，使用默认值: {e}")
            db_config = {}
        
        self.host = host or db_config.get('host', '113.44.144.219')
        self.port = port or db_config.get('port', 3306)
        self.user = user or db_config.get('user', 'root')
        self.password = password or db_config.get('password', '123456')
        self.database = database or db_config.get('database', 'xupt_sta')
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """连接到数据库"""
        if not MYSQL_CONNECTOR_AVAILABLE and mysql is None:
            logger.warning("未安装MySQL驱动，请运行: pip install mysql-connector-python 或 pip install pymysql")
            return False
        
        try:
            if MYSQL_CONNECTOR_AVAILABLE:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    connect_timeout=5  # 5秒超时
                )
            else:
                self.connection = mysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.password,
                    db=self.database,
                    connect_timeout=5
                )
            self.cursor = self.connection.cursor()
            logger.info("数据库连接成功")
            return True
        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            return False
        except Exception as e:
            logger.error(f"数据库连接异常: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            try:
                if hasattr(self.connection, 'is_connected') and self.connection.is_connected():
                    self.cursor.close()
                    self.connection.close()
                    logger.info("数据库连接已关闭")
                elif hasattr(self.connection, 'close'):
                    self.cursor.close()
                    self.connection.close()
                    logger.info("数据库连接已关闭")
            except Exception as e:
                logger.error(f"关闭数据库连接失败: {e}")

    def create_user_table(self) -> bool:
        """创建用户表"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS mv_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info("用户表创建成功或已存在")
            return True
        except Error as e:
            logger.error(f"创建用户表失败: {e}")
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        注册新用户

        Args:
            username: 用户名
            password: 密码

        Returns:
            (success, message)
        """
        if not username or not password:
            return False, "用户名和密码不能为空"

        if len(username) < 3:
            return False, "用户名长度至少为3个字符"

        if len(password) < 6:
            return False, "密码长度至少为6个字符"

        try:
            hashed_password = self.hash_password(password)
            # 修复：使用正确的字段名
            insert_query = "INSERT INTO mv_user (username, password) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (username, hashed_password))
            self.connection.commit()
            logger.info(f"用户注册成功: {username}")
            return True, "注册成功"
        except Error as e:
            error_msg = str(e)
            if "Duplicate entry" in error_msg or "UNIQUE" in error_msg:
                return False, "用户名已存在"
            logger.error(f"注册失败: {e}")
            return False, f"注册失败: {error_msg}"

    def login_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        用户登录验证

        Args:
            username: 用户名
            password: 密码

        Returns:
            (success, message)
        """
        if not username or not password:
            return False, "用户名和密码不能为空"

        try:
            # 修复：使用正确的字段名
            query = "SELECT password FROM mv_user WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()

            if result is None:
                return False, "用户不存在"

            stored_password = result[0]
            hashed_input_password = self.hash_password(password)

            # 兼容旧数据（明文密码）和新数据（哈希密码）
            if stored_password == hashed_input_password or stored_password == password:
                logger.info(f"用户登录成功: {username}")
                return True, "登录成功"
            else:
                return False, "密码错误"
        except Error as e:
            logger.error(f"登录失败: {e}")
            return False, f"登录失败: {e}"

    def user_exists(self, username: str) -> bool:
        """检查用户是否存在"""
        try:
            query = "SELECT id FROM mv_user WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone() is not None
        except Error as e:
            logger.error(f"检查用户失败: {e}")
            return False

