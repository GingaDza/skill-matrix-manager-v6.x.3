#!/usr/bin/env python3
"""設定タブにタブ追加メソッドを実装"""

import os

def fix_settings_tab():
    """設定タブにタブ追加メソッドを実装"""
    filepath = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
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
    
    # add_new_tabメソッドがなければ追加
    if "def add_new_tab" not in content:
        # クラス定義の終わりを探す
        class_end = content.find("if __name__")
        if class_end < 0:
            # if __name__がない場合はファイルの最後
            class_end = len(content)
        
        # メソッドを追加
        new_method = """
    def add_new_tab(self):
        """新規タブを追加"""
        try:
            # 選択カテゴリーを確認
            current_item = self.category_tree.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "タブにするカテゴリーを選択してください")
                return
            
            # カテゴリーであることを確認（親がない=トップレベル項目）
            if current_item.parent():
                QMessageBox.warning(self, "警告", "カテゴリーのみタブに変換できます")
                return
            
            # カテゴリー名を取得
            category_name = current_item.text(0)
            
            # メインウィンドウの参照を取得
            main_window = self
            while main_window.parent():
                main_window = main_window.parent()
            
            # タブ追加メソッドを呼び出す
            if hasattr(main_window, "add_category_tab"):
                result = main_window.add_category_tab(category_name)
                if result:
                    QMessageBox.information(self, "成功", f"新規タブ「{category_name}」を追加しました")
            else:
                QMessageBox.warning(self, "エラー", "タブ追加機能が見つかりません")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"タブ追加中にエラーが発生しました: {str(e)}")
"""
        
        # Pythonの文字列リテラル修正（docstringエスケープ）
        new_method = new_method.replace('"""新規タブを追加"""', '\"\"\"新規タブを追加\"\"\"')
        
        # メソッド追加
        content = content[:class_end] + new_method + content[class_end:]
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にタブ追加メソッドを実装しました")
    return True

if __name__ == "__main__":
    fix_settings_tab()
