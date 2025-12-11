#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载性别分类模型脚本
"""

import os
import sys
import urllib.request
from pathlib import Path

def download_file(url: str, save_path: str):
    """下载文件"""
    print(f"正在下载: {url}")
    print(f"保存到: {save_path}")
    
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        def progress_hook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r进度: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, save_path, progress_hook)
        print("\n✅ 下载完成!")
        return True
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("性别分类模型下载工具")
    print("=" * 60)
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("\n可用的性别分类模型:")
    print("1. OpenCV官方性别分类模型 (Caffe格式)")
    print("2. 手动下载说明")
    
    choice = input("\n请选择 (1/2): ").strip()
    
    if choice == "1":
        print("\n正在下载OpenCV官方性别分类模型...")
        print("注意: 这些模型需要从OpenCV官方仓库获取")
        print("\n请访问以下链接手动下载:")
        print("https://github.com/opencv/opencv/tree/master/samples/dnn")
        print("\n或使用以下命令:")
        print("wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt")
        print("wget https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/gender_net.caffemodel")
        
        # 尝试从常见来源下载
        print("\n尝试从备用源下载...")
        
        # 注意：这些URL可能需要更新
        prototxt_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/gender_deploy.prototxt"
        model_url = "https://github.com/opencv/opencv_extra/raw/master/testdata/dnn/gender_net.caffemodel"
        
        prototxt_path = models_dir / "gender_deploy.prototxt"
        model_path = models_dir / "gender_net.caffemodel"
        
        if download_file(prototxt_url, str(prototxt_path)):
            print(f"✅ Prototxt文件已保存到: {prototxt_path}")
        
        if download_file(model_url, str(model_path)):
            print(f"✅ 模型文件已保存到: {model_path}")
            print("\n配置说明:")
            print("在 config.yaml 中添加:")
            print(f"  detection:")
            print(f"    gender:")
            print(f"      model_path: \"{model_path}\"")
            print(f"      prototxt_path: \"{prototxt_path}\"")
    
    elif choice == "2":
        print("\n手动下载说明:")
        print("=" * 60)
        print("\n1. 推荐模型来源:")
        print("   - OpenCV官方: https://github.com/opencv/opencv")
        print("   - GitHub搜索: 'gender classification caffe' 或 'gender classification onnx'")
        print("   - 模型格式: Caffe (.caffemodel + .prototxt) 或 ONNX (.onnx)")
        print("\n2. 模型要求:")
        print("   - 输入尺寸: 通常为 227x227 或 224x224")
        print("   - 输出: 2个值（男性概率、女性概率）")
        print("\n3. 放置位置:")
        print("   - 将模型文件放到 models/ 目录")
        print("   - 或 data/models/ 目录")
        print("\n4. 配置:")
        print("   在 config.yaml 中设置 model_path")
        print("=" * 60)
    
    else:
        print("无效选择")

if __name__ == '__main__':
    main()

