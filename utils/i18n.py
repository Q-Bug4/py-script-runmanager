from PyQt6.QtCore import QObject
import json
import os
from core.config import Config

class I18n(QObject):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.current_language = self._get_language()
        self.translations = self._load_translations()
    
    def _get_language(self):
        """获取当前语言设置"""
        language = self.config.user_config.get("language", "auto")
        if language == "auto":
            import locale
            system_lang = locale.getdefaultlocale()[0]
            return "zh-CN" if system_lang.startswith("zh") else "en"
        return language
    
    def _load_translations(self):
        """加载翻译文件"""
        translations = {}
        # 获取项目根目录的绝对路径
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        translations_dir = os.path.join(root_dir, "translations")
        
        # 确保translations目录存在
        if not os.path.exists(translations_dir):
            os.makedirs(translations_dir)
        
        # 加载所有语言的翻译
        for lang in ["en", "zh-CN"]:
            file_path = os.path.join(translations_dir, f"{lang}.json")
            try:
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        translations[lang] = json.load(f)
                else:
                    print(f"Warning: Translation file not found: {file_path}")
                    translations[lang] = {}
            except Exception as e:
                print(f"Warning: Failed to load translation file {file_path}: {str(e)}")
                translations[lang] = {}
        
        return translations
    
    def tr(self, text: str) -> str:
        """翻译文本"""
        if self.current_language == "zh-CN":
            return text
        return self.translations.get(self.current_language, {}).get(text, text)
    
    def change_language(self, language: str):
        """更改语言设置"""
        self.config.user_config["language"] = language
        self.config.save_user_config()
        self.current_language = language 