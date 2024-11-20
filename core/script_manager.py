import os
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import Script, ScriptParameter, User
from utils.logger import get_logger
from utils.file_utils import ensure_directory, read_file, write_file

logger = get_logger(__name__)

class ScriptManager:
    def __init__(self, db: Session):
        self.db = db
        self.scripts_dir = "scripts"
        ensure_directory(self.scripts_dir)
    
    def create_script(self, name: str, content: str, script_type: str,
                     description: str = "", user_id: int = None) -> Script:
        """创建新脚本"""
        try:
            script = Script(
                name=name,
                content=content,
                type=script_type,
                description=description,
                user_id=user_id
            )
            self.db.add(script)
            self.db.commit()
            self.db.refresh(script)
            
            # 保存脚本文件
            file_path = self._get_script_path(script)
            write_file(file_path, content)
            
            logger.info(f"Created script: {name}")
            return script
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create script: {str(e)}")
            raise
    
    def update_script(self, script_id: int, content: str,
                     name: Optional[str] = None,
                     description: Optional[str] = None) -> Script:
        """更新脚本"""
        try:
            script = self.db.query(Script).get(script_id)
            if not script:
                raise ValueError(f"Script {script_id} not found")
            
            if name:
                script.name = name
            if description:
                script.description = description
            
            script.content = content
            script.updated_at = datetime.now()
            
            self.db.commit()
            
            # 更新脚本文件
            file_path = self._get_script_path(script)
            write_file(file_path, content)
            
            logger.info(f"Updated script: {script_id}")
            return script
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update script: {str(e)}")
            raise
    
    def delete_script(self, script_id: int):
        """删除脚本"""
        try:
            script = self.db.query(Script).get(script_id)
            if not script:
                raise ValueError(f"Script {script_id} not found")
            
            # 删除脚本文件
            file_path = self._get_script_path(script)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            self.db.delete(script)
            self.db.commit()
            
            logger.info(f"Deleted script: {script_id}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete script: {str(e)}")
            raise
    
    def get_script(self, script_id: int) -> Optional[Script]:
        """获取脚本详情"""
        return self.db.query(Script).get(script_id)
    
    def get_scripts(self, user_id: Optional[int] = None,
                   script_type: Optional[str] = None) -> List[Script]:
        """获取脚本列表"""
        query = self.db.query(Script)
        if user_id:
            query = query.filter(Script.user_id == user_id)
        if script_type:
            query = query.filter(Script.type == script_type)
        return query.all()
    
    def add_parameter(self, script_id: int, name: str,
                     description: str = "", default_value: str = "",
                     param_type: str = "string") -> ScriptParameter:
        """添加脚本参数"""
        try:
            param = ScriptParameter(
                script_id=script_id,
                name=name,
                description=description,
                default_value=default_value,
                parameter_type=param_type
            )
            self.db.add(param)
            self.db.commit()
            self.db.refresh(param)
            
            logger.info(f"Added parameter {name} to script {script_id}")
            return param
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to add parameter: {str(e)}")
            raise
    
    def _get_script_path(self, script: Script) -> str:
        """获取脚本文件路径"""
        extension = {
            "python": ".py",
            "nodejs": ".js",
            "shell": ".sh"
        }.get(script.type, ".txt")
        
        return os.path.join(self.scripts_dir, f"{script.id}{extension}") 