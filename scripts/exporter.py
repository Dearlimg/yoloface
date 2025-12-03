"""
模型导出工具
将PyTorch模型导出为ONNX、NCNN等格式，用于EAIDK-310部署
"""

import torch
from ultralytics import YOLO
import argparse
import os


def export_to_onnx(model_path, output_path=None, imgsz=640):
    """
    导出模型为ONNX格式
    
    Args:
        model_path: 输入模型路径
        output_path: 输出路径
        imgsz: 输入图像尺寸
    """
    try:
        print(f"加载模型: {model_path}")
        model = YOLO(model_path)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(model_path))[0]
            output_path = f"{base_name}.onnx"
        
        print(f"导出ONNX模型到: {output_path}")
        model.export(format='onnx', imgsz=imgsz, simplify=True)
        print(f"ONNX模型导出成功: {output_path}")
        return output_path
    except Exception as e:
        print(f"导出ONNX模型失败: {e}")
        return None


def export_to_ncnn(model_path, output_dir=None, imgsz=640):
    """
    导出模型为NCNN格式（用于EAIDK-310）
    
    Args:
        model_path: 输入模型路径
        output_dir: 输出目录
        imgsz: 输入图像尺寸
    """
    try:
        print(f"加载模型: {model_path}")
        model = YOLO(model_path)
        
        if output_dir is None:
            base_name = os.path.splitext(os.path.basename(model_path))[0]
            output_dir = f"{base_name}_ncnn_model"
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"导出NCNN模型到: {output_dir}")
        model.export(format='ncnn', imgsz=imgsz)
        
        # 移动文件到输出目录
        base_name = os.path.splitext(os.path.basename(model_path))[0]
        ncnn_files = [f"{base_name}.param", f"{base_name}.bin"]
        
        for file in ncnn_files:
            if os.path.exists(file):
                import shutil
                shutil.move(file, os.path.join(output_dir, file))
        
        print(f"NCNN模型导出成功: {output_dir}")
        return output_dir
    except Exception as e:
        print(f"导出NCNN模型失败: {e}")
        return None


def export_to_tensorrt(model_path, output_path=None, imgsz=640):
    """
    导出模型为TensorRT格式
    
    Args:
        model_path: 输入模型路径
        output_path: 输出路径
        imgsz: 输入图像尺寸
    """
    try:
        print(f"加载模型: {model_path}")
        model = YOLO(model_path)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(model_path))[0]
            output_path = f"{base_name}.engine"
        
        print(f"导出TensorRT模型到: {output_path}")
        model.export(format='engine', imgsz=imgsz)
        print(f"TensorRT模型导出成功: {output_path}")
        return output_path
    except Exception as e:
        print(f"导出TensorRT模型失败: {e}")
        return None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='模型导出工具')
    parser.add_argument('--model', type=str, required=True, help='输入模型路径')
    parser.add_argument('--format', type=str, choices=['onnx', 'ncnn', 'tensorrt', 'all'],
                       default='onnx', help='导出格式')
    parser.add_argument('--output', type=str, default=None, help='输出路径/目录')
    parser.add_argument('--imgsz', type=int, default=640, help='输入图像尺寸')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"错误: 模型文件不存在: {args.model}")
        return
    
    if args.format == 'all':
        export_to_onnx(args.model, args.output, args.imgsz)
        export_to_ncnn(args.model, args.output, args.imgsz)
    elif args.format == 'onnx':
        export_to_onnx(args.model, args.output, args.imgsz)
    elif args.format == 'ncnn':
        export_to_ncnn(args.model, args.output, args.imgsz)
    elif args.format == 'tensorrt':
        export_to_tensorrt(args.model, args.output, args.imgsz)
    
    print("导出完成")


if __name__ == '__main__':
    main()

