#!/usr/bin/env python3
"""設定タブのメソッドを完成させる"""

import os

def complete_tab_methods():
    """設定タブに必要なメソッドを追加"""
    filepath = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 必要なメソッドを確認
    missing_methods = []
    
    methods = [
        "add_group", "edit_group", "delete_group",
        "add_category", "edit_category", "delete_category",
        "add_skill", "edit_skill", "delete_skill"
    ]
    
    for method in methods:
        if f"def {method}" not in content:
            missing_methods.append(method)
    
    # 足りないメソッドがあれば追加
    if missing_methods:
        # バックアップ
        backup = filepath + ".methods.bak"
        with open(filepath, 'r') as src:
            with open(backup, 'w') as dst:
                dst.write(src.read())
        print(f"バックアップ: {backup}")
        
        # 追加する場所を探す
        last_def = content.rfind("def ")
        class_end = content.find("if __name__", last_def) if "if __name__" in content else len(content)
        
        # 足りないメソッドを追加
        additional_methods = """
    # 以下は自動生成されたメソッドです
"""
        
        # グループ関連
        if "add_group" in missing_methods:
            additional_methods += """
    def add_group(self):
        \"\"\"グループ追加\"\"\"
        group_name, ok = QInputDialog.getText(self, "グループ追加", "グループ名:")
        if ok and group_name:
            self.group_list.addItem(group_name)
            if hasattr(self, "update_main_window"):
                self.update_main_window()
"""
        
        if "edit_group" in missing_methods:
            additional_methods += """
    def edit_group(self):
        \"\"\"グループ編集\"\"\"
        current_item = self.group_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するグループを選択してください")
            return
        
        old_name = current_item.text()
        new_name, ok = QInputDialog.getText(self, "グループ編集", "グループ名:", text=old_name)
        
        if ok and new_name:
            current_item.setText(new_name)
            if hasattr(self, "update_main_window"):
                self.update_main_window()
"""
        
        if "delete_group" in missing_methods:
            additional_methods += """
    def delete_group(self):
        \"\"\"グループ削除\"\"\"
        current_row = self.group_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "削除するグループを選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このグループを削除しますか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.group_list.takeItem(current_row)
            if hasattr(self, "update_main_window"):
                self.update_main_window()
"""
        
        # カテゴリ関連
        if "add_category" in missing_methods:
            additional_methods += """
    def add_category(self):
        \"\"\"カテゴリー追加\"\"\"
        category_name, ok = QInputDialog.getText(self, "カテゴリー追加", "カテゴリー名:")
        if ok and category_name:
            category_item = QTreeWidgetItem([category_name])
            self.category_tree.addTopLevelItem(category_item)
            self.category_tree.setCurrentItem(category_item)
"""
        
        if "edit_category" in missing_methods:
            additional_methods += """
    def edit_category(self):
        \"\"\"カテゴリー編集\"\"\"
        current_item = self.category_tree.currentItem()
        if not current_item or current_item.parent():
            QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください")
            return
        
        old_name = current_item.text(0)
        new_name, ok = QInputDialog.getText(self, "カテゴリー編集", "カテゴリー名:", text=old_name)
        
        if ok and new_name:
            current_item.setText(0, new_name)
"""
        
        if "delete_category" in missing_methods:
            additional_methods += """
    def delete_category(self):
        \"\"\"カテゴリー削除\"\"\"
        current_item = self.category_tree.currentItem()
        if not current_item or current_item.parent():
            QMessageBox.warning(self, "警告", "削除するカテゴリーを選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このカテゴリーとそのスキルを削除しますか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            index = self.category_tree.indexOfTopLevelItem(current_item)
            self.category_tree.takeTopLevelItem(index)
"""
        
        # スキル関連
        if "add_skill" in missing_methods:
            additional_methods += """
    def add_skill(self):
        \"\"\"スキル追加\"\"\"
        current_item = self.category_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "スキルを追加するカテゴリーを選択してください")
            return
        
        # 親カテゴリを取得
        parent_item = current_item if not current_item.parent() else None
        if not parent_item:
            parent_item = current_item.parent()
        
        if parent_item:
            skill_name, ok = QInputDialog.getText(self, "スキル追加", "スキル名:")
            if ok and skill_name:
                skill_item = QTreeWidgetItem([skill_name])
                parent_item.addChild(skill_item)
                parent_item.setExpanded(True)
"""
        
        if "edit_skill" in missing_methods:
            additional_methods += """
    def edit_skill(self):
        \"\"\"スキル編集\"\"\"
        current_item = self.category_tree.currentItem()
        if not current_item or not current_item.parent():
            QMessageBox.warning(self, "警告", "編集するスキルを選択してください")
            return
        
        old_name = current_item.text(0)
        new_name, ok = QInputDialog.getText(self, "スキル編集", "スキル名:", text=old_name)
        
        if ok and new_name:
            current_item.setText(0, new_name)
"""
        
        if "delete_skill" in missing_methods:
            additional_methods += """
    def delete_skill(self):
        \"\"\"スキル削除\"\"\"
        current_item = self.category_tree.currentItem()
        if not current_item or not current_item.parent():
            QMessageBox.warning(self, "警告", "削除するスキルを選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このスキルを削除しますか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            parent_item = current_item.parent()
            index = parent_item.indexOfChild(current_item)
            parent_item.takeChild(index)
"""
        
        # メソッド追加
        content = content[:class_end] + additional_methods + content[class_end:]
        
        # 変更保存
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"{filepath}に不足していたメソッドを追加しました: {', '.join(missing_methods)}")
    else:
        print(f"全ての必要なメソッドは既に実装されています")
    
    return True

if __name__ == "__main__":
    complete_tab_methods()
