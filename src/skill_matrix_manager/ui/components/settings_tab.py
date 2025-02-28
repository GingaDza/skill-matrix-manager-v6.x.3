#!/usr/bin/env python3
import traceback
"""初期設定タブ"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                           QPushButton, QLabel, QInputDialog, QMessageBox,
                           QTreeWidget, QTreeWidgetItem)

class SettingsTab(QWidget):
    """設定タブクラス"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """UIの初期化"""
        # メインレイアウト
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # 左側：グループリスト
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("グループリスト"))
        
        self.group_list = QListWidget()
        left_layout.addWidget(self.group_list)
        
        # グループ操作ボタン
        group_buttons = QHBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        group_buttons.addWidget(self.add_group_btn)
        group_buttons.addWidget(self.edit_group_btn)
        group_buttons.addWidget(self.delete_group_btn)
        
        left_layout.addLayout(group_buttons)
        
        # 右側：カテゴリとスキル
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("カテゴリー/スキル"))
        
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(["名前"])
        right_layout.addWidget(self.category_tree)
        
        # カテゴリ/スキル操作ボタン
        cat_buttons = QVBoxLayout()
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.edit_category_btn = QPushButton("カテゴリー編集")
        self.delete_category_btn = QPushButton("カテゴリー削除")
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        
        cat_buttons.addWidget(self.add_category_btn)
        cat_buttons.addWidget(self.edit_category_btn)
        cat_buttons.addWidget(self.delete_category_btn)
        cat_buttons.addWidget(self.add_skill_btn)
        cat_buttons.addWidget(self.edit_skill_btn)
        cat_buttons.addWidget(self.delete_skill_btn)
        
        right_layout.addLayout(cat_buttons)
        
        # 新規タブ追加ボタン
        self.add_tab_btn = QPushButton("新規タブ追加")
        right_layout.addWidget(self.add_tab_btn)
        
        # レイアウト配置
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        # イベント接続
        self.add_group_btn.clicked.connect(self.add_group)
        self.edit_group_btn.clicked.connect(self.edit_group)
        self.delete_group_btn.clicked.connect(self.delete_group)
        self.add_category_btn.clicked.connect(self.add_category)
        self.edit_category_btn.clicked.connect(self.edit_category)
        self.delete_category_btn.clicked.connect(self.delete_category)
        self.add_skill_btn.clicked.connect(self.add_skill)
        self.edit_skill_btn.clicked.connect(self.edit_skill)
        self.delete_skill_btn.clicked.connect(self.delete_skill)
        self.add_tab_btn.clicked.connect(self.add_new_tab)

    # 以下は自動生成されたメソッドです

    def add_group(self):
        """グループ追加"""
        group_name, ok = QInputDialog.getText(self, "グループ追加", "グループ名:")
        if ok and group_name:
            self.group_list.addItem(group_name)
            if hasattr(self, "update_main_window"):
                self.update_main_window()

    def edit_group(self):
        """グループ編集"""
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

    def delete_group(self):
        """グループ削除"""
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

    def add_category(self):
        """カテゴリー追加"""
        category_name, ok = QInputDialog.getText(self, "カテゴリー追加", "カテゴリー名:")
        if ok and category_name:
            category_item = QTreeWidgetItem([category_name])
            self.category_tree.addTopLevelItem(category_item)
            self.category_tree.setCurrentItem(category_item)

    def edit_category(self):
        """カテゴリー編集"""
        current_item = self.category_tree.currentItem()
        if not current_item or current_item.parent():
            QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください")
            return
        
        old_name = current_item.text(0)
        new_name, ok = QInputDialog.getText(self, "カテゴリー編集", "カテゴリー名:", text=old_name)
        
        if ok and new_name:
            current_item.setText(0, new_name)

    def delete_category(self):
        """カテゴリー削除"""
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

    def add_skill(self):
        """スキル追加"""
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

    def edit_skill(self):
        """スキル編集"""
        current_item = self.category_tree.currentItem()
        if not current_item or not current_item.parent():
            QMessageBox.warning(self, "警告", "編集するスキルを選択してください")
            return
        
        old_name = current_item.text(0)
        new_name, ok = QInputDialog.getText(self, "スキル編集", "スキル名:", text=old_name)
        
        if ok and new_name:
            current_item.setText(0, new_name)

    def delete_skill(self):
        """スキル削除"""
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

    def add_new_tab(self):
        print("=== 新規タブ追加メソッドが呼び出されました ====")
        """新規タブを追加"""
        try:
            print("新規タブ追加の処理を開始します")
            # 選択カテゴリーを確認
            current_item = self.category_tree.currentItem()
            print(f"選択項目: {current_item}")
            if not current_item:
                QMessageBox.warning(self, "警告", "タブにするカテゴリーを選択してください")
                return
            
            # カテゴリーであることを確認（親がない=トップレベル項目）
            if current_item.parent():
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
            
            # タブ追加メソッドを呼び出す
            print(f"メインウィンドウは add_category_tab メソッドを持っていますか？: {hasattr(main_window, 'add_category_tab')}")
            if hasattr(main_window, "add_category_tab"):
                result = main_window.add_category_tab(category_name)
                if result:
                    QMessageBox.information(self, "成功", f"新規タブ「{category_name}」を追加しました")
            else:
                QMessageBox.warning(self, "エラー", "タブ追加機能が見つかりません")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"タブ追加中にエラーが発生しました: {str(e)}")
