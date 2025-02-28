#!/usr/bin/env python3
"""RadarChartDialogのエラーを修正"""
import os
import re

filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"

# バックアップ作成
os.system(f"cp {filepath} {filepath}.error_fix.bak")
print(f"バックアップ作成: {filepath}.error_fix.bak")

# ファイルを読み込む
with open(filepath, 'r') as f:
    content = f.read()

# 既存のshow_radar_chartメソッド内で問題を修正
# 現在のエラー：dialog = RadarChartDialog(self, stages_data) の呼び出し箇所で
# compare_modeパラメータが不足している

# 既存の呼び出し方法を修正する (show_radar_chartメソッド内)
radar_chart_call_pattern = r'dialog\s*=\s*RadarChartDialog\(self,\s*stages_data\)'
if re.search(radar_chart_call_pattern, content):
    content = re.sub(
        radar_chart_call_pattern,
        'dialog = RadarChartDialog(self, stages_data, compare_mode=False)',
        content
    )
    print("RadarChartDialogの呼び出しを修正しました")
else:
    print("RadarChartDialogの呼び出しが見つかりませんでした")

# 保存
with open(filepath, 'w') as f:
    f.write(content)

# ファイルパス
tab_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"

# タブファイルを読み込む
with open(tab_path, 'r') as f:
    tab_content = f.read()

# RadarChartDialogの呼び出しを修正
radar_chart_call_pattern = r'dialog\s*=\s*RadarChartDialog\(self,\s*stages_data\)'
if re.search(radar_chart_call_pattern, tab_content):
    tab_content = re.sub(
        radar_chart_call_pattern,
        'dialog = RadarChartDialog(self, stages_data, compare_mode=False)',
        tab_content
    )
    print(f"{tab_path}内のRadarChartDialogの呼び出しを修正しました")
    
    # 保存
    with open(tab_path, 'w') as f:
        f.write(tab_content)
else:
    print(f"{tab_path}内のRadarChartDialogの呼び出しが見つかりませんでした")

print("エラー修正を完了しました。アプリケーションを再起動します...")
