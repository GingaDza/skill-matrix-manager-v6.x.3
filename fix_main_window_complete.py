#!/usr/bin/env python3
"""メインウィンドウにタブ追加機能を完全実装"""

import os

def fix_main_window():
    """メインウィンドウにタブ追加機能を実装"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup = filepath + ".complete.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ: {backup}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. jsonモジュールのインポートを追加
    if "import json" not in content:
        # 他のインポートを探す
        import_section = content.find("import")
        if import_section >= 0:
            # 最初のインポート行の前に追加
            content = content[:import_section] + "import json\n" + content[import_section:]
    
    # 2. add_category_tabメソッドとsave_tab_configメソッドを追加
    if "def add_category_tab" not in content:
        # クラス定義の終わりを探す
        class_end = content.find("if __name__")
        if class_end < 0:
            # if __name__がない場合はファイルの最後
            class_end = len(content)
        
        # メソッドを追加
        new_methods = """
    def add_category_tab(self, category_name):
        """カテゴリータブを追加"""
        # 既存タブ確認
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == category_name:
                self.tabs.setCurrentIndex(i)
                return True
        
        # 新規タブ作成
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        label = QLabel(f"{category_name}タブの内容")
        layout.addWidget(label)
        
        # タブに追加
        self.tabs.addTab(new_tab, category_name)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        
        # 設定保存
        self._save_tab_config()
        return True
    
    def _save_tab_config(self):
        """タブ設定を保存"""
        try:
            tabs = []
            for i in range(self.tabs.count()):
                tab_name = self.tabs.tabText(i)
                tabs.append({"name": tab_name, "type": "category"})
            
            with open("tab_config.json", "w", encoding="utf-8") as f:
                json.dump({"tabs": tabs}, f, ensure_ascii=False, indent=2)
            print("タブ設定を保存しました")
        except Exception as e:
            print(f"タブ設定保存エラー: {e}")
"""
        
        # Pythonの文字列リテラル修正（docstringエスケープ）
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
    fix_main_window()
