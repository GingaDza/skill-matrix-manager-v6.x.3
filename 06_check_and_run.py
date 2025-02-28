#!/usr/bin/env python3
"""構文チェックとアプリケーション実行"""
import os
import sys
import subprocess

def check_syntax(filepath):
    """構文エラーがないか確認"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        compile(content, filepath, 'exec')
        print(f"✓ {filepath}の構文は正常です")
        return True
    except SyntaxError as e:
        print(f"✗ {filepath}の構文エラー: {e}")
        print(f"  行 {e.lineno}, 列 {e.offset}: {e.text}")
        return False

# ファイルパス
files = [
    "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py",
    "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
]

# 構文チェック
all_ok = True
for filepath in files:
    if not check_syntax(filepath):
        all_ok = False

if all_ok:
    print("\n構文チェック完了。エラーはありません。")
    print("アプリケーションを起動します...")
    sys.exit(0)  # 正常終了（main.pyはこのスクリプトの後に実行）
else:
    print("\n構文エラーがあります。修正が必要です。")
    sys.exit(1)  # エラー終了
