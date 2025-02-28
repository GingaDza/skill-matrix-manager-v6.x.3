#!/usr/bin/env python3
"""メインウィンドウに設定タブを追加"""

import os

def add_settings_tab_to_main():
    """メインウィンドウに設定タブを追加"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup = filepath + ".settings.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ: {backup}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 設定タブをインポート
    if "from .components.settings_tab import SettingsTab" not in content and "from .ui.components.settings_tab import SettingsTab" not in content:
        # インポート部分を見つける
        import_section = content.find("import")
        last_import = content.find("\n\nclass", import_section)
        
        # 相対インポート用のパス
        relative_path = ""
        if "from .ui." in content:
            relative_path = ".ui."
        
        # インポート追加
        import_code = f"\nfrom {relative_path}components.settings_tab import SettingsTab"
        content = content[:last_import] + import_code + content[last_import:]
    
    # 設定タブを追加（まだ追加されていない場合）
    if "self.tabs.addTab(SettingsTab(self)" not in content and "settings_tab = SettingsTab(self)" not in content:
        # タブ初期化を探す
        init_ui = content.find("def init_ui")
        if init_ui > 0:
            # タブ追加部分を探す
            tabs_init = content.find("self.tabs = ", init_ui)
            if tabs_init > 0:
                # 最後のタブ追加を見つける
                last_add_tab = content.rfind("self.tabs.addTab(", tabs_init, content.find("def ", tabs_init + 10) if content.find("def ", tabs_init + 10) > 0 else len(content))
                if last_add_tab > 0:
                    # 行の終わりを探す
                    line_end = content.find("\n", last_add_tab)
                    
                    # 設定タブ追加
                    settings_tab_code = """
        # 設定タブ
        settings_tab = SettingsTab(self)
        self.tabs.addTab(settings_tab, "設定")
"""
                    content = content[:line_end+1] + settings_tab_code + content[line_end+1:]
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}に設定タブを追加しました")
    return True

if __name__ == "__main__":
    add_settings_tab_to_main()
