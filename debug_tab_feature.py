#!/usr/bin/env python3
"""タブ機能のデバッグログを収集"""

import os
import datetime

def collect_debug_info():
    """タブ機能のデバッグ情報を収集"""
    # ファイルパス
    main_window_path = "src/skill_matrix_manager/ui/main_window.py"
    settings_tab_path = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    # ログファイル
    log_file = f"tab_debug_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    with open(log_file, 'w') as f:
        f.write(f"=== タブ機能デバッグログ ===\n")
        f.write(f"日時: {datetime.datetime.now()}\n\n")
        
        # メインウィンドウ確認
        f.write("=== メインウィンドウ確認 ===\n")
        if os.path.exists(main_window_path):
            with open(main_window_path, 'r') as main_f:
                content = main_f.read()
                f.write(f"ファイルサイズ: {len(content)} bytes\n")
                
                # 重要な機能の有無確認
                f.write(f"add_category_tabメソッド: {'あり' if 'def add_category_tab' in content else 'なし'}\n")
                f.write(f"_save_tab_configメソッド: {'あり' if 'def _save_tab_config' in content else 'なし'}\n")
                f.write(f"jsonモジュールのインポート: {'あり' if 'import json' in content else 'なし'}\n")
        else:
            f.write(f"ファイルが見つかりません: {main_window_path}\n")
        
        # 設定タブ確認
        f.write("\n=== 設定タブ確認 ===\n")
        if os.path.exists(settings_tab_path):
            with open(settings_tab_path, 'r') as settings_f:
                content = settings_f.read()
                f.write(f"ファイルサイズ: {len(content)} bytes\n")
                
                # 重要な機能の有無確認
                f.write(f"add_new_tabメソッド: {'あり' if 'def add_new_tab' in content else 'なし'}\n")
                f.write(f"add_tab_btnの定義: {'あり' if 'self.add_tab_btn' in content else 'なし'}\n")
                f.write(f"QMessageBoxのインポート: {'あり' if 'QMessageBox' in content else 'なし'}\n")
        else:
            f.write(f"ファイルが見つかりません: {settings_tab_path}\n")
        
        # タブ設定ファイル確認
        f.write("\n=== タブ設定ファイル確認 ===\n")
        if os.path.exists("tab_config.json"):
            with open("tab_config.json", 'r') as conf_f:
                f.write(f"内容:\n{conf_f.read()}\n")
        else:
            f.write("ファイルが見つかりません: tab_config.json\n")
    
    print(f"デバッグ情報を {log_file} に保存しました")
    return log_file

if __name__ == "__main__":
    collect_debug_info()
