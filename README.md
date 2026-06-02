# 🚀 DevEnvSync - 智能开发环境配置同步引擎

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-orange.svg)]()

**English** | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## 🎉 Introduction

**DevEnvSync** is a lightweight, zero-dependency, cross-platform development environment configuration management tool. It helps developers easily synchronize, backup, and restore their precious dotfiles and development environment configurations across multiple devices.

### ✨ Key Features

- 🔄 **Smart Sync** - Automatically identify and sync configuration files
- 💾 **Backup & Restore** - One-click backup and restore of all configurations
- 🔍 **Config Scan** - Automatically scan common configuration files
- 📦 **Import/Export** - Easily migrate configurations between devices
- 🔐 **Safe & Reliable** - Automatic backup before any modification
- 🎯 **Zero Dependencies** - Pure Python standard library implementation
- 🌐 **Cross-Platform** - Supports Linux, macOS, and Windows

---

## 🚀 Quick Start

### Installation

#### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/lobster8k/DevEnvSync.git
cd DevEnvSync

# Install
chmod +x install.sh
./install.sh

# Or install with pip
pip install .
```

#### Windows

```powershell
# Clone the repository
git clone https://github.com/lobster8k/DevEnvSync.git
cd DevEnvSync

# Install
.\install.ps1
```

### Usage

```bash
# Create a backup
devenvsync backup

# List all backups
devenvsync list

# Restore from backup
devenvsync restore

# Scan local configurations
devenvsync scan

# Export configurations
devenvsync export ~/my-configs

# Import configurations
devenvsync import ~/my-configs

# Show help
devenvsync --help
```

---

## 📖 Detailed Usage Guide

### Supported Configuration Files

DevEnvSync automatically recognizes the following configuration files:

**Shell Configuration:**
- `.bashrc`, `.bash_profile`, `.bash_aliases`
- `.zshrc`, `.zprofile`, `.zsh_aliases`
- `.profile`, `.aliases`

**Editor Configuration:**
- `.vimrc`, `.nvimrc`, `.vim/`
- `.config/nvim/`, `.config/fish/`

**Git Configuration:**
- `.gitconfig`, `.gitignore_global`

**Terminal Configuration:**
- `.tmux.conf`, `.screenrc`
- `.config/alacritty/`, `.config/kitty/`

**Security Configuration:**
- `.ssh/config`, `.gnupg/gpg.conf`

### Custom Configuration

```bash
# Add custom sync pattern
devenvsync config --add-pattern ".myconfig"

# Remove sync pattern
devenvsync config --remove-pattern ".myconfig"

# Show current configuration
devenvsync config --show
```

---

## 💡 Design Philosophy

DevEnvSync was born to solve a common developer pain point: **How to quickly synchronize development environments across multiple devices?**

We adhere to the following design principles:

1. **Simplicity First** - Zero dependencies, ready to use out of the box
2. **Safety First** - Automatic backup before any operation
3. **Privacy First** - All data stored locally, no cloud upload
4. **Cross-Platform** - Consistent experience across all platforms

---

## 📦 Packaging & Deployment

### Build from Source

```bash
# Install build dependencies
pip install setuptools wheel

# Build distribution package
make build

# Or use Python directly
python setup.py sdist bdist_wheel
```

### Direct Execution

```bash
# No installation required, run directly
python devenvsync.py --help
```

---

## 🤝 Contributing

We welcome all forms of contributions!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Thanks to all developers who contributed to this project
- Inspired by various dotfiles management tools

---

<div align="center">

**Made with ❤️ by DevEnvSync Team**

</div>

---

# 简体中文

## 🎉 项目介绍

**DevEnvSync** 是一个轻量级、零依赖、跨平台的开发环境配置管理工具。它帮助开发者轻松同步、备份和恢复珍贵的 dotfiles 和开发环境配置。

### ✨ 核心特性

- 🔄 **智能同步** - 自动识别并同步配置文件
- 💾 **备份恢复** - 一键备份和恢复所有配置
- 🔍 **配置扫描** - 自动扫描常见配置文件
- 📦 **导入导出** - 轻松在设备间迁移配置
- 🔐 **安全可靠** - 任何修改前自动备份
- 🎯 **零依赖** - 纯Python标准库实现
- 🌐 **跨平台** - 支持Linux、macOS和Windows

### 🚀 快速开始

```bash
# 创建备份
devenvsync backup

# 列出所有备份
devenvsync list

# 从备份恢复
devenvsync restore

# 扫描本地配置
devenvsync scan
```

---

# 繁體中文

## 🎉 專案介紹

**DevEnvSync** 是一個輕量級、零依賴、跨平台的開發環境配置管理工具。它幫助開發者輕鬆同步、備份和恢復珍貴的 dotfiles 和開發環境配置。

### ✨ 核心特性

- 🔄 **智能同步** - 自動識別並同步配置文件
- 💾 **備份恢復** - 一鍵備份和恢復所有配置
- 🔍 **配置掃描** - 自動掃描常見配置文件
- 📦 **導入導出** - 輕鬆在設備間遷移配置
- 🔐 **安全可靠** - 任何修改前自動備份
- 🎯 **零依賴** - 純Python標準庫實現
- 🌐 **跨平台** - 支持Linux、macOS和Windows

### 🚀 快速開始

```bash
# 創建備份
devenvsync backup

# 列出所有備份
devenvsync list

# 從備份恢復
devenvsync restore

# 掃描本地配置
devenvsync scan
```
