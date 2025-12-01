.PHONY: install install-dev test clean run help

help:
	@echo "可用命令:"
	@echo "  make install      - 安装项目依赖"
	@echo "  make install-dev - 安装开发依赖"
	@echo "  make test        - 运行测试"
	@echo "  make run         - 运行主程序"
	@echo "  make clean       - 清理临时文件"
	@echo "  make help        - 显示此帮助信息"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

run:
	python -m yoloface.app

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

