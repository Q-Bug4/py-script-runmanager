import logging
import os
from datetime import datetime

def setup_logger():
    """设置日志系统"""
    # 创建日志目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件名
    log_file = os.path.join(log_dir, f"script_manager_{datetime.now().strftime('%Y%m%d')}.log")
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def get_logger(name):
    """获取指定名称的日志记录器"""
    return logging.getLogger(name) 