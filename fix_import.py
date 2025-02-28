#!/usr/bin/env python3
"""インポートエラーを修正"""

import os

def fix_settings_import():
    """設定タブのインポートパスを修正"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup = filepath + ".import.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ: {backup}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 誤ったインポート文を修正
    if "from components.settings_tab import SettingsTab" in content:
        content = content.replace(
            "from components.settings_tab import SettingsTab", 
            "from src.skill_matrix_manager.ui.components.settings_tab import SettingsTab"
        )
    elif "from .components.settings_tab import SettingsTab" in content:
        pass  # 既に相対パスで正しい
    elif "from .ui.components.settings_tab import SettingsTab" in content:
        pass  # 既に相対パスで正しい
    elif "SettingsTab" in content and not any([
        "from components.settings_tab import SettingsTab" in content,
        "from .components.settings_tab import SettingsTab" in content,
        "from src.skill_matrix_manager.ui.components.settings_tab import SettingsTab" in content
    ]):
        # インポート文がないのにSettingsTabを使用している場合、適切なインポートを追加
        import_section = content.find("import")
        last_import = content.find("\n\nclass", import_section)
        
        import_code = "\nfrom src.skill_matrix_manager.ui.components.settings_tab import SettingsTab"
        content = content[:last_import] + import_code + content[last_import:]
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}のインポート文を修正しました")
    return True

if __name__ == "__main__":
    fix_settings_import()
