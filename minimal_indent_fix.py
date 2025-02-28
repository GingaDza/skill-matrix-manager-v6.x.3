#!/usr/bin/env python3
"""最も小さい変更でインデントエラーを修正する"""

import os
import re

def find_and_fix_indentation():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップを作成
    backup_path = filepath + ".minimal.bak"
    os.system(f"cp {filepath} {backup_path}")
    print(f"バックアップ作成: {backup_path}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 問題の行を見つける
    dialog_exec_line = -1
    else_line = -1
    for i, line in enumerate(lines):
        if "dialog.exec_()" in line:
            dialog_exec_line = i
        if line.strip() == "else:":
            else_line = i
            # 前の行がdialog.exec_()の場合、これが問題
            if i > 0 and "dialog.exec_()" in lines[i-1]:
                print(f"問題を発見: {i+1}行目の'else:'はインデント問題があります")
    
    # 問題の修正: elseブロック全体を削除
    if dialog_exec_line >= 0 and else_line >= 0:
        # elseから次のブロックまでを特定
        block_end = else_line + 1
        while block_end < len(lines) and (lines[block_end].strip() == "" or 
                                          lines[block_end].startswith(' ')):
            block_end += 1
        
        print(f"削除範囲: {else_line+1}行目から{block_end}行目")
        
        # 削除
        new_lines = lines[:else_line] + lines[block_end:]
        
        # 保存
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        
        print(f"{filepath}の不正なelseブロックを削除しました")
        return True
    else:
        print("インデント問題が見つかりませんでした")
        return False

# 実行
find_and_fix_indentation()
