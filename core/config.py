import json
import os
from typing import Dict, Any
from utils.logger import get_logger
from utils.file_utils import ensure_directory, read_file, write_file

logger = get_logger(__name__)

class Config:
    def __init__(self):
        self.config_dir = "config"
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.user_config_file = os.path.join(self.config_dir, "user_config.json")
        
        ensure_directory(self.config_dir)
        self._load_configs()
    
    def _load_configs(self):
        """加载配置文件"""
        # 系统配置默认值
        self.system_config = {
            "database_url": "sqlite:///script_manager.db",
            "scripts_dir": "scripts",
            "logs_dir": "logs",
            "max_execution_time": 3600,
            "max_output_size": 1048576,
            "supported_script_types": ["python", "nodejs", "shell"]
        }
        
        # 用户配置默认值
        self.user_config = {
            "theme": "light",
            "editor_font_size": 12,
            "editor_font_family": "Consolas",
            "show_line_numbers": True,
            "auto_save": True,
            "default_script_type": "python"
        }
        
        # 加载保存的配置
        try:
            if os.path.exists(self.config_file):
                saved_config = json.loads(read_file(self.config_file))
                self.system_config.update(saved_config)
            
            if os.path.exists(self.user_config_file):
                saved_user_config = json.loads(read_file(self.user_config_file))
                self.user_config.update(saved_user_config)
                
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
    
    def get_system_config(self, key: str, default: Any = None) -> Any:
        """获取系统配置"""
        return self.system_config.get(key, default)
    
    def get_user_config(self, key: str, default: Any = None) -> Any:
        """获取用户配置"""
        return self.user_config.get(key, default)
    
    def update_system_config(self, updates: Dict[str, Any]):
        """更新系统配置"""
        try:
            self.system_config.update(updates)
            write_file(self.config_file, json.dumps(self.system_config, indent=4))
            logger.info("Updated system config")
        except Exception as e:
            logger.error(f"Failed to update system config: {str(e)}")
            raise
    
    def update_user_config(self, updates: Dict[str, Any]):
        """更新用户配置"""
        try:
            self.user_config.update(updates)
            write_file(self.user_config_file, json.dumps(self.user_config, indent=4))
            logger.info("Updated user config")
        except Exception as e:
            logger.error(f"Failed to update user config: {str(e)}")
            raise
    
    def reset_system_config(self):
        """重置系统配置"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self._load_configs()
    
    def reset_user_config(self):
        """重置用户配置"""
        if os.path.exists(self.user_config_file):
            os.remove(self.user_config_file)
        self._load_configs() 