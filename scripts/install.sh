#!/bin/bash

# 安装脚本
# 用于安装项目依赖和设置环境

echo "========================================="
echo "基于EAIDK-310的人脸识别系统 - 安装脚本"
echo "========================================="

# 检查Python版本
echo "检查Python版本..."
python3 --version

if [ $? -ne 0 ]; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境? (y/n): " create_venv
if [ "$create_venv" = "y" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "虚拟环境已创建并激活"
fi

# 安装依赖
echo "安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p haarcascades
mkdir -p models
mkdir -p yolo_fastestv2

echo "========================================="
echo "安装完成！"
echo "========================================="
echo ""
echo "使用方法:"
echo "1. 运行主程序: python -m yoloface.app"
echo "2. 运行测试: python -m pytest tests/"
echo "3. 检查依赖: python scripts/check_imports.py"
echo ""
echo "注意:"
echo "- 首次运行YOLO11时会自动下载预训练模型"
echo "- 确保摄像头已连接并可用"
echo ""

