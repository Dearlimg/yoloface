"""
文本绘制工具
解决OpenCV无法显示中文的问题
"""

import cv2
import numpy as np
from typing import Tuple, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def put_chinese_text(
    img: np.ndarray,
    text: str,
    position: Tuple[int, int],
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    在图像上绘制中文文本
    
    Args:
        img: 输入图像 (BGR格式)
        text: 要绘制的文本
        position: 文本位置 (x, y)
        font_scale: 字体大小
        color: 文本颜色 (B, G, R)
        thickness: 线条粗细
        
    Returns:
        绘制了文本的图像
    """
    # 如果文本不包含中文字符，直接使用OpenCV
    if not any('\u4e00' <= char <= '\u9fff' for char in text):
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
        return img
    
    # 如果包含中文且PIL可用，使用PIL绘制
    if PIL_AVAILABLE:
        try:
            # 转换为PIL图像
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)
            
            # 尝试加载中文字体
            font = None
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                '/System/Library/Fonts/PingFang.ttc',  # macOS
                'C:/Windows/Fonts/simhei.ttf',  # Windows
                'C:/Windows/Fonts/msyh.ttc',  # Windows
            ]
            
            font_size = int(font_scale * 20)
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
            
            # 如果没有找到字体，使用默认字体
            if font is None:
                font = ImageFont.load_default()
            
            # 绘制文本
            # PIL使用RGB颜色，需要转换
            rgb_color = (color[2], color[1], color[0])
            draw.text(position, text, font=font, fill=rgb_color)
            
            # 转换回OpenCV格式
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            return img
        except Exception as e:
            # 如果PIL绘制失败，回退到OpenCV（会显示为??）
            pass
    
    # 回退到OpenCV（中文会显示为??）
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
               font_scale, color, thickness)
    return img

