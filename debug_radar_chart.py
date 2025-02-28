#!/usr/bin/env python3
"""レーダーチャートダイアログのデバッグコード追加"""

import os

def add_radar_debug():
    """レーダーチャートダイアログにデバッグコードを追加"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup = filepath + ".debug.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ: {backup}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # インポート追加
    if "import traceback" not in content:
        import_pos = content.find("import")
        if import_pos >= 0:
            # インポート文の後に追加
            import_end = content.find("\n\n", import_pos)
            if import_end < 0:
                import_end = content.find("class", import_pos)
            
            if import_end > 0:
                debug_imports = "\nimport traceback\nimport logging\n"
                content = content[:import_end] + debug_imports + content[import_end:]
    
    # __init__メソッドにデバッグコード追加
    if "def __init__" in content:
        init_pos = content.find("def __init__")
        init_body_start = content.find(":", init_pos) + 1
        
        # ロギング設定を追加
        debug_init = """
        # ロギング設定
        self.logger = logging.getLogger('RadarChartDialog')
        self.logger.debug(f"RadarChartDialog初期化: {len(stage_data)}個のステージデータ")
        
        # 受け取ったデータを詳細にログ出力
        for i, stage in enumerate(stage_data):
            self.logger.debug(f"ステージ{i+1}: {stage.get('name', '名前なし')} - スキル数: {len(stage.get('skills', []))}")
            for j, skill in enumerate(stage.get('skills', [])):
                self.logger.debug(f"  スキル{j+1}: 名前={skill.get('name', '名前なし')}, 値={skill.get('value', 'なし')}")
        """
        
        content = content[:init_body_start] + debug_init + content[init_body_start:]
    
    # setup_chartメソッドにデバッグコード追加
    if "def setup_chart" in content:
        setup_pos = content.find("def setup_chart")
        setup_body_start = content.find(":", setup_pos) + 1
        
        # ロギング追加
        debug_setup = """
        self.logger.debug("setup_chart メソッド開始")
        """
        
        content = content[:setup_body_start] + debug_setup + content[setup_body_start:]
    
    # draw_chartメソッドにデバッグコード追加（特にデータ不足の検出部分）
    if "def draw_chart" in content:
        draw_pos = content.find("def draw_chart")
        draw_end = content.find("def ", draw_pos + 1)
        if draw_end < 0:
            draw_end = len(content)
        
        draw_content = content[draw_pos:draw_end]
        
        # データ検証を追加
        if "if not skills:" in draw_content:
            no_skills_pos = draw_content.find("if not skills:")
            warning_pos = draw_content.find("logging.warning", no_skills_pos)
            
            if warning_pos > 0:
                # 警告メッセージを詳細化
                new_warning = """            logging.warning(f"表示するスキルがありません (データ: {skills})")
            self.logger.debug(f"Skills型: {type(skills)}, 内容: {skills}")
            if isinstance(skills, list) and len(skills) == 0:
                self.logger.debug("スキルリストが空です")
            # スタックトレースを表示して呼び出し元を特定
            self.logger.debug("呼び出し元スタックトレース:")
            for line in traceback.format_stack()[:-1]:
                self.logger.debug(line.strip())"""
                
                # 置換
                old_warning_end = draw_content.find("\n", warning_pos)
                new_draw = draw_content[:warning_pos] + new_warning + draw_content[old_warning_end:]
                
                content = content[:draw_pos] + new_draw + content[draw_end:]
    
    # 保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にデバッグコードを追加しました")
    return True

if __name__ == "__main__":
    add_radar_debug()
