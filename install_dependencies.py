#!/usr/bin/env python3
"""
YoloFace 依赖安装脚本
自动安装项目所需的所有依赖包
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """运行命令并处理错误"""
    if description:
        print(f"\n{'='*60}")
        print(f"📦 {description}")
        print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {description} 失败")
        print(f"错误信息: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 YoloFace 依赖安装脚本")
    print("="*60)

    # 获取项目根目录
    project_root = Path(__file__).parent
    requirements_file = project_root / "requirements.txt"

    # 检查 requirements.txt 是否存在
    if not requirements_file.exists():
        print(f"❌ 错误: 找不到 {requirements_file}")
        sys.exit(1)

    print(f"📂 项目路径: {project_root}")
    print(f"📋 依赖文件: {requirements_file}")

    # 升级 pip
    print("\n[1/3] 升级 pip...")
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "升级 pip"
    )

    # 安装基础依赖
    print("\n[2/3] 安装基础依赖...")
    if not run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "安装 requirements.txt 中的依赖"
    ):
        print("⚠️  基础依赖安装失败，但继续尝试...")

    # 安装开发依赖（可选）
    print("\n[3/3] 安装开发依赖...")
    dev_deps = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.0.0",
    ]

    dev_deps_str = " ".join([f'"{dep}"' for dep in dev_deps])
    run_command(
        f"{sys.executable} -m pip install {dev_deps_str}",
        "安装开发依赖"
    )

    # 验证安装
    print("\n" + "="*60)
    print("✅ 验证安装...")
    print("="*60)

    required_packages = [
        "cv2",
        "PyQt5",
        "numpy",
        "ultralytics",
        "torch",
        "torchvision",
        "PIL",
        "yaml",
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing_packages.append(package)

    print("\n" + "="*60)
    if missing_packages:
        print(f"⚠️  以下包未成功安装: {', '.join(missing_packages)}")
        print("请手动运行以下命令:")
        print(f"  {sys.executable} -m pip install {' '.join(missing_packages)}")
        sys.exit(1)
    else:
        print("🎉 所有依赖安装成功！")
        print("="*60)
        sys.exit(0)


if __name__ == "__main__":
    main()

