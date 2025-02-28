#!/usr/bin/env python3
"""メインウィンドウを完全に作り直し"""

import os

def recreate_main_window():
    """メインウィンドウファイルを作り直す"""
    filepath = "src/skill_matrix_manager/ui/main_window.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # オリジナルをバックアップ
    backup = filepath + ".original.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"オリジナルをバックアップ: {backup}")
    
    # オリジナルの内容を取得
    with open(backup, 'r') as f:
        original = f.read()
    
    # 必要なインポートを追加して再構築
    lines = original.split('\n')
    
    # 新しい内容を構築
    new_content = []
    
    # 最初のインポートの前に必要なインポートを追加
    import_section = False
    import_added = False
    
    for line in lines:
        if line.startswith('import') or line.startswith('from'):
            import_section = True
            
            # 最初のインポート行の前に追加
            if not import_added:
                new_content.append('import json')
                new_content.append('from .components.settings_tab import SettingsTab')
                import_added = True
        
        # 既存のSettingsTabインポートをスキップ
        if "settings_tab" in line and "import" in line:
            continue
        
        # jsonインポートもスキップ
        if "import json" in line:
            continue
        
        # 他の行はそのまま追加
        new_content.append(line)
    
    # タブ追加メソッドを探す
    if "def add_category_tab" not in original:
        # クラスの終わりを見つける（if __name__の前）
        for i, line in enumerate(new_content):
            if line.startswith('if __name__'):
                # メソッドを追加
                tab_methods = [
                    '    def add_category_tab(self, category_name):',
                    '        """カテゴリータブを追加"""',
                    '        # 既存タブ確認',
                    '        for i in range(self.tabs.count()):',
                    '            if self.tabs.tabText(i) == category_name:',
                    '                self.tabs.setCurrentIndex(i)',
                    '                return True',
                    '        ',
                    '        # 新規タブ作成',
                    '        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel',
                    '        new_tab = QWidget()',
                    '        layout = QVBoxLayout(new_tab)',
                    '        label = QLabel(f"{category_name}タブの内容")',
                    '        layout.addWidget(label)',
                    '        ',
                    '        # タブに追加',
                    '        self.tabs.addTab(new_tab, category_name)',
                    '        self.tabs.setCurrentIndex(self.tabs.count() - 1)',
                    '        ',
                    '        # 設定保存',
                    '        self._save_tab_config()',
                    '        return True',
                    '    ',
                    '    def _save_tab_config(self):',
                    '        """タブ設定を保存"""',
                    '        try:',
                    '            tabs = []',
                    '            for i in range(self.tabs.count()):',
                    '                tab_name = self.tabs.tabText(i)',
                    '                tabs.append({"name": tab_name, "type": "category"})',
                    '            ',
                    '            with open("tab_config.json", "w", encoding="utf-8") as f:',
                    '                json.dump({"tabs": tabs}, f, ensure_ascii=False, indent=2)',
                    '            print("タブ設定を保存しました")',
                    '        except Exception as e:',
                    '            print(f"タブ設定保存エラー: {e}")',
                    '    '
                ]
                # メソッドを挿入
                for j, method_line in enumerate(tab_methods):
                    new_content.insert(i + j, method_line)
                break
    
    # 設定タブを追加
    setup_tabs = False
    settings_tab_added = False
    
    for i, line in enumerate(new_content):
        if "self.tabs = " in line:
            setup_tabs = True
        
        if setup_tabs and "self.tabs.addTab" in line and "settings_tab" not in line and not settings_tab_added:
            # 最後のタブ追加を見つける
            last_tab_index = i
            for j in range(i+1, len(new_content)):
                if "self.tabs.addTab" in new_content[j]:
                    last_tab_index = j
                elif "self.tabs.setCurrentIndex" in new_content[j]:
                    break
            
            # 設定タブを追加
            settings_tab_code = [
                '        # 設定タブ',
                '        settings_tab = SettingsTab(self)',
                '        self.tabs.addTab(settings_tab, "設定")'
            ]
            
            # タブを挿入
            for j, tab_line in enumerate(settings_tab_code):
                new_content.insert(last_tab_index + j + 1, tab_line)
            
            settings_tab_added = True
            break
    
    # 保存
    with open(filepath, 'w') as f:
        f.write('\n'.join(new_content))
    
    print(f"{filepath}を完全に作り直しました")
    return True

if __name__ == "__main__":
    recreate_main_window()
