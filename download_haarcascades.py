#!/usr/bin/env python3
"""
下载OpenCV Haar级联分类器文件
"""

import os
import urllib.request
import sys

# Haar级联分类器文件列表
HAARCASCADES = {
    'haarcascade_frontalface_default.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml',
    'haarcascade_frontalface_alt.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt.xml',
    'haarcascade_frontalface_alt2.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml',
    'haarcascade_profileface.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_profileface.xml',
}

def download_haarcascades():
    """下载Haar级联分类器文件"""

    # 创建haarcascades目录
    haarcascades_dir = os.path.join(os.path.dirname(__file__), 'haarcascades')
    os.makedirs(haarcascades_dir, exist_ok=True)

    print(f"下载Haar级联分类器到: {haarcascades_dir}")
    print("-" * 60)

    for filename, url in HAARCASCADES.items():
        filepath = os.path.join(haarcascades_dir, filename)

        # 如果文件已存在，跳过
        if os.path.exists(filepath):
            print(f"✓ {filename} 已存在，跳过")
            continue

        try:
            print(f"下载 {filename}...", end=' ', flush=True)
            urllib.request.urlretrieve(url, filepath)
            print("✓ 完成")
        except Exception as e:
            print(f"✗ 失败: {e}")
            return False

    print("-" * 60)
    print("所有文件下载完成！")
    return True

if __name__ == '__main__':
    try:
        success = download_haarcascades()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

