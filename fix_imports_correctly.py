#!/usr/bin/env python3
"""正しいインポートパスを設定"""

import os

def fix_imports():
    """正しいインポートパスを設定"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 設定タブのインポートを確認
    settings_import = None
    
    # 可能なインポート文を探す
    possible_imports = [
        "from .components.settings_tab import SettingsTab",
        "from src.skill_matrix_manager.ui.components.settings_tab import SettingsTab",
        "from components.settings_tab import SettingsTab"
    ]
    
    for imp in possible_imports:
        if imp in content:
            settings_import = imp
            break
    
    # インポート文がなければ追加
    if settings_import is None:
        # インポート部分を見つける
        import_section = content.find("import")
        last_import = content.find("\n\nclass", import_section)
        
        # 正しいインポートを追加（相対パスを使用）
        import_code = "\nfrom .components.settings_tab import SettingsTab"
        content = content[:last_import] + import_code + content[last_import:]
    # 間違ったインポートの場合は修正
    elif settings_import == "from components.settings_tab import SettingsTab":
        content = content.replace(
            "from components.settings_tab import SettingsTab",
            "from .components.settings_tab import SettingsTab"
        )
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}のインポートパスを修正しました")
    return True

if __name__ == "__main__":
    fix_imports()
