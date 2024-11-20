import os
import signal
import subprocess
import threading
import time
from typing import Optional, Dict, Callable
from datetime import datetime
from database.models import ScriptExecution
from utils.logger import get_logger

logger = get_logger(__name__)

class ScriptExecutor:
    def __init__(self, db_session):
        self.db = db_session
        self.running_processes = {}
        self.output_callbacks = {}
    
    def execute(self, script_id: int, content: str,
                parameters: Dict[str, str] = None,
                timeout: int = 3600,
                output_callback: Optional[Callable[[str], None]] = None) -> int:
        """
        执行脚本
        
        Args:
            script_id: 脚本ID
            content: 脚本内容
            parameters: 脚本参数
            timeout: 超时时间（秒）
            output_callback: 输出回调函数
        
        Returns:
            execution_id: 执行记录ID
        """
        try:
            # 创建执行记录
            execution = ScriptExecution(
                script_id=script_id,
                status="running"
            )
            self.db.add(execution)
            self.db.commit()
            self.db.refresh(execution)
            
            # 设置环境变量
            env = os.environ.copy()
            if parameters:
                env.update(parameters)
            
            # 启动进程
            process = subprocess.Popen(
                ["python", "-c", content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 记录进程信息
            self.running_processes[execution.id] = process
            if output_callback:
                self.output_callbacks[execution.id] = output_callback
            
            # 启动监控线程
            monitor_thread = threading.Thread(
                target=self._monitor_execution,
                args=(execution.id, process, timeout)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            logger.info(f"Started execution {execution.id} for script {script_id}")
            return execution.id
            
        except Exception as e:
            logger.error(f"Failed to execute script: {str(e)}")
            if execution:
                execution.status = "failed"
                execution.error = str(e)
                execution.finished_at = datetime.now()
                self.db.commit()
            raise
    
    def stop_execution(self, execution_id: int):
        """停止脚本执行"""
        process = self.running_processes.get(execution_id)
        if process:
            try:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
                
                logger.info(f"Stopped execution {execution_id}")
            except Exception as e:
                logger.error(f"Failed to stop execution {execution_id}: {str(e)}")
    
    def _monitor_execution(self, execution_id: int,
                          process: subprocess.Popen,
                          timeout: int):
        """监控脚本执行"""
        output = []
        error_output = []
        
        def read_output():
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                output.append(line)
                callback = self.output_callbacks.get(execution_id)
                if callback:
                    callback(line)
        
        def read_error():
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                error_output.append(line)
                callback = self.output_callbacks.get(execution_id)
                if callback:
                    callback(f"ERROR: {line}")
        
        # 启动输出读取线程
        stdout_thread = threading.Thread(target=read_output)
        stderr_thread = threading.Thread(target=read_error)
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        try:
            # 等待进程完成或超时
            return_code = process.wait(timeout=timeout)
            
            # 更新执行记录
            execution = self.db.query(ScriptExecution).get(execution_id)
            execution.finished_at = datetime.now()
            execution.output = "".join(output)
            execution.error = "".join(error_output)
            
            if return_code == 0:
                execution.status = "completed"
            else:
                execution.status = "failed"
            
            self.db.commit()
            logger.info(f"Execution {execution_id} finished with status {execution.status}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            execution = self.db.query(ScriptExecution).get(execution_id)
            execution.status = "timeout"
            execution.finished_at = datetime.now()
            execution.output = "".join(output)
            execution.error = "Execution timeout"
            self.db.commit()
            logger.warning(f"Execution {execution_id} timeout")
        
        finally:
            # 清理资源
            self.running_processes.pop(execution_id, None)
            self.output_callbacks.pop(execution_id, None) 