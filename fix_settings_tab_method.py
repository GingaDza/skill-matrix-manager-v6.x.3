#!/usr/bin/env python3
"""設定タブのメソッドを修正"""

import os

def add_method_to_settings():
    """設定タブにメソッドを追加"""
    filepath = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイルを読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # メソッドを追加
    if "def add_new_tab" not in content:
        # 最後のメソッドを見つける
        last_def = content.rfind("def ")
        
        # クラスの終わりを見つける
        if "if __name__" in content:
            class_end = content.find("if __name__", last_def)
        else:
            class_end = len(content)
        
        # メソッドを追加
        method = """
    def add_new_tab(self):
        \"\"\"新規タブを追加\"\"\"
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
        
        content = content[:class_end] + method + content[class_end:]
        
        # 保存
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"{filepath}にメソッドを追加しました")
    else:
        print(f"{filepath}にはすでにメソッドが存在します")
    
    return True

if __name__ == "__main__":
    add_method_to_settings()
