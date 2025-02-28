#!/usr/bin/env python3
"""設定タブにデバッグロギング追加"""

import os

def add_logging_to_settings_tab():
    """設定タブにロギングを追加"""
    settings_file = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    if not os.path.exists(settings_file):
        print(f"エラー: {settings_file}が見つかりません")
        return False
    
    # バックアップ作成
    backup_file = f"{settings_file}.debug.bak"
    with open(settings_file, 'r') as src:
        with open(backup_file, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ作成: {backup_file}")
    
    # ファイル読み込み
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # ログインポート追加
    if "import logging" not in content:
        if "import" in content:
            first_import = content.find("import")
            content = content[:first_import] + "import logging\nimport traceback\n" + content[first_import:]
        else:
            content = "import logging\nimport traceback\n" + content
    
    # クリックイベント接続を確認
    if "self.add_tab_btn.clicked.connect(self.add_new_tab)" not in content:
        # イベント接続の位置を探す
        event_pos = content.find("# イベント接続")
        if event_pos < 0:
            event_pos = content.find(".clicked.connect")
        
        if event_pos > 0:
            # 段落の終わりを見つける
            paragraph_end = content.find("\n\n", event_pos)
            if paragraph_end < 0:
                paragraph_end = content.find("def ", event_pos)
            if paragraph_end < 0:
                paragraph_end = len(content)
            
            # コード挿入
            tab_connect = "\n        # 新規タブ追加ボタン接続\n        self.add_tab_btn.clicked.connect(self.add_new_tab)"
            content = content[:paragraph_end] + tab_connect + content[paragraph_end:]
    
    # add_new_tabメソッドが存在するか確認
    if "def add_new_tab" not in content:
        # クラス終了位置を探す
        class_end = content.find("if __name__")
        if class_end < 0:
            class_end = len(content)
        
        # メソッド追加
        add_new_tab_method = """
    def add_new_tab(self):
        """新規タブを追加"""
        print("===== 新規タブ追加メソッドが実行されました =====")
        try:
            # 選択カテゴリーを確認
            current_item = self.category_tree.currentItem()
            print(f"選択項目: {current_item}")
            
            if not current_item:
                print("カテゴリーが選択されていません")
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "タブにするカテゴリーを選択してください")
                return
            
            # カテゴリーであることを確認
            if current_item.parent():
                print("選択項目はカテゴリーではなくスキルです")
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "警告", "カテゴリーのみタブに変換できます")
                return
            
            # カテゴリー名を取得
            category_name = current_item.text(0)
            print(f"カテゴリー名: {category_name}")
            
            # メインウィンドウを取得
            print("メインウィンドウを取得中...")
            main_window = self
            while main_window.parent():
                main_window = main_window.parent()
                print(f"親ウィンドウ: {main_window}")
            
            # タブ追加メソッドを呼び出す
            print(f"メインウィンドウはadd_category_tabメソッドを持っていますか？: {hasattr(main_window, 'add_category_tab')}")
            if hasattr(main_window, "add_category_tab"):
                print(f"add_category_tabメソッドを呼び出します: {category_name}")
                result = main_window.add_category_tab(category_name)
                print(f"メソッド呼び出し結果: {result}")
                
                if result:
                    from PyQt5.QtWidgets import QMessageBox
                    print(f"成功: 新規タブ「{category_name}」を追加しました")
                    QMessageBox.information(self, "成功", f"新規タブ「{category_name}」を追加しました")
            else:
                from PyQt5.QtWidgets import QMessageBox
                print("エラー: タブ追加機能が見つかりません")
                QMessageBox.warning(self, "エラー", "タブ追加機能が見つかりません")
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            print(f"エラーが発生しました: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"タブ追加中にエラーが発生しました: {str(e)}")
"""
        
        # Pythonの文字列リテラル修正（docstringエスケープ）
        add_new_tab_method = add_new_tab_method.replace('"""新規タブを追加"""', '\"\"\"新規タブを追加\"\"\"')
        
        # メソッド追加
        content = content[:class_end] + add_new_tab_method + content[class_end:]
    
    # 結果を保存
    with open(settings_file, 'w') as f:
        f.write(content)
    
    print(f"{settings_file}にロギングとadd_new_tabメソッドを追加しました")
    return True

if __name__ == "__main__":
    add_logging_to_settings_tab()
