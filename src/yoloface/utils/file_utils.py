"""
文件工具模块
"""

import os
from pathlib import Path
from typing import Optional


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        Path对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_model_path(model_name: str, models_dir: str = 'data/models') -> str:
    """
    获取模型文件路径
    
    Args:
        model_name: 模型文件名
        models_dir: 模型目录
        
    Returns:
        模型文件完整路径
    """
    # 首先检查指定目录
    model_path = os.path.join(models_dir, model_name)
    if os.path.exists(model_path):
        return model_path
    
    # 检查当前目录
    if os.path.exists(model_name):
        return model_name
    
    # 检查models目录（旧路径兼容）
    old_path = os.path.join('models', model_name)
    if os.path.exists(old_path):
        return old_path
    
    return model_path


def find_file(filename: str, search_dirs: list) -> Optional[str]:
    """
    在多个目录中查找文件
    
    Args:
        filename: 文件名
        search_dirs: 搜索目录列表
        
    Returns:
        文件路径，如果未找到则返回None
    """
    for directory in search_dirs:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            return file_path
    return None

