#!/usr/bin/env python3
"""グループとメンバー管理の同期問題を修正するスクリプト"""

import os
from datetime import datetime

def backup_file(filepath):
    """ファイルのバックアップを作成"""
    if os.path.exists(filepath):
        dir_name = os.path.dirname(filepath)
        backup_dir = os.path.join(dir_name, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        base_name = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{base_name}.{timestamp}")
        
        with open(filepath, 'r', encoding='utf-8') as src:
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        print(f"バックアップを作成しました: {backup_path}")
        return True
    return False

def add_update_method():
    """メインウィンドウにグループコンボボックス更新メソッドを追加"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルの読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 必要なimportの確認と追加
    if "from src.skill_matrix_manager.database import SkillMatrixDatabase" not in content:
        import_section = content.find("import")
        import_end = content.find("\n\n", import_section)
        
        if import_end > 0:
            content = content[:import_end] + "\nfrom src.skill_matrix_manager.database import SkillMatrixDatabase" + content[import_end:]
    
    # メソッドの追加 (存在しない場合のみ)
    if "def update_group_combo" not in content:
        # クラスの最後にメソッドを追加する場所を探す
        last_method = content.rfind("def ")
        if last_method > 0:
            next_def = content.find("def ", last_method + 4)
            if next_def < 0:  # 最後のメソッド
                # クラスの終わりを見つける
                class_end = content.find("\nif __name__")
                if class_end < 0:
                    class_end = len(content)
                
                # 更新メソッドを追加
                update_method = """
    def update_group_combo(self):
        """グループコンボボックス更新"""
        try:
            # 現在の選択を保存
            current_selection = self.group_combo.currentText()
            
            # グループリストをクリア
            self.group_combo.clear()
            
            # グループの読み込み
            db = SkillMatrixDatabase()
            db.connect()
            groups = db.get_groups()
            db.close()
            
            # 「すべて」の選択肢を追加
            self.group_combo.addItem("すべて")
            
            # グループを追加
            for group in groups:
                self.group_combo.addItem(group)
            
            # 以前の選択を復元
            index = self.group_combo.findText(current_selection)
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
            else:
                self.group_combo.setCurrentIndex(0)
                
            # ユーザーリストも更新
            self.update_user_list()
        except Exception as e:
            print(f"グループコンボボックス更新エラー: {e}")
"""
                
                content = content[:class_end] + update_method + content[class_end:]
    
    # 初期化時にグループコンボボックス更新を呼び出す
    if "self.update_group_combo()" not in content:
        # show()を探す
        show_pos = content.find("self.show()")
        if show_pos > 0:
            line_start = content.rfind("\n", 0, show_pos)
            content = content[:line_start] + "\n        # グループコンボボックス初期化\n        self.update_group_combo()" + content[line_start:]
    
    # 変更を保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{filepath} を修正しました")
    return True

def connect_settings_tab():
    """設定タブのグループ操作にメインウィンドウ更新を追加"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "components", "settings_tab.py")
    
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルの読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # update_main_window メソッドがなければ追加
    if "def update_main_window" not in content:
        # クラスの最後にメソッドを追加
        last_method = content.rfind("def ")
        next_class = content.find("class ", last_method)
        
        if next_class < 0:  # 次のクラスがない場合
            next_class = len(content)
        
        # メソッドの終わりを探す
        method_end = content.find("\n\n", last_method)
        if method_end < 0 or method_end > next_class:
            method_end = next_class
        
        # メソッドを追加
        update_method = """
    def update_main_window(self):
        """メインウィンドウにグループ変更を通知"""
        try:
            # ルートウィンドウを取得
            main_window = self
            while main_window.parent():
                main_window = main_window.parent()
            
            # グループコンボボックス更新メソッドを呼び出し
            if hasattr(main_window, "update_group_combo"):
                main_window.update_group_combo()
        except Exception as e:
            print(f"メインウィンドウ更新エラー: {e}")
"""
        
        content = content[:method_end] + update_method + content[method_end:]
    
    # グループ操作後に更新メソッドを呼び出す箇所を追加
    operations = [
        ("self.group_list.addItem(group_name)", "self.group_list.addItem(group_name)\n            # メインウィンドウに通知\n            self.update_main_window()"),
        ("self.group_list.currentItem().setText(new_name)", "self.group_list.currentItem().setText(new_name)\n            # メインウィンドウに通知\n            self.update_main_window()"),
        ("self.group_list.takeItem(row)", "self.group_list.takeItem(row)\n            # メインウィンドウに通知\n            self.update_main_window()")
    ]
    
    for old, new in operations:
        if old in content and old + "\n            # メインウィンドウに通知" not in content:
            content = content.replace(old, new)
    
    # 変更を保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{filepath} を修正しました")
    return True

if __name__ == "__main__":
    print("グループとメンバー管理の同期問題を修正します...")
    
    # メインウィンドウにグループコンボボックス更新メソッドを追加
    add_update_method()
    
    # 設定タブのグループ操作にメインウィンドウ更新を追加
    connect_settings_tab()
    
    print("修正が完了しました。")
