#!/usr/bin/env python3
"""RadarChartDialogに比較モードを追加"""
import os
import re

filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"

# ファイルを読み込む
with open(filepath, 'r') as f:
    content = f.read()

# __init__メソッドのパラメータを更新
init_pattern = r'def __init__\(self, parent=None, stages_data=None\):'
if re.search(init_pattern, content):
    content = re.sub(
        init_pattern,
        'def __init__(self, parent=None, stages_data=None, compare_mode=False):',
        content
    )
    print("__init__メソッドのパラメータを更新しました")
else:
    print("__init__メソッドが見つかりませんでした")

# compare_mode属性を初期化
init_body_pattern = r'def __init__.*?super\(.*?\)\.__init__\(parent\)(.*?)self\.setup_ui\(\)'
init_body_match = re.search(init_body_pattern, content, re.DOTALL)
if init_body_match:
    init_body = init_body_match.group(1)
    new_init_body = init_body + "\n        # 比較モード\n        self.compare_mode = compare_mode\n        "
    content = content.replace(init_body, new_init_body)
    print("compare_mode属性を初期化しました")
else:
    print("__init__メソッドの本体が見つかりませんでした")

# 保存
with open(filepath, 'w') as f:
    f.write(content)

print("RadarChartDialogの初期化メソッド更新が完了しました。")
