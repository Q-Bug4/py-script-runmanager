from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置关键字高亮格式
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#0000FF"))
        self.keyword_format.setFontWeight(700)
        
        # Python关键字
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield'
        ]
    
    def highlightBlock(self, text):
        for word in text.split():
            if word in self.keywords:
                index = text.index(word)
                self.setFormat(index, len(word), self.keyword_format)

class ScriptEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 创建编辑器
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 12))
        self.layout.addWidget(self.editor)
        
        # 设置语法高亮
        self.highlighter = PythonHighlighter(self.editor.document())
    
    def get_content(self) -> str:
        return self.editor.toPlainText()
    
    def set_content(self, content: str):
        self.editor.setPlainText(content) 