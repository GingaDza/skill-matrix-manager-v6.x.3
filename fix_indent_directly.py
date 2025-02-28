#!/usr/bin/env python3
"""インデントエラーを直接修正する簡単なスクリプト"""

import os

def fix_indent():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ作成
    backup = filepath + ".simple_fix.bak"
    with open(filepath, 'r') as f:
        content = f.read()
    
    with open(backup, 'w') as f:
        f.write(content)
    print(f"バックアップ作成: {backup}")
    
    # 問題のある行を探す
    lines = content.split('\n')
    exec_line = -1
    
    for i, line in enumerate(lines):
        if "dialog.exec_()" in line:
            exec_line = i
            print(f"dialog.exec_()の行を見つけました: {i+1}行目")
            print(f"現在の行: '{line}'")
            break
    
    if exec_line >= 0:
        # エラーの行の前の行を見つける（空行でない）
        prev_line = exec_line - 1
        while prev_line >= 0 and not lines[prev_line].strip():
            prev_line -= 1
        
        if prev_line >= 0:
            # 前の行のインデントを取得
            prev_indent = len(lines[prev_line]) - len(lines[prev_line].lstrip())
            print(f"前の行: '{lines[prev_line]}'")
            print(f"前の行のインデント: {prev_indent}スペース")
            
            # 新しいインデントを適用
            lines[exec_line] = ' ' * prev_indent + lines[exec_line].strip()
            print(f"修正後の行: '{lines[exec_line]}'")
        
        # 修正した内容を保存
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        print(f"{filepath}のインデントを修正しました")
        
        return True
    else:
        print("dialog.exec_()の行が見つかりませんでした")
        return False

def check_indent():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    try:
        compile(content, filepath, 'exec')
        print("構文チェック成功!")
        return True
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        if hasattr(e, 'lineno'):
            lines = content.split('\n')
            if 0 <= e.lineno - 1 < len(lines):
                print(f"エラー行 ({e.lineno}): {lines[e.lineno - 1]}")
                if e.lineno - 2 >= 0:
                    print(f"前の行 ({e.lineno - 1}): {lines[e.lineno - 2]}")
                if e.lineno < len(lines):
                    print(f"次の行 ({e.lineno + 1}): {lines[e.lineno]}")
        return False

if __name__ == "__main__":
    if fix_indent():
        check_indent()
