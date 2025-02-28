#!/usr/bin/env python3
"""相対インポートに修正"""

import os

def use_relative_import():
    """相対インポートに修正"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 既存のインポート文を全て削除
    if "SettingsTab" in content:
        import_lines = []
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "SettingsTab" in line and "import" in line:
                import_lines.append(i)
        
        # 削除は後ろから
        for i in sorted(import_lines, reverse=True):
            lines.pop(i)
        
        # 正しいインポート文を追加
        for i, line in enumerate(lines):
            if line.startswith("import") or "import" in line:
                lines.insert(i+1, "from .components.settings_tab import SettingsTab")
                break
        
        content = "\n".join(lines)
    
    # 変更保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}のインポートを相対パスに修正しました")
    return True

if __name__ == "__main__":
    use_relative_import()
