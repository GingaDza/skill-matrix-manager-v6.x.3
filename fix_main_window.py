#!/usr/bin/env python3
"""メインウィンドウにタブ追加機能を実装"""

import os

def backup_file(filepath):
    """バックアップ作成"""
    if os.path.exists(filepath):
        backup = filepath + ".bak"
        with open(filepath, 'r') as src:
            with open(backup, 'w') as dst:
                dst.write(src.read())
        print(f"バックアップ: {backup}")

def add_tab_feature():
    """タブ追加機能を実装"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup_file(filepath)
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # jsonのインポート追加
    if "import json" not in content:
        first_import = content.find("import")
        content = content[:first_import] + "import json\n" + content[first_import:]
    
    # タブ追加メソッド実装
    if "def add_category_tab" not in content:
        # クラス終了位置を探す
        class_end = content.find("if __name__")
        if class_end < 0:
            class_end = len(content)
        
        # メソッド追加
        new_methods = """
    def add_category_tab(self, category_name):
        """カテゴリータブを追加"""
        # 同名タブ確認
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == category_name:
                self.tabs.setCurrentIndex(i)
                return True
        
        # 新タブ作成
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel(f"{category_name}タブの内容")
        layout.addWidget(label)
        
        # タブ追加
        self.tabs.addTab(tab, category_name)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        
        # 設定保存
        self._save_tab_config()
        return True
    
    def _save_tab_config(self):
        """タブ設定を保存"""
        try:
            tabs = []
            for i in range(self.tabs.count()):
                tabs.append({
                    "name": self.tabs.tabText(i),
                    "type": "category"
                })
            
            with open("tab_config.json", "w") as f:
                json.dump({"tabs": tabs}, f, indent=2)
        except Exception as e:
            print(f"設定保存エラー: {e}")
"""
        
        # Pythonのdocstringをエスケープ
        new_methods = new_methods.replace('"""カテゴリータブを追加"""', '\"\"\"カテゴリータブを追加\"\"\"')
        new_methods = new_methods.replace('"""タブ設定を保存"""', '\"\"\"タブ設定を保存\"\"\"')
        
        # メソッド追加
        content = content[:class_end] + new_methods + content[class_end:]
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にタブ追加機能を実装しました")
    return True

if __name__ == "__main__":
    add_tab_feature()
