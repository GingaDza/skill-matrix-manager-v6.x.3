#!/usr/bin/env python3
"""設定タブファイルを作成"""

import os

def create_settings_tab():
    """設定タブファイルを作成"""
    filepath = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    # 既存のファイルがあるか確認
    if os.path.exists(filepath):
        print(f"{filepath}は既に存在します。修正スクリプトを使用してください。")
        return False
    
    # ディレクトリ作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 基本的な設定タブファイル作成
    with open(filepath, 'w') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"初期設定タブ\"\"\"

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                           QPushButton, QLabel, QInputDialog, QMessageBox,
                           QTreeWidget, QTreeWidgetItem)

class SettingsTab(QWidget):
    \"\"\"設定タブクラス\"\"\"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        \"\"\"UIの初期化\"\"\"
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
""")
    
    print(f"{filepath}を作成しました")
    return True

if __name__ == "__main__":
    create_settings_tab()
