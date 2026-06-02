#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevEnvSync - 智能开发环境配置同步引擎
Intelligent Development Environment Configuration Sync Engine

一个轻量级、零依赖的跨平台开发环境配置管理工具，支持 dotfiles、
shell配置、编辑器配置的智能同步与版本管理。

Author: DevEnvSync Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
import getpass
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


__version__ = "1.0.0"
__author__ = "DevEnvSync Team"


class Colors:
    """终端颜色定义"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class Config:
    """配置常量"""
    APP_NAME = "DevEnvSync"
    CONFIG_DIR = Path.home() / ".config" / "devenvsync"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    BACKUP_DIR = CONFIG_DIR / "backups"
    LOG_FILE = CONFIG_DIR / "devenvsync.log"
    
    # 默认同步配置
    DEFAULT_PATTERNS = [
        ".bashrc", ".bash_profile", ".bash_aliases",
        ".zshrc", ".zprofile", ".zsh_aliases",
        ".vimrc", ".nvimrc", ".vim",
        ".gitconfig", ".gitignore_global",
        ".ssh/config", ".gnupg/gpg.conf",
        ".tmux.conf", ".screenrc",
        ".profile", ".aliases",
    ]
    
    DEFAULT_DIRS = [
        ".config/nvim",
        ".config/fish",
        ".config/alacritty",
        ".config/kitty",
        ".config/vscode",
        ".config/code",
    ]


class Logger:
    """日志记录器"""
    
    @staticmethod
    def log(message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # 确保日志目录存在
        Config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    @staticmethod
    def info(message: str):
        """信息日志"""
        Logger.log(message, "INFO")
    
    @staticmethod
    def error(message: str):
        """错误日志"""
        Logger.log(message, "ERROR")
    
    @staticmethod
    def warning(message: str):
        """警告日志"""
        Logger.log(message, "WARNING")


class UI:
    """终端UI工具"""
    
    @staticmethod
    def print_banner():
        """打印程序横幅"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🚀 DevEnvSync - 智能开发环境配置同步引擎                ║
║   Intelligent Development Environment Config Sync        ║
║                                                          ║
║   Version: {__version__}                                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
    
    @staticmethod
    def success(message: str):
        """打印成功消息"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    
    @staticmethod
    def error(message: str):
        """打印错误消息"""
        print(f"{Colors.FAIL}❌ {message}{Colors.END}")
    
    @staticmethod
    def warning(message: str):
        """打印警告消息"""
        print(f"{Colors.WARNING}⚠️  {message}{Colors.END}")
    
    @staticmethod
    def info(message: str):
        """打印信息消息"""
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")
    
    @staticmethod
    def header(message: str):
        """打印标题"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{message}{Colors.END}")
        print("=" * 60)
    
    @staticmethod
    def ask(message: str) -> str:
        """询问用户输入"""
        return input(f"{Colors.WARNING}❓ {message}: {Colors.END}")
    
    @staticmethod
    def confirm(message: str) -> bool:
        """确认对话框"""
        response = input(f"{Colors.WARNING}❓ {message} (y/n): {Colors.END}").lower()
        return response in ('y', 'yes', '是')


