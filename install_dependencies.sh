#!/bin/bash

# YoloFace 依赖安装脚本 (Shell 版本)
# 自动安装项目所需的所有依赖包

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

# 打印带颜色的消息
print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 主函数
main() {
    print_header "🚀 YoloFace 依赖安装脚本"

    # 检查 Python 是否安装
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 版本: $PYTHON_VERSION"

    # 检查 requirements.txt 是否存在
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "找不到 $REQUIREMENTS_FILE"
        exit 1
    fi

    print_success "项目路径: $PROJECT_ROOT"
    print_success "依赖文件: $REQUIREMENTS_FILE"

    # 升级 pip
    print_header "[1/3] 升级 pip"
    python3 -m pip install --upgrade pip || print_warning "pip 升级失败，继续..."

    # 安装基础依赖
    print_header "[2/3] 安装基础依赖"
    if python3 -m pip install -r "$REQUIREMENTS_FILE"; then
        print_success "基础依赖安装成功"
    else
        print_warning "基础依赖安装失败，但继续..."
    fi

    # 安装开发依赖（可选）
    print_header "[3/3] 安装开发依赖"
    python3 -m pip install \
        "pytest>=7.0.0" \
        "pytest-cov>=4.0.0" \
        "black>=23.0.0" \
        "flake8>=6.0.0" \
        "mypy>=1.0.0" || print_warning "开发依赖安装失败"

    # 验证安装
    print_header "✅ 验证安装"

    MISSING_PACKAGES=()

    for package in cv2 PyQt5 numpy ultralytics torch torchvision PIL yaml; do
        if python3 -c "import $package" 2>/dev/null; then
            print_success "$package"
        else
            print_error "$package"
            MISSING_PACKAGES+=("$package")
        fi
    done

    print_header "安装完成"

    if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
        echo -e "${GREEN}🎉 所有依赖安装成功！${NC}"
        exit 0
    else
        print_warning "以下包未成功安装: ${MISSING_PACKAGES[*]}"
        echo "请手动运行以下命令:"
        echo "  python3 -m pip install ${MISSING_PACKAGES[*]}"
        exit 1
    fi
}

# 运行主函数
main

