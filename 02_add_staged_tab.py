#!/usr/bin/env python3
"""段階的目標タブを追加"""
import os
import re

filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"

# ファイルを読み込む
with open(filepath, 'r') as f:
    content = f.read()

# setup_tabs メソッドを更新
setup_tabs_pattern = r'def setup_tabs\(self\):(.*?)self\.add_sample_tabs\(\)'
if re.search(setup_tabs_pattern, content, re.DOTALL):
    content = re.sub(
        setup_tabs_pattern,
        'def setup_tabs(self):\\1self.add_sample_tabs()\n        # 段階的目標設定タブを追加\n        self.add_staged_targets_tab()',
        content
    )
    print("setup_tabs メソッドを更新しました")
else:
    print("setup_tabs メソッドが見つかりませんでした")

# add_staged_targets_tab メソッドを追加
staged_tab_method = """
    def add_staged_targets_tab(self):
        \"\"\"段階的な目標設定タブを追加\"\"\"
        # 段階的目標タブ
        staged_tab = QWidget()
        staged_layout = QVBoxLayout()
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # 内部コンテンツウィジェット
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # タイトルとヘルプテキスト
        title_label = QLabel("段階的な目標設定")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        content_layout.addWidget(title_label)
        
        help_text = QLabel("各段階でのスキル目標値を設定します。現在値と目標値を比較表示できます。")
        help_text.setWordWrap(True)
        content_layout.addWidget(help_text)
        
        # スキル段階選択
        stages_layout = QHBoxLayout()
        stages_layout.addWidget(QLabel("表示する段階:"))
        
        # 段階の選択（チェックボックス）
        stages = self.generate_test_data()
        self.stage_checkboxes = []
        
        for i, stage in enumerate(stages):
            stage_name = stage.get('name', f'段階{i+1}')
            checkbox = QCheckBox(stage_name)
            checkbox.setChecked(True)  # デフォルトでは全て選択
            stages_layout.addWidget(checkbox)
            self.stage_checkboxes.append(checkbox)
        
        content_layout.addLayout(stages_layout)
        
        # コンテンツをセット
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        staged_layout.addWidget(scroll)
        
        # ボタン配置
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        # 比較チャート表示ボタン
        compare_button = QPushButton("比較チャート表示")
        compare_button.clicked.connect(self.show_comparison_chart)
        button_layout.addWidget(compare_button)
        
        staged_layout.addLayout(button_layout)
        staged_tab.setLayout(staged_layout)
        
        # タブに追加
        self.tabs.addTab(staged_tab, "段階的目標")
"""

# クラス定義の末尾を探す
class_end = content.rfind("    def ")
if class_end != -1:
    # 最後のメソッドを見つける
    last_method_match = re.search(r'(    def [^\(]+\([^:]+:.*?)(\Z)', content[class_end:], re.DOTALL)
    if last_method_match:
        insertion_point = class_end + last_method_match.end(1)
        # メソッドを挿入
        content = content[:insertion_point] + staged_tab_method + content[insertion_point:]
        print("add_staged_targets_tab メソッドを追加しました")
    else:
        print("最後のメソッドが見つかりませんでした")
else:
    print("クラス定義が見つかりませんでした")

# 保存
with open(filepath, 'w') as f:
    f.write(content)

print("段階的目標タブの追加が完了しました。")
