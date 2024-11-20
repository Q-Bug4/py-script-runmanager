from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess
import sys

class ExecutionPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 创建输出显示区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)
        
        # 清除按钮
        self.clear_button = QPushButton("清除输出")
        self.clear_button.clicked.connect(self.clear_output)
        self.layout.addWidget(self.clear_button)
        
        # 进程对象
        self.process = None
    
    def run_script(self, content: str):
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_output)
            self.process.readyReadStandardError.connect(self.handle_error)
            self.process.finished.connect(self.handle_finished)
        
        self.output_text.clear()
        self.output_text.append("开始执行脚本...\n")
        
        # 将脚本内容写入临时文件
        with open("temp_script.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        # 使用Python解释器执行脚本
        self.process.start(sys.executable, ["temp_script.py"])
    
    def handle_output(self):
        output = bytes(self.process.readAllStandardOutput()).decode()
        self.output_text.append(output)
    
    def handle_error(self):
        error = bytes(self.process.readAllStandardError()).decode()
        self.output_text.append(f"错误：{error}")
    
    def handle_finished(self, exit_code, exit_status):
        self.output_text.append(f"\n脚本执行{'成功' if exit_code == 0 else '失败'}")
        self.process = None
    
    def clear_output(self):
        self.output_text.clear()