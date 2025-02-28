#!/usr/bin/env python3
"""loggingモジュールのインポート問題を解決する"""

import os
import re

def fix_radar_chart_dialog_import():
    """radar_chart_dialog.pyのloggingインポートを強制的に修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    # バックアップ作成
    backup_file = filepath + ".import_fix.bak"
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"バックアップを作成しました: {backup_file}")
    
    # 正規表現で先頭のインポート文を確認
    imports = re.findall(r'^import [^;]+|^from [^;]+', content, re.MULTILINE)
    
    has_logging_import = False
    for imp in imports:
        if "import logging" in imp:
            has_logging_import = True
            break
    
    # インポートがない場合は追加
    if not has_logging_import:
        # ファイルの先頭に追加する場合
        if content.startswith('import ') or content.startswith('from '):
            # 既存のインポート文の前に追加
            content = "import logging\n\n" + content
        else:
            # ファイルの先頭に追加
            first_line_end = content.find('\n')
            if first_line_end >= 0:
                content = content[:first_line_end+1] + "import logging\n" + content[first_line_end+1:]
            else:
                content = "import logging\n" + content
    
    # ファイルを保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にloggingインポートを追加しました")
    
    # 確認のためファイルの先頭部分を表示
    with open(filepath, 'r') as f:
        head = ''.join(f.readlines()[:10])
    print(f"ファイルの先頭部分:\n{head}")
    
    return True

def fix_staged_target_tab_import():
    """staged_target_tab.pyのloggingインポートを強制的に修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    # バックアップ作成
    backup_file = filepath + ".import_fix.bak"
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"バックアップを作成しました: {backup_file}")
    
    # 正規表現で先頭のインポート文を確認
    imports = re.findall(r'^import [^;]+|^from [^;]+', content, re.MULTILINE)
    
    has_logging_import = False
    for imp in imports:
        if "import logging" in imp:
            has_logging_import = True
            break
    
    # インポートがない場合は追加
    if not has_logging_import:
        # ファイルの先頭に追加する場合
        if content.startswith('import ') or content.startswith('from '):
            # 既存のインポート文の前に追加
            content = "import logging\n\n" + content
        else:
            # ファイルの先頭に追加
            first_line_end = content.find('\n')
            if first_line_end >= 0:
                content = content[:first_line_end+1] + "import logging\n" + content[first_line_end+1:]
            else:
                content = "import logging\n" + content
    
    # ファイルを保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にloggingインポートを追加しました")
    
    return True

def check_import_exists(filepath, module_name):
    """指定したファイルに特定のモジュールのインポート文があるか確認"""
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    with open(filepath, 'r') as f:
        content = f.readlines()
    
    for line in content:
        if line.strip().startswith('import ') and module_name in line:
            return True
        if line.strip().startswith('from ') and f"import {module_name}" in line:
            return True
    
    return False

if __name__ == "__main__":
    # 修正
    radar_fixed = fix_radar_chart_dialog_import()
    staged_fixed = fix_staged_target_tab_import()
    
    # 確認
    radar_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    staged_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    print("\n検証結果:")
    print(f"radar_chart_dialog.py にloggingインポートがあるか: {check_import_exists(radar_path, 'logging')}")
    print(f"staged_target_tab.py にloggingインポートがあるか: {check_import_exists(staged_path, 'logging')}")
