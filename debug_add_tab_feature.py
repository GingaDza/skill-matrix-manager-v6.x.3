#!/usr/bin/env python3
"""タブ追加機能のデバッグ"""

import os
import traceback

def add_debug_code():
    """デバッグコードを追加"""
    # 設定タブファイル
    settings_file = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    # メインウィンドウファイル
    main_window_file = "src/skill_matrix_manager/ui/main_window.py"
    
    # 両方のファイルが存在するか確認
    for file_path in [settings_file, main_window_file]:
        if not os.path.exists(file_path):
            print(f"エラー: {file_path}が見つかりません")
            return False
    
    # 設定タブにデバッグコードを追加
    add_debug_to_settings_tab(settings_file)
    
    # メインウィンドウにデバッグコードを追加
    add_debug_to_main_window(main_window_file)
    
    print("デバッグコードを追加しました")
    return True

def add_debug_to_settings_tab(filepath):
    """設定タブにデバッグログを追加"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # add_new_tabメソッド内にデバッグ出力を追加
    if "def add_new_tab" in content:
        # メソッド全体を探す
        method_start = content.find("def add_new_tab")
        method_end = content.find("def ", method_start + 1)
        if method_end == -1:  # 最後のメソッドの場合
            method_end = len(content)
        
        method_content = content[method_start:method_end]
        
        # デバッグ出力を追加
        debug_method = method_content.replace(
            "def add_new_tab(self):", 
            "def add_new_tab(self):\n        print(\"=== 新規タブ追加メソッドが呼び出されました ====\")"
        )
        
        debug_method = debug_method.replace(
            "try:", 
            "try:\n            print(\"新規タブ追加の処理を開始します\")"
        )
        
        debug_method = debug_method.replace(
            "current_item = self.category_tree.currentItem()", 
            "current_item = self.category_tree.currentItem()\n            print(f\"選択項目: {current_item}\")"
        )
        
        debug_method = debug_method.replace(
            "category_name = current_item.text(0)", 
            "category_name = current_item.text(0)\n            print(f\"カテゴリー名: {category_name}\")"
        )
        
        debug_method = debug_method.replace(
            "main_window = self", 
            "main_window = self\n            print(\"メインウィンドウの参照を取得中\")"
        )
        
        debug_method = debug_method.replace(
            "if hasattr(main_window, \"add_category_tab\"):", 
            "print(f\"メインウィンドウは add_category_tab メソッドを持っていますか？: {hasattr(main_window, 'add_category_tab')}\")\n            if hasattr(main_window, \"add_category_tab\"):"
        )
        
        debug_method = debug_method.replace(
            "except Exception as e:", 
            "except Exception as e:\n            print(f\"エラーが発生しました: {e}\")\n            traceback.print_exc()"
        )
        
        # メソッドを置換
        content = content[:method_start] + debug_method + content[method_end:]
        
        # traceback モジュールのインポートを追加
        if "import traceback" not in content:
            first_line = content.find("\n")
            content = content[:first_line+1] + "import traceback\n" + content[first_line+1:]
    else:
        # メソッドがなければ追加
        class_end = content.find("if __name__")
        if class_end == -1:
            class_end = len(content)
        
        debug_method = """
    def add_new_tab(self):
        \"\"\"新規タブを追加\"\"\"
        print("=== 新規タブ追加メソッドが呼び出されました ===")
        try:
            print("新規タブ追加の処理を開始します")
            # 選択カテゴリーを確認
            current_item = self.category_tree.currentItem()
            print(f"選択項目: {current_item}")
            if not current_item:
                print("選択項目がありません")
                QMessageBox.warning(self, "警告", "タブにするカテゴリーを選択してください")
                return
            
            # カテゴリーであることを確認（親がない=トップレベル項目）
            if current_item.parent():
                print("選択項目はカテゴリーではなくスキルです")
                QMessageBox.warning(self, "警告", "カテゴリーのみタブに変換できます")
                return
            
            # カテゴリー名を取得
            category_name = current_item.text(0)
            print(f"カテゴリー名: {category_name}")
            
            # メインウィンドウの参照を取得
            main_window = self
            print("メインウィンドウの参照を取得中")
            while main_window.parent():
                main_window = main_window.parent()
                print(f"親ウィンドウ: {main_window}")
            
            # タブ追加メソッドを呼び出す
            print(f"メインウィンドウは add_category_tab メソッドを持っていますか？: {hasattr(main_window, 'add_category_tab')}")
            if hasattr(main_window, "add_category_tab"):
                print("add_category_tabメソッドを呼び出します")
                result = main_window.add_category_tab(category_name)
                print(f"メソッド呼び出し結果: {result}")
                if result:
                    QMessageBox.information(self, "成功", f"新規タブ「{category_name}」を追加しました")
            else:
                print("add_category_tabメソッドがありません")
                QMessageBox.warning(self, "エラー", "タブ追加機能が見つかりません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"タブ追加中にエラーが発生しました: {str(e)}")
"""
        
        # traceback モジュールのインポートを追加
        if "import traceback" not in content:
            first_line = content.find("\n")
            content = content[:first_line+1] + "import traceback\n" + content[first_line+1:]
        
        content = content[:class_end] + debug_method + content[class_end:]
    
    # 結果を保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にデバッグコードを追加しました")

def add_debug_to_main_window(filepath):
    """メインウィンドウにデバッグログを追加"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # add_category_tabメソッド内にデバッグ出力を追加
    if "def add_category_tab" in content:
        # メソッド全体を探す
        method_start = content.find("def add_category_tab")
        method_end = content.find("def ", method_start + 1)
        if method_end == -1:  # 最後のメソッドの場合
            method_end = len(content)
        
        method_content = content[method_start:method_end]
        
        # デバッグ出力を追加
        debug_method = method_content.replace(
            "def add_category_tab(self, category_name):", 
            "def add_category_tab(self, category_name):\n        print(f\"=== add_category_tab メソッドが呼び出されました: {category_name} ====\")"
        )
        
        # メソッドを置換
        content = content[:method_start] + debug_method + content[method_end:]
    else:
        # メソッドがなければ追加
        class_end = content.find("if __name__")
        if class_end == -1:
            class_end = len(content)
        
        debug_method = """
    def add_category_tab(self, category_name):
        \"\"\"カテゴリータブを追加\"\"\"
        print(f"=== add_category_tab メソッドが呼び出されました: {category_name} ====")
        # 既存タブ確認
        print(f"タブ数: {self.tabs.count()}")
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
        \"\"\"タブ設定を保存\"\"\"
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
        
        content = content[:class_end] + debug_method + content[class_end:]
    
    # 結果を保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にデバッグコードを追加しました")

if __name__ == "__main__":
    add_debug_code()
