"""
配置管理类
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path and os.path.exists(self.config_path):
            if YAML_AVAILABLE:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                import warnings
                warnings.warn("PyYAML未安装，使用默认配置。请运行: pip install PyYAML")
                self._config = self._get_default_config()
        else:
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'camera': {
                'index': 0,
                'width': 640,
                'height': 480,
                'fps': 30
            },
            'detection': {
                'haar': {
                    'cascade_path': None,  # None表示使用OpenCV内置
                    'scale_factor': 1.1,
                    'min_neighbors': 5,
                    'min_size': (30, 30)
                },
                'yolo11': {
                    'model_path': 'models/yolo11n.pt',
                    'conf_threshold': 0.25,
                    'iou_threshold': 0.45,
                    'imgsz': 640
                },
                'fastestv2': {
                    'model_path': 'yolo_fastestv2/model.onnx',
                    'conf_threshold': 0.25,
                    'imgsz': 416
                },
                'tracking': {
                    'iou_threshold': 0.3,
                    'max_history': 30,
                    'track_lost_threshold': 5
                }
            },
            'gui': {
                'window_title': '基于EAIDK-310的人脸识别系统',
                'window_width': 1200,
                'window_height': 800,
                'video_width': 640,
                'video_height': 480
            },
            'paths': {
                'models_dir': 'data/models',
                'haarcascades_dir': 'data/haarcascades',
                'output_dir': 'data/output',
                'logs_dir': 'logs'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'logs/app.log',
                'console': True
            },
            'performance': {
                'fps_update_interval': 30,
                'enable_multiprocess': False,
                'num_processes': 2
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键，如 'camera.index'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            path: 保存路径，如果为None则使用初始化时的路径
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML未安装，无法保存配置。请运行: pip install PyYAML")
        
        save_path = path or self.config_path
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._config.copy()


# 全局配置实例
_global_config: Optional[Config] = None


def load_config(config_path: Optional[str] = None) -> Config:
    """
    加载配置（单例模式）
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Config实例
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(config_path)
    return _global_config


def get_config() -> Config:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config

