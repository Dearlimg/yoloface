"""
数据库管理模块（文件存储版本）
使用本地JSON文件存储用户数据
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Tuple, Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger(__name__)


class DatabaseManager:
    """数据库管理类（文件存储版本）"""

    def __init__(self, data_file: Optional[str] = None):
        """
        初始化文件存储管理器

        Args:
            data_file: 数据文件路径，如果为None则使用默认路径
        """
        try:
            config = get_config()
            # 获取数据目录配置
            paths_config = config.get('paths', {})
            output_dir = paths_config.get('output_dir', 'data/output')
        except Exception as e:
            logger.warning(f"获取配置失败，使用默认值: {e}")
            output_dir = 'data/output'
        
        # 确保输出目录存在
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 数据文件路径
        if data_file:
            self.data_file = Path(data_file)
        else:
            self.data_file = output_path / 'users.json'
        
        # 确保数据文件存在
        if not self.data_file.exists():
            self._init_data_file()
        
        logger.info(f"使用文件存储: {self.data_file}")

    def _init_data_file(self):
        """初始化数据文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'users': []}, f, ensure_ascii=False, indent=2)
            logger.info(f"创建数据文件: {self.data_file}")
        except Exception as e:
            logger.error(f"创建数据文件失败: {e}")

    def _load_data(self) -> dict:
        """加载数据文件"""
        try:
            if not self.data_file.exists():
                self._init_data_file()
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 确保数据结构正确
            if 'users' not in data:
                data['users'] = []
            
            return data
        except json.JSONDecodeError:
            logger.warning("数据文件格式错误，重新初始化")
            self._init_data_file()
            return {'users': []}
        except Exception as e:
            logger.error(f"加载数据文件失败: {e}")
            return {'users': []}

    def _save_data(self, data: dict):
        """保存数据到文件"""
        try:
            # 使用临时文件，确保原子性写入
            temp_file = self.data_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 替换原文件
            if os.name == 'nt':  # Windows
                if self.data_file.exists():
                    os.remove(self.data_file)
                os.rename(temp_file, self.data_file)
            else:  # Unix/Linux
                os.replace(temp_file, self.data_file)
            
        except Exception as e:
            logger.error(f"保存数据文件失败: {e}")
            # 清理临时文件
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except:
                pass
            raise

    def connect(self) -> bool:
        """连接（文件存储版本，总是返回True）"""
        try:
            # 确保数据文件存在
            if not self.data_file.exists():
                self._init_data_file()
            
            # 测试读写
            data = self._load_data()
            self._save_data(data)
            
            logger.info("文件存储初始化成功")
            return True
        except Exception as e:
            logger.error(f"文件存储初始化失败: {e}")
            return False

    @property
    def connection(self):
        """兼容性属性，返回self（表示已连接）"""
        return self if self.data_file.exists() else None

    def disconnect(self):
        """断开连接（文件存储版本，无需操作）"""
        logger.info("文件存储连接已关闭")

    def create_user_table(self) -> bool:
        """创建用户表（文件存储版本，确保数据文件存在）"""
        try:
            if not self.data_file.exists():
                self._init_data_file()
            else:
                # 验证文件格式
                data = self._load_data()
                if 'users' not in data:
                    data['users'] = []
                    self._save_data(data)
            
            logger.info("用户数据文件检查/创建成功")
            return True
        except Exception as e:
            logger.error(f"创建用户数据文件失败: {e}")
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
            data = self._load_data()
            users = data.get('users', [])
            
            # 检查用户是否已存在
            for user in users:
                if user.get('username') == username:
                    return False, "用户名已存在"
            
            # 添加新用户
            hashed_password = self.hash_password(password)
            new_user = {
                'id': len(users) + 1,
                'username': username,
                'password': hashed_password,
                'created_at': self._get_timestamp()
            }
            users.append(new_user)
            data['users'] = users
            
            self._save_data(data)
            logger.info(f"用户注册成功: {username}")
            return True, "注册成功"
            
        except Exception as e:
            logger.error(f"注册用户失败: {e}")
            return False, f"注册失败: {e}"

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
            data = self._load_data()
            users = data.get('users', [])
            
            # 查找用户
            user = None
            for u in users:
                if u.get('username') == username:
                    user = u
                    break
            
            if user is None:
                return False, "用户不存在"
            
            # 验证密码
            stored_password = user.get('password', '')
            hashed_input_password = self.hash_password(password)
            
            # 兼容旧数据（明文密码）和新数据（哈希密码）
            if stored_password == hashed_input_password or stored_password == password:
                logger.info(f"用户登录成功: {username}")
                return True, "登录成功"
            else:
                return False, "密码错误"
                
        except Exception as e:
            logger.error(f"登录失败: {e}")
            return False, f"登录失败: {e}"

    def user_exists(self, username: str) -> bool:
        """检查用户是否存在"""
        try:
            data = self._load_data()
            users = data.get('users', [])
            
            for user in users:
                if user.get('username') == username:
                    return True
            return False
        except Exception as e:
            logger.error(f"检查用户失败: {e}")
            return False

    @staticmethod
    def _get_timestamp() -> str:
        """获取当前时间戳字符串"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
