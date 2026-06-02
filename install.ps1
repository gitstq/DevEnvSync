# DevEnvSync Windows 安装脚本
# PowerShell 安装脚本

param(
    [Parameter()]
    [ValidateSet("install", "uninstall")]
    [string]$Action = "install"
)

# 颜色函数
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }

# 打印横幅
function Print-Banner {
    Write-Host @"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🚀 DevEnvSync - 智能开发环境配置同步引擎                ║
║   Intelligent Development Environment Config Sync        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan
}

# 检查Python
function Check-Python {
    Write-Info "检查Python版本..."
    
    $pythonCmd = $null
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonCmd = "python"
    } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
    }
    
    if (-not $pythonCmd) {
        Write-Error "未找到Python，请先安装Python 3.8或更高版本"
        Write-Info "下载地址: https://www.python.org/downloads/"
        exit 1
    }
    
    $version = & $pythonCmd --version 2>&1
    Write-Success "找到Python: $version"
    
    # 检查版本
    $versionStr = ($version -split " ")[1]
    $versionParts = $versionStr -split "\."
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Error "需要Python 3.8或更高版本"
        exit 1
    }
    
    return $pythonCmd
}

# 安装
function Install-DevEnvSync {
    Print-Banner
    $pythonCmd = Check-Python
    
    Write-Info "开始安装 DevEnvSync..."
    
    $installDir = "$env:LOCALAPPDATA\DevEnvSync"
    $binDir = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
    
    # 创建目录
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
    
    # 复制主程序
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    Copy-Item "$scriptPath\devenvsync.py" $installDir -Force
    
    # 创建启动脚本
    $launcherContent = @"
@echo off
$pythonCmd "$installDir\devenvsync.py" %*
"@
    Set-Content -Path "$binDir\devenvsync.bat" -Value $launcherContent
    
    # 创建快捷命令
    $shortcutContent = @"
@echo off
$pythonCmd "$installDir\devenvsync.py" %*
"@
    Set-Content -Path "$binDir\des.bat" -Value $shortcutContent
    
    Write-Success "安装完成!"
    Write-Info "使用方法:"
    Write-Host "  devenvsync --help    显示帮助信息"
    Write-Host "  devenvsync backup    创建配置备份"
    Write-Host "  devenvsync list      列出所有备份"
    Write-Host ""
    Write-Info "快捷命令: des (devenvsync的缩写)"
    Write-Host ""
    Write-Warning "请重新打开命令提示符或PowerShell以使用命令"
}

# 卸载
function Uninstall-DevEnvSync {
    Print-Banner
    Write-Info "开始卸载 DevEnvSync..."
    
    $installDir = "$env:LOCALAPPDATA\DevEnvSync"
    $binDir = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
    
    Remove-Item $installDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$binDir\devenvsync.bat" -Force -ErrorAction SilentlyContinue
    Remove-Item "$binDir\des.bat" -Force -ErrorAction SilentlyContinue
    
    Write-Success "卸载完成!"
}

# 主函数
switch ($Action) {
    "install" { Install-DevEnvSync }
    "uninstall" { Uninstall-DevEnvSync }
}
