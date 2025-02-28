#!/usr/bin/env python3
"""イベント接続を明示的に修正"""

import os

def fix_tab_button_connection():
    """タブ追加ボタンの接続を修正"""
    settings_file = "src/skill_matrix_manager/ui/components/settings_tab.py"
    
    if not os.path.exists(settings_file):
        print(f"エラー: {settings_file}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # イベント接続コードの挿入位置を特定
    # init_uiメソッド内の最後の行を探す
    init_ui_start = content.find("def init_ui")
    init_ui_end = content.find("def ", init_ui_start + 1)
    
    if init_ui_start > 0 and init_ui_end > 0:
        init_ui_body = content[init_ui_start:init_ui_end]
        
        # イベント接続コードがあるか確認
        if "self.add_tab_btn.clicked.connect(self.add_new_tab)" not in init_ui_body:
            # 最後の行を見つける（インデントが減る場所）
            last_line_pos = -1
            lines = init_ui_body.split('\n')
            
            for i in range(len(lines)-1, 0, -1):
                if lines[i].strip() and not lines[i].startswith(' ' * 8):
                    break
                if lines[i].strip() and lines[i].startswith(' ' * 8):
                    last_line_pos = i
                    break
            
            if last_line_pos >= 0:
                # 明示的なイベント接続コードを追加
                connection_code = """
        # 明示的なイベント接続
        print("新規タブ追加ボタンのクリックイベントを接続します")
        self.add_tab_btn.clicked.connect(self.add_new_tab)
        print("イベント接続完了")"""
                
                lines.insert(last_line_pos + 1, connection_code)
                new_init_ui = '\n'.join(lines)
                
                # 更新
                content = content[:init_ui_start] + new_init_ui + content[init_ui_end:]
                
                # 保存
                with open(settings_file, 'w') as f:
                    f.write(content)
                
                print(f"{settings_file}のイベント接続を修正しました")
                return True
    
    print(f"{settings_file}のイベント接続は既に設定されているか、修正できませんでした")
    return False

if __name__ == "__main__":
    fix_tab_button_connection()
