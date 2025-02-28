#!/usr/bin/env python3
"""メインウィンドウにデバッグロギング追加"""

import os

def add_category_tab_method():
    """メインウィンドウにadd_category_tabメソッドを確実に追加"""
    main_file = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(main_file):
        print(f"エラー: {main_file}が見つかりません")
        return False
    
    # バックアップ作成
    backup_file = f"{main_file}.method.bak"
    with open(main_file, 'r') as src:
        with open(backup_file, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ作成: {backup_file}")
    
    # ファイル読み込み
    with open(main_file, 'r') as f:
        content = f.read()
    
    # jsonモジュールをインポート
    if "import json" not in content:
        first_import = content.find("import")
        if first_import >= 0:
            content = content[:first_import] + "import json\n" + content[first_import:]
        else:
            content = "import json\n" + content
    
    # add_category_tabメソッドが存在するか確認
    if "def add_category_tab" not in content:
        # クラス終了位置を探す
        class_end = content.find("if __name__")
        if class_end < 0:
            class_end = len(content)
        
        # メソッド追加
        add_tab_method = """
    def add_category_tab(self, category_name):
        """カテゴリータブを追加"""
        print(f"===== add_category_tab メソッドが呼び出されました: {category_name} =====")
        
        # 既存タブ確認
        print(f"現在のタブ数: {self.tabs.count()}")
        for i in range(self.tabs.count()):
            tab_name = self.tabs.tabText(i)
            print(f"タブ {i}: {tab_name}")
            if tab_name == category_name:
                print(f"同名のタブが既に存在します: {category_name}")
                self.tabs.setCurrentIndex(i)
                return True
        
        # 新規タブ作成
        print("新規タブを作成します")
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        label = QLabel(f"{category_name}タブの内容")
        layout.addWidget(label)
        
        # タブに追加
        print("タブを追加します")
        self.tabs.addTab(new_tab, category_name)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        
        # 設定保存
        print("設定を保存します")
        self._save_tab_config()
        return True
    
    def _save_tab_config(self):
        """タブ設定を保存"""
        try:
            tabs = []
            for i in range(self.tabs.count()):
                tab_name = self.tabs.tabText(i)
                tabs.append({"name": tab_name, "type": "category"})
            
            print(f"保存するタブ設定: {tabs}")
            with open("tab_config.json", "w", encoding="utf-8") as f:
                json.dump({"tabs": tabs}, f, ensure_ascii=False, indent=2)
            print("タブ設定を保存しました")
        except Exception as e:
            print(f"タブ設定保存エラー: {e}")
            import traceback
            traceback.print_exc()
"""
        
        # Pythonの文字列リテラル修正（docstringエスケープ）
        add_tab_method = add_tab_method.replace('"""カテゴリータブを追加"""', '\"\"\"カテゴリータブを追加\"\"\"')
        add_tab_method = add_tab_method.replace('"""タブ設定を保存"""', '\"\"\"タブ設定を保存\"\"\"')
        
        # メソッド追加
        content = content[:class_end] + add_tab_method + content[class_end:]
    
    # 結果を保存
    with open(main_file, 'w') as f:
        f.write(content)
    
    print(f"{main_file}にadd_category_tabメソッドを追加しました")
    return True

if __name__ == "__main__":
    add_category_tab_method()
