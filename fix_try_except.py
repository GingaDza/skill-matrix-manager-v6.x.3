#!/usr/bin/env python3
"""正しい範囲で問題のある行だけを修正"""

import os
import re

def restore_and_fix():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    # 最新のバックアップを特定
    backup_files = []
    for file in os.listdir("src/skill_matrix_manager/ui/components/skill_gap_tab/"):
        if file.startswith("staged_target_tab.py.") and file.endswith(".bak"):
            backup_files.append(os.path.join("src/skill_matrix_manager/ui/components/skill_gap_tab/", file))
    
    if not backup_files:
        print("バックアップファイルが見つかりません")
        return False
    
    # 最新のバックアップを使用（timeで並べ替え）
    backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_backup = backup_files[0]
    print(f"最新バックアップ: {latest_backup}")
    
    # ファイルをバックアップから復元
    os.system(f"cp {latest_backup} {filepath}")
    print(f"{filepath}をバックアップから復元しました")
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 新しいバックアップを作成
    new_backup = filepath + ".proper_fix.bak"
    with open(new_backup, 'w') as f:
        f.write(content)
    print(f"新しいバックアップを作成: {new_backup}")
    
    # 問題のパターンを探して修正
    # try ... dialog.exec_() + else: ... except の構造を見つける
    pattern = r'(\s+)try:.*?\n.*?dialog\.exec_\(\).*?\n(\s+)else:'
    
    if re.search(pattern, content, re.DOTALL):
        # elseだけを削除（既存のインデントと行末の改行は維持）
        fixed_content = re.sub(
            r'(\s+)else:\s*\n',
            r'\1\n',
            content
        )
        
        # elseに続く行のインデントを1レベル下げる必要がある場合
        fixed_content = re.sub(
            r'(\s+)else:\s*\n(\s+)([^\s])',
            r'\1\n\1\3',
            content
        )
        
        # 保存
        with open(filepath, 'w') as f:
            f.write(fixed_content)
        
        print(f"{filepath}の'else:'行を削除しました")
    else:
        print("'else:'のパターンが見つかりませんでした")
    
    # 問題の行を直接編集
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 'else:'行を見つけて削除
    for i, line in enumerate(lines):
        if line.strip() == 'else:':
            print(f"'else:'行を見つけました: {i+1}行目")
            # 前の行がdialog.exec_()ならこれは問題の行
            if i > 0 and 'dialog.exec_()' in lines[i-1]:
                # 行を削除
                lines.pop(i)
                print(f"問題の'else:'行を削除しました")
                break
    
    # 保存
    with open(filepath, 'w') as f:
        f.writelines(lines)
    
    # 構文チェック
    try:
        compile(open(filepath).read(), filepath, 'exec')
        print(f"{filepath}の構文チェック成功")
        return True
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return False

# 実行
restore_and_fix()
