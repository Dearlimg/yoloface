"""
数据库管理模块
处理MySQL数据库连接和用户认证
"""

import hashlib

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_CONNECTOR_AVAILABLE = True
except ImportError:
    MYSQL_CONNECTOR_AVAILABLE = False
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        import MySQLdb as mysql
        from MySQLdb import Error
    except ImportError:
        pass


class DatabaseManager:
    """数据库管理类"""

    def __init__(self, host='113.44.144.219', port=3306, user='root', password='123456', database='xupt_sta'):
        """
        初始化数据库连接

        Args:
            host: 数据库主机地址
            port: 数据库端口
            user: 数据库用户名
            password: 数据库密码
            database: 数据库名称
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接到数据库"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("数据库连接成功")
            return True
        except Error as e:
            print(f"数据库连接失败: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("数据库连接已关闭")

    def create_user_table(self):
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
            print("用户表创建成功或已存在")
            return True
        except Error as e:
            print(f"创建用户表失败: {e}")
            return False

    @staticmethod
    def hash_password(password):
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
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
            insert_query = "INSERT INTO mv_user (name, password) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (username, password))
            self.connection.commit()
            return True, "注册成功"
        except mysql.connector.errors.IntegrityError:
            return False, "用户名已存在"
        except Error as e:
            return False, f"注册失败: {e}"

    def login_user(self, username, password):
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
            query = "SELECT password FROM mv_user WHERE name = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()

            if result is None:
                return False, "用户不存在"

            stored_password = result[0]
            hashed_input_password = self.hash_password(password)

            if stored_password == password:
                return True, "登录成功"
            else:
                return False, "密码错误"
        except Error as e:
            return False, f"登录失败: {e}"

    def user_exists(self, username):
        """检查用户是否存在"""
        try:
            query = "SELECT id FROM mv_user WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone() is not None
        except Error as e:
            print(f"检查用户失败: {e}")
            return False

