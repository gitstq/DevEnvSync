#!/bin/bash
# DevEnvSync 安装脚本
# 支持 Linux/macOS

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 打印横幅
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║   🚀 DevEnvSync - 智能开发环境配置同步引擎                ║"
    echo "║   Intelligent Development Environment Config Sync        ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查Python版本
check_python() {
    print_info "检查Python版本..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "未找到Python，请先安装Python 3.8或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_success "找到Python: $PYTHON_VERSION"
    
    # 检查版本是否 >= 3.8
    REQUIRED_VERSION="3.8"
    if [ "$($PYTHON_CMD -c "import sys; print(sys.version_info >= (3, 8))")" != "True" ]; then
        print_error "需要Python 3.8或更高版本，当前版本: $PYTHON_VERSION"
        exit 1
    fi
}

# 安装
do_install() {
    print_banner
    check_python
    
    print_info "开始安装 DevEnvSync..."
    
    # 获取脚本所在目录
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    cd "$SCRIPT_DIR"
    
    # 创建安装目录
    INSTALL_DIR="$HOME/.local/share/devenvsync"
    mkdir -p "$INSTALL_DIR"
    
    # 复制主程序
    cp devenvsync.py "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/devenvsync.py"
    
    # 创建bin目录
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    
    # 创建启动脚本
    cat > "$BIN_DIR/devenvsync" << 'EOF'
#!/bin/bash
python3 "$HOME/.local/share/devenvsync/devenvsync.py" "$@"
EOF
    chmod +x "$BIN_DIR/devenvsync"
    
    # 创建快捷命令
    ln -sf "$BIN_DIR/devenvsync" "$BIN_DIR/des"
    
    # 添加到PATH
    SHELL_RC=""
    if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# DevEnvSync PATH" >> "$SHELL_RC"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            print_info "已添加到 $SHELL_RC，请运行 'source $SHELL_RC' 或重新打开终端"
        fi
    fi
    
    print_success "安装完成!"
    print_info "使用方法:"
    echo "  devenvsync --help    显示帮助信息"
    echo "  devenvsync backup    创建配置备份"
    echo "  devenvsync list      列出所有备份"
    echo ""
    print_info "快捷命令: des (devenvsync的缩写)"
    
    # 检查PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_warning "$BIN_DIR 不在PATH中"
        print_info "请运行以下命令或重新打开终端:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

# 卸载
do_uninstall() {
    print_banner
    print_info "开始卸载 DevEnvSync..."
    
    INSTALL_DIR="$HOME/.local/share/devenvsync"
    BIN_DIR="$HOME/.local/bin"
    
    # 删除文件
    rm -rf "$INSTALL_DIR"
    rm -f "$BIN_DIR/devenvsync"
    rm -f "$BIN_DIR/des"
    
    print_success "卸载完成!"
}

# 主函数
main() {
    case "${1:-install}" in
        install)
            do_install
            ;;
        uninstall)
            do_uninstall
            ;;
        *)
            echo "用法: $0 [install|uninstall]"
            exit 1
            ;;
    esac
}

main "$@"
