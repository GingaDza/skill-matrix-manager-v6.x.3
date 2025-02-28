#!/usr/bin/env python3
"""レーダーチャートダイアログのデータ構造を修正"""

import os

def fix_radar_chart():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # バックアップ作成
    backup_path = filepath + ".data_fix.bak"
    os.system(f"cp {filepath} {backup_path}")
    print(f"バックアップ作成: {backup_path}")
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 各行を修正
    modified_lines = []
    in_draw_radar_chart = False
    
    for line in lines:
        # draw_radar_chartメソッド内を検出
        if "def draw_radar_chart" in line:
            in_draw_radar_chart = True
            modified_lines.append(line)
        elif in_draw_radar_chart and "def " in line:
            in_draw_radar_chart = False
            modified_lines.append(line)
        elif in_draw_radar_chart and "if not self.stages_data or not self.stages_data[0]['targets']:" in line:
            # ターゲットキーの代わりにskillsキーを使用
            modified_line = line.replace("['targets']", "['skills']")
            modified_lines.append(modified_line)
            print(f"['targets']を['skills']に変更: {modified_line.strip()}")
        elif in_draw_radar_chart and "'targets'" in line:
            # その他のターゲット参照も変更
            modified_line = line.replace("'targets'", "'skills'")
            modified_lines.append(modified_line)
            print(f"'targets'を'skills'に変更: {modified_line.strip()}")
        else:
            modified_lines.append(line)
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.writelines(modified_lines)
    
    print(f"{filepath}のターゲット参照を修正しました")
    return True

# draw_chartメソッド内の修正
def fix_draw_chart():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 各行を修正
    modified_lines = []
    in_draw_chart = False
    
    for line in lines:
        # draw_chartメソッド内を検出
        if "def draw_chart" in line:
            in_draw_chart = True
            modified_lines.append(line)
        elif in_draw_chart and "def " in line:
            in_draw_chart = False
            modified_lines.append(line)
        elif in_draw_chart and "if not skills:" in line:
            # skills条件を強化
            modified_line = line.replace("if not skills:", "if not skills or len(skills) == 0:")
            modified_lines.append(modified_line)
            print(f"'if not skills:'を条件強化: {modified_line.strip()}")
        else:
            modified_lines.append(line)
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.writelines(modified_lines)
    
    print(f"{filepath}のdraw_chartメソッドを修正しました")
    return True

# さらにコードを詳しく調べて修正
def inspect_radar_chart_dialog():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    print("\n--- レーダーチャートダイアログの構造を調査 ---")
    
    # メソッド名を抽出
    methods = re.findall(r'def (\w+)', content)
    print(f"メソッド一覧: {', '.join(methods)}")
    
    # データ構造の扱いを確認
    if "stages_data" in content:
        print("stages_dataが見つかりました")
        # 初期化部分を探す
        init_match = re.search(r'def __init__.*?:(.*?)def ', content, re.DOTALL)
        if init_match:
            init_code = init_match.group(1)
            print("\n初期化コード:")
            print(init_code)
    
    # データ参照パターンを抽出
    targets_refs = re.findall(r"(\w+)\['targets'\]", content)
    skills_refs = re.findall(r"(\w+)\['skills'\]", content)
    
    print(f"\n'targets'参照: {targets_refs}")
    print(f"'skills'参照: {skills_refs}")
    
    return True

# 全修正関数を実行
import re
fix_radar_chart()
fix_draw_chart()
inspect_radar_chart_dialog()
