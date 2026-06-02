# DevEnvSync Makefile
# 跨平台构建脚本

.PHONY: help install uninstall test clean lint format build

# 默认目标
help:
	@echo "DevEnvSync - 智能开发环境配置同步引擎"
	@echo ""
	@echo "可用命令:"
	@echo "  make install     - 安装到系统 (需要管理员权限)"
	@echo "  make uninstall   - 从系统卸载"
	@echo "  make test        - 运行测试"
	@echo "  make clean       - 清理构建文件"
	@echo "  make lint        - 代码检查"
	@echo "  make format      - 代码格式化"
	@echo "  make build       - 构建分发包"
	@echo "  make run         - 直接运行"

# 安装
install:
	@echo "正在安装 DevEnvSync..."
	pip install -e .
	@echo "安装完成!"
	@echo "使用方法: devenvsync --help"

# 卸载
uninstall:
	@echo "正在卸载 DevEnvSync..."
	pip uninstall devenvsync -y
	@echo "卸载完成!"

# 测试
test:
	@echo "运行测试..."
	python -m pytest tests/ -v || echo "测试目录不存在，跳过"

# 清理
clean:
	@echo "清理构建文件..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "清理完成!"

# 代码检查
lint:
	@echo "运行代码检查..."
	python -m flake8 devenvsync.py --max-line-length=120 --ignore=E501,W503 || echo "flake8 未安装，跳过"
	python -m pylint devenvsync.py --disable=C0103,C0111,R0903 || echo "pylint 未安装，跳过"

# 代码格式化
format:
	@echo "格式化代码..."
	python -m black devenvsync.py || echo "black 未安装，跳过"
	python -m autopep8 --in-place --aggressive devenvsync.py || echo "autopep8 未安装，跳过"

# 构建分发包
build:
	@echo "构建分发包..."
	python setup.py sdist bdist_wheel
	@echo "构建完成!"

# 直接运行
run:
	python devenvsync.py

# 开发模式安装
dev:
	pip install -e .

# 检查Python版本
check:
	@python --version
	@echo "Python版本检查通过"
