#!/usr/bin/env python3
"""オリジナルファイルを復元し、最小限の修正を適用"""

import os
import re
import glob

def find_oldest_backup(prefix):
    """最も古いバックアップファイルを見つける"""
    backups = glob.glob(f"{prefix}*.bak")
    if not backups:
        return None
    
    # 更新時間で並べ替え（古い順）
    backups.sort(key=lambda x: os.path.getmtime(x))
    return backups[0]

def restore_original_files():
    """オリジナルファイルの復元"""
    # staged_target_tab.pyの最も古いバックアップを見つける
    tab_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    tab_backup = find_oldest_backup(tab_path)
    
    if tab_backup:
        print(f"StagedTargetTabの最も古いバックアップ: {tab_backup}")
        os.system(f"cp {tab_backup} {tab_path}")
        print(f"{tab_path}をオリジナルから復元しました")
    else:
        print(f"警告: {tab_path}のバックアップが見つかりません")
    
    # radar_chart_dialog.pyの最も古いバックアップを見つける
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    dialog_backup = find_oldest_backup(dialog_path)
    
    if dialog_backup:
        print(f"RadarChartDialogの最も古いバックアップ: {dialog_backup}")
        os.system(f"cp {dialog_backup} {dialog_path}")
        print(f"{dialog_path}をオリジナルから復元しました")
    else:
        print(f"警告: {dialog_path}のバックアップが見つかりません")
    
    return True

def fix_indentation_only():
    """インデントの問題だけを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    # ファイルを読み込む
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 行番号をつけて表示
    print("\n--- インデントを修正する部分を特定 ---")
    for i, line in enumerate(lines):
        if "dialog.exec_(" in line:
            print(f"行 {i+1}: {line.strip()}")
            # 前後の行を確認
            start = max(0, i-2)
            end = min(len(lines), i+3)
            for j in range(start, end):
                if j != i:
                    prefix = "  "
                    print(f"{prefix}行 {j+1}: {lines[j].strip()}")
    
    # インデントの問題だけを修正
    modified = False
    for i, line in enumerate(lines):
        if "dialog.exec_(" in line and i+1 < len(lines):
            if lines[i+1].strip() == "else:":
                print(f"\n問題を特定: {i+2}行目の'else:'は無効です")
                # elseの行を削除
                lines.pop(i+1)
                modified = True
                print("'else:'行を削除しました")
                break
    
    if modified:
        # 保存
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"{filepath}のインデント問題を修正しました")
    else:
        print("インデント問題は見つかりませんでした")
    
    return modified

def fix_radar_skills_only():
    """RadarChartDialogのskillsアクセス問題だけを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイルを読み込む
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # skills.keys()が使われている場合、リスト型へのアクセスを修正
    modified = False
    for i, line in enumerate(lines):
        if "stage['skills'].keys()" in line:
            print(f"\n問題を特定: {i+1}行目で'stage['skills'].keys()'が使われています")
            # リストとして処理
            indent = line[:line.find("all_skills")]
            new_line = f"{indent}# リスト形式のスキルに対応\n"
            new_line += f"{indent}for skill in stage['skills']:\n"
            new_line += f"{indent}    if isinstance(skill, dict) and 'name' in skill:\n"
            new_line += f"{indent}        all_skills.add(skill['name'])\n"
            
            # 置き換え
            lines[i] = new_line
            modified = True
            print("スキルアクセスを修正しました")
            
        elif "values.append(stage['skills'].get(skill_id, 0))" in line:
            print(f"\n問題を特定: {i+1}行目で'stage['skills'].get(skill_id, 0)'が使われています")
            # リストとして処理
            indent = line[:line.find("values")]
            new_line = f"{indent}# リスト形式のスキルに対応\n"
            new_line += f"{indent}skill_value = 0\n"
            new_line += f"{indent}for skill in stage['skills']:\n"
            new_line += f"{indent}    if skill.get('name') == skill_id:\n"
            new_line += f"{indent}        skill_value = skill.get('value', 0)\n"
            new_line += f"{indent}        break\n"
            new_line += f"{indent}values.append(skill_value)\n"
            
            # 置き換え
            lines[i] = new_line
            modified = True
            print("値アクセスを修正しました")
    
    if modified:
        # 保存
        with open(filepath, 'w') as f:
            f.writelines(lines)
        print(f"{filepath}のスキルアクセス問題を修正しました")
    else:
        print("スキルアクセス問題は見つかりませんでした")
    
    return modified

def check_syntax():
    """構文エラーがないか確認"""
    files = [
        "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py",
        "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    ]
    
    all_ok = True
    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            compile(content, filepath, 'exec')
            print(f"✓ {filepath}の構文は正常です")
        except SyntaxError as e:
            print(f"✗ {filepath}の構文エラー: {e}")
            all_ok = False
    
    return all_ok

# 実行
restore_original_files()
fix_indentation_only()
fix_radar_skills_only()
check_syntax()

print("\n修正が完了しました。アプリケーションを起動します...")