class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def calculate_hash(filepath: Path) -> str:
        """计算文件MD5哈希"""
        if not filepath.exists():
            return ""
        
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    @staticmethod
    def copy_with_backup(src: Path, dst: Path, backup_dir: Path) -> bool:
        """复制文件并创建备份"""
        try:
            # 如果目标文件存在，先备份
            if dst.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{dst.name}.{timestamp}.backup"
                backup_path = backup_dir / backup_name
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, backup_path)
                Logger.info(f"已创建备份: {backup_path}")
            
            # 确保目标目录存在
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            if src.is_file():
                shutil.copy2(src, dst)
            elif src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            
            return True
        except Exception as e:
            Logger.error(f"复制失败 {src} -> {dst}: {str(e)}")
            return False
    
    @staticmethod
    def find_config_files(patterns: List[str], base_dir: Path = None) -> List[Path]:
        """查找配置文件"""
        if base_dir is None:
            base_dir = Path.home()
        
        found_files = []
        for pattern in patterns:
            path = base_dir / pattern
            if path.exists():
                found_files.append(path)
        
        return found_files


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """加载配置"""
        if Config.CONFIG_FILE.exists():
            try:
                with open(Config.CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                Logger.error(f"加载配置失败: {str(e)}")
        
        return self.get_default_config()
    
    def save_config(self):
        """保存配置"""
        try:
            Config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(Config.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Logger.error(f"保存配置失败: {str(e)}")
            return False
    
    def get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "version": __version__,
            "sync_patterns": Config.DEFAULT_PATTERNS,
            "sync_dirs": Config.DEFAULT_DIRS,
            "exclude_patterns": [
                "*.log",
                "*.tmp",
                "*.cache",
                ".DS_Store",
                "Thumbs.db"
            ],
            "backup_enabled": True,
            "auto_sync": False,
            "sync_interval": 3600,
            "remote_url": "",
            "encryption_enabled": False,
            "last_sync": None,
            "sync_stats": {
                "total_syncs": 0,
                "files_synced": 0,
                "last_sync_time": None
            }
        }
    
    def update_config(self, key: str, value: Any):
        """更新配置项"""
        self.config[key] = value
        self.save_config()
    
    def add_sync_pattern(self, pattern: str):
        """添加同步模式"""
        if pattern not in self.config["sync_patterns"]:
            self.config["sync_patterns"].append(pattern)
            self.save_config()
    
    def remove_sync_pattern(self, pattern: str):
        """移除同步模式"""
        if pattern in self.config["sync_patterns"]:
            self.config["sync_patterns"].remove(pattern)
            self.save_config()


class SyncEngine:
    """同步引擎"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.stats = {
            "files_synced": 0,
            "files_skipped": 0,
            "files_failed": 0,
            "backups_created": 0
        }
    
    def scan_local_configs(self) -> Dict[str, List[Path]]:
        """扫描本地配置文件"""
        UI.header("🔍 扫描本地配置文件")
        
        found = {
            "files": [],
            "dirs": []
        }
        
        home = Path.home()
        
        # 扫描文件
        for pattern in self.config.config["sync_patterns"]:
            path = home / pattern
            if path.exists():
                found["files"].append(path)
                UI.info(f"发现文件: {path}")
        
        # 扫描目录
        for dir_pattern in self.config.config["sync_dirs"]:
            path = home / dir_pattern
            if path.exists():
                found["dirs"].append(path)
                UI.info(f"发现目录: {path}")
        
        UI.success(f"扫描完成: 发现 {len(found['files'])} 个文件, {len(found['dirs'])} 个目录")
        return found
    
    def create_backup(self, target_dir: Path) -> Path:
        """创建配置备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Config.BACKUP_DIR / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        UI.header(f"📦 创建备份: {backup_dir.name}")
        
        configs = self.scan_local_configs()
        
        # 备份文件
        for file_path in configs["files"]:
            try:
                dst = backup_dir / file_path.relative_to(Path.home())
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dst)
                UI.success(f"备份文件: {file_path.name}")
                self.stats["backups_created"] += 1
            except Exception as e:
                UI.error(f"备份失败 {file_path.name}: {str(e)}")
        
        # 备份目录
        for dir_path in configs["dirs"]:
            try:
                dst = backup_dir / dir_path.relative_to(Path.home())
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(dir_path, dst)
                UI.success(f"备份目录: {dir_path.name}")
            except Exception as e:
                UI.error(f"备份失败 {dir_path.name}: {str(e)}")
        
        # 保存备份清单
        manifest = {
            "timestamp": timestamp,
            "system": platform.system(),
            "user": getpass.getuser(),
            "files": [str(f.relative_to(Path.home())) for f in configs["files"]],
            "dirs": [str(d.relative_to(Path.home())) for d in configs["dirs"]]
        }
        
        with open(backup_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        UI.success(f"备份创建完成: {backup_dir}")
        return backup_dir
    
    def restore_backup(self, backup_dir: Path):
        """从备份恢复配置"""
        UI.header(f"🔄 从备份恢复: {backup_dir.name}")
        
        manifest_file = backup_dir / "manifest.json"
        if not manifest_file.exists():
            UI.error("备份清单不存在，无法恢复")
            return False
        
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            UI.error(f"读取备份清单失败: {str(e)}")
            return False
        
        home = Path.home()
        
        # 恢复文件
        for file_rel in manifest.get("files", []):
            src = backup_dir / file_rel
            dst = home / file_rel
            
            if src.exists():
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    UI.success(f"恢复文件: {file_rel}")
                except Exception as e:
                    UI.error(f"恢复失败 {file_rel}: {str(e)}")
        
        # 恢复目录
        for dir_rel in manifest.get("dirs", []):
            src = backup_dir / dir_rel
            dst = home / dir_rel
            
            if src.exists():
                try:
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    UI.success(f"恢复目录: {dir_rel}")
                except Exception as e:
                    UI.error(f"恢复失败 {dir_rel}: {str(e)}")
        
        UI.success("恢复完成!")
        return True
    
    def list_backups(self) -> List[Path]:
        """列出所有备份"""
        if not Config.BACKUP_DIR.exists():
            return []
        
        backups = []
        for item in Config.BACKUP_DIR.iterdir():
            if item.is_dir() and item.name.startswith("backup_"):
                backups.append(item)
        
        return sorted(backups, key=lambda x: x.name, reverse=True)
    
    def export_configs(self, export_path: Path) -> bool:
        """导出配置到指定路径"""
        UI.header(f"📤 导出配置到: {export_path}")
        
        try:
            if export_path.exists():
                if export_path.is_dir():
                    shutil.rmtree(export_path)
                else:
                    export_path.unlink()
            
            backup_dir = self.create_backup(export_path)
            UI.success(f"配置已导出到: {export_path}")
            return True
        except Exception as e:
            UI.error(f"导出失败: {str(e)}")
            return False
    
    def import_configs(self, import_path: Path) -> bool:
        """从指定路径导入配置"""
        UI.header(f"📥 从 {import_path} 导入配置")
        
        if not import_path.exists():
            UI.error(f"导入路径不存在: {import_path}")
            return False
        
        return self.restore_backup(import_path)
    
    def compare_configs(self, other_dir: Path) -> Dict:
        """比较配置差异"""
        UI.header(f"🔍 比较配置差异: {other_dir}")
        
        differences = {
            "only_local": [],
            "only_remote": [],
            "modified": [],
            "identical": []
        }
        
        local_configs = self.scan_local_configs()
        home = Path.home()
        
        # 比较文件
        for file_path in local_configs["files"]:
            rel_path = file_path.relative_to(home)
            other_file = other_dir / rel_path
            
            if not other_file.exists():
                differences["only_local"].append(str(rel_path))
            else:
                local_hash = FileUtils.calculate_hash(file_path)
                other_hash = FileUtils.calculate_hash(other_file)
                
                if local_hash == other_hash:
                    differences["identical"].append(str(rel_path))
                else:
                    differences["modified"].append(str(rel_path))
        
        # 检查远程独有的文件
        if (other_dir / "manifest.json").exists():
            try:
                with open(other_dir / "manifest.json", "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                
                local_files = {str(p.relative_to(home)) for p in local_configs["files"]}
                
                for file_rel in manifest.get("files", []):
                    if file_rel not in local_files:
                        differences["only_remote"].append(file_rel)
            except:
                pass
        
        return differences


class DevEnvSync:
    """主程序类"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.sync_engine = SyncEngine(self.config_manager)
    
    def run(self, args=None):
        """运行主程序"""
        parser = argparse.ArgumentParser(
            description="DevEnvSync - 智能开发环境配置同步引擎",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  %(prog)s backup                    创建配置备份
  %(prog)s restore                   从备份恢复配置
  %(prog)s list                      列出所有备份
  %(prog)s export ~/myconfigs        导出配置到指定目录
  %(prog)s import ~/myconfigs        从指定目录导入配置
  %(prog)s scan                      扫描本地配置文件
  %(prog)s config                    显示当前配置
            """
        )
        
        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__version__}"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="可用命令")
        
        # backup 命令
        backup_parser = subparsers.add_parser("backup", help="创建配置备份")
        
        # restore 命令
        restore_parser = subparsers.add_parser("restore", help="从备份恢复配置")
        restore_parser.add_argument("backup_name", nargs="?", help="备份名称")
        
        # list 命令
        list_parser = subparsers.add_parser("list", help="列出所有备份")
        
        # export 命令
        export_parser = subparsers.add_parser("export", help="导出配置")
        export_parser.add_argument("path", help="导出路径")
        
        # import 命令
        import_parser = subparsers.add_parser("import", help="导入配置")
        import_parser.add_argument("path", help="导入路径")
        
        # scan 命令
        scan_parser = subparsers.add_parser("scan", help="扫描本地配置文件")
        
        # config 命令
        config_parser = subparsers.add_parser("config", help="管理配置")
        config_parser.add_argument("--add-pattern", help="添加同步模式")
        config_parser.add_argument("--remove-pattern", help="移除同步模式")
        config_parser.add_argument("--show", action="store_true", help="显示配置")
        
        # compare 命令
        compare_parser = subparsers.add_parser("compare", help="比较配置差异")
        compare_parser.add_argument("path", help="要比较的备份路径")
        
        parsed_args = parser.parse_args(args)
        
        UI.print_banner()
        
        if not parsed_args.command:
            parser.print_help()
            return
        
        # 执行命令
        if parsed_args.command == "backup":
            self.cmd_backup()
        elif parsed_args.command == "restore":
            self.cmd_restore(parsed_args.backup_name)
        elif parsed_args.command == "list":
            self.cmd_list()
        elif parsed_args.command == "export":
            self.cmd_export(parsed_args.path)
        elif parsed_args.command == "import":
            self.cmd_import(parsed_args.path)
        elif parsed_args.command == "scan":
            self.cmd_scan()
        elif parsed_args.command == "config":
            self.cmd_config(parsed_args)
        elif parsed_args.command == "compare":
            self.cmd_compare(parsed_args.path)
    
    def cmd_backup(self):
        """备份命令"""
        backup_dir = self.sync_engine.create_backup(Config.BACKUP_DIR)
        UI.success(f"\n✨ 备份创建成功!")
        UI.info(f"备份位置: {backup_dir}")
    
    def cmd_restore(self, backup_name: Optional[str]):
        """恢复命令"""
        backups = self.sync_engine.list_backups()
        
        if not backups:
            UI.error("没有可用的备份")
            return
        
        if backup_name:
            backup_dir = Config.BACKUP_DIR / backup_name
            if not backup_dir.exists():
                UI.error(f"备份不存在: {backup_name}")
                return
        else:
            # 显示备份列表让用户选择
            UI.header("可用备份")
            for i, backup in enumerate(backups, 1):
                print(f"  {i}. {backup.name}")
            
            choice = UI.ask("请选择备份编号")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(backups):
                    backup_dir = backups[idx]
                else:
                    UI.error("无效的选择")
                    return
            except ValueError:
                UI.error("请输入有效的数字")
                return
        
        if UI.confirm(f"确定要恢复备份 {backup_dir.name} 吗? 这将覆盖现有配置"):
            self.sync_engine.restore_backup(backup_dir)
    
    def cmd_list(self):
        """列出备份命令"""
        backups = self.sync_engine.list_backups()
        
        UI.header("📋 备份列表")
        
        if not backups:
            UI.info("暂无备份")
            return
        
        for i, backup in enumerate(backups, 1):
            # 读取备份信息
            manifest_file = backup / "manifest.json"
            if manifest_file.exists():
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    timestamp = manifest.get("timestamp", "未知")
                    system = manifest.get("system", "未知")
                    files_count = len(manifest.get("files", []))
                    dirs_count = len(manifest.get("dirs", []))
                    
                    print(f"  {i}. {Colors.CYAN}{backup.name}{Colors.END}")
                    print(f"     时间: {timestamp}")
                    print(f"     系统: {system}")
                    print(f"     文件: {files_count} 个, 目录: {dirs_count} 个")
                    print()
                except:
                    print(f"  {i}. {backup.name} (无法读取信息)")
            else:
                print(f"  {i}. {backup.name}")
    
    def cmd_export(self, path: str):
        """导出命令"""
        export_path = Path(path).expanduser().resolve()
        self.sync_engine.export_configs(export_path)
    
    def cmd_import(self, path: str):
        """导入命令"""
        import_path = Path(path).expanduser().resolve()
        
        if UI.confirm(f"确定要从 {import_path} 导入配置吗? 这将覆盖现有配置"):
            self.sync_engine.import_configs(import_path)
    
    def cmd_scan(self):
        """扫描命令"""
        self.sync_engine.scan_local_configs()
    
    def cmd_config(self, args):
        """配置命令"""
        if args.add_pattern:
            self.config_manager.add_sync_pattern(args.add_pattern)
            UI.success(f"已添加同步模式: {args.add_pattern}")
        
        elif args.remove_pattern:
            self.config_manager.remove_sync_pattern(args.remove_pattern)
            UI.success(f"已移除同步模式: {args.remove_pattern}")
        
        else:
            # 显示配置
            UI.header("⚙️  当前配置")
            print(json.dumps(self.config_manager.config, indent=2, ensure_ascii=False))
    
    def cmd_compare(self, path: str):
        """比较命令"""
        compare_path = Path(path).expanduser().resolve()
        differences = self.sync_engine.compare_configs(compare_path)
        
        UI.header("📊 比较结果")
        
        if differences["only_local"]:
            print(f"\n{Colors.GREEN}仅本地存在:{Colors.END}")
            for f in differences["only_local"]:
                print(f"  + {f}")
        
        if differences["only_remote"]:
            print(f"\n{Colors.BLUE}仅远程存在:{Colors.END}")
            for f in differences["only_remote"]:
                print(f"  - {f}")
        
        if differences["modified"]:
            print(f"\n{Colors.WARNING}已修改:{Colors.END}")
            for f in differences["modified"]:
                print(f"  ~ {f}")
        
        if differences["identical"]:
            print(f"\n{Colors.CYAN}完全一致:{Colors.END}")
            print(f"  共 {len(differences['identical'])} 个文件")


def main():
    """程序入口"""
    try:
        app = DevEnvSync()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  操作已取消{Colors.END}")
        sys.exit(0)
    except Exception as e:
        UI.error(f"程序错误: {str(e)}")
        Logger.error(f"程序错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
