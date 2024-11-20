from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                           QPushButton, QInputDialog)
from PyQt6.QtCore import pyqtSignal
from database.db_manager import get_db
from database.models import Script

class ScriptListWidget(QWidget):
    script_selected = pyqtSignal(int)  # 发送选中的脚本ID
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # 创建树形视图
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("脚本列表")
        self.layout.addWidget(self.tree)
        
        # 添加按钮
        self.add_button = QPushButton("添加脚本")
        self.layout.addWidget(self.add_button)
        
        # 连接信号
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)
        self.add_button.clicked.connect(self.add_script)
        
        # 加载脚本列表
        self.load_scripts()
    
    def load_scripts(self):
        self.tree.clear()
        
        # 创建脚本类型的根节点
        python_root = QTreeWidgetItem(self.tree, ["Python脚本"])
        node_root = QTreeWidgetItem(self.tree, ["Node.js脚本"])
        shell_root = QTreeWidgetItem(self.tree, ["Shell脚本"])
        
        # 从数据库加载脚本
        db = next(get_db())
        scripts = db.query(Script).all()
        
        # 将脚本添加到对应类型的节点下
        for script in scripts:
            if script.type == "python":
                parent = python_root
            elif script.type == "nodejs":
                parent = node_root
            else:
                parent = shell_root
            
            item = QTreeWidgetItem(parent, [script.name])
            item.setData(0, Qt.ItemDataRole.UserRole, script.id)
    
    def on_selection_changed(self):
        items = self.tree.selectedItems()
        if items and items[0].parent():  # 确保选中的是脚本而不是类型节点
            script_id = items[0].data(0, Qt.ItemDataRole.UserRole)
            self.script_selected.emit(script_id)
    
    def add_script(self):
        name, ok = QInputDialog.getText(self, "添加脚本", "请输入脚本名称：")
        if ok and name:
            # TODO: 打开新建脚本对话框
            self.load_scripts()  # 重新加载列表 