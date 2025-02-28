#!/usr/bin/env python3
"""レーダーチャートのデバッグコードを修正"""

import os

def fix_radar_chart_dialog():
    """radar_chart_dialog.pyのデバッグコードを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 初期化メソッドにデバッグコード追加
    init_pos = content.find("def __init__")
    if init_pos >= 0:
        # メソッド本体の開始位置を見つける
        init_body_start = content.find(":", init_pos) + 1
        
        # 既存のデバッグコードがあるかチェック
        if "self.logger" not in content[init_pos:init_pos+200]:  # 初期化メソッドの最初の部分を確認
            # デバッグコードを追加
            debug_code = """
        # デバッグ用ロギング設定
        self.logger = logging.getLogger('RadarChartDialog')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(f"RadarChartDialog初期化: {len(stage_data)}個のステージデータ")
        
        # ステージデータの詳細をログ出力
        for i, stage in enumerate(stage_data):
            self.logger.debug(f"ステージ {i+1}: {stage.get('name', '名前なし')}")
            skills = stage.get('skills', [])
            self.logger.debug(f"  スキル数: {len(skills)}")
            for j, skill in enumerate(skills):
                self.logger.debug(f"    スキル {j+1}: {skill.get('name', '不明')} = {skill.get('value', '不明')}")
        """
            
            # コードを挿入
            content = content[:init_body_start] + debug_code + content[init_body_start:]
    
    # draw_chartメソッドにスキルデータのデバッグ追加
    draw_pos = content.find("def draw_chart")
    if draw_pos >= 0:
        # メソッド本体の開始位置を見つける
        draw_body_start = content.find(":", draw_pos) + 1
        
        # 既存のデバッグがあるか確認
        if "self.logger.debug" not in content[draw_pos:draw_pos+100]:
            # デバッグコードを追加
            debug_code = """
        self.logger.debug(f"draw_chart開始: スキル数={len(skills)}")
        self.logger.debug(f"スキル名リスト: {[skill.get('name', '不明') for skill in skills]}")
        
        # スキルデータが空かチェック
        if not skills:
            self.logger.warning(f"スキルデータが空です。詳細: {skills}")
        """
            
            # コードを挿入
            content = content[:draw_body_start] + debug_code + content[draw_body_start:]
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にデバッグコードを追加しました")
    return True

def add_test_data_to_staged_target():
    """テストデータ生成メソッドを追加"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # テストデータ生成メソッドが既に存在するか確認
    if "def generate_test_data" not in content:
        # クラス終了位置を探す
        class_end = content.find("if __name__")
        if class_end < 0:
            # クラス終了位置が見つからない場合はファイル末尾
            class_end = len(content)
        
        # テストデータ生成メソッドを追加
        test_data_method = """
    def generate_test_data(self, num_skills=5):
        \"\"\"テストデータを生成\"\"\"
        logging.debug("テストデータ生成")
        import random
        
        # スキル名のリスト
        skill_names = [
            "Python", "JavaScript", "SQL", "データ分析", "機械学習",
            "UIデザイン", "APIテスト", "CI/CD", "サーバー管理", "セキュリティ"
        ]
        
        # 使用するスキル名を選択
        selected_skills = skill_names[:num_skills] if num_skills <= len(skill_names) else skill_names
        
        # 段階名と期間
        stages = [
            {"name": "現在", "months": 0},
            {"name": "3ヶ月後", "months": 3},
            {"name": "6ヶ月後", "months": 6},
            {"name": "9ヶ月後", "months": 9},
            {"name": "目標", "months": 12}
        ]
        
        # 各段階のスキルデータを生成
        stage_data = []
        base_values = [random.randint(1, 3) for _ in range(len(selected_skills))]
        
        for i, stage in enumerate(stages):
            # 進捗に応じて値を増加
            progress_factor = i / (len(stages) - 1)  # 0から1の範囲
            
            skills = []
            for j, skill_name in enumerate(selected_skills):
                # 基本値から段階に応じて値を増加（最大5）
                base_val = base_values[j]
                value = min(5, base_val + (5 - base_val) * progress_factor)
                # 小数点以下を切り捨て
                value = int(value)
                
                skills.append({
                    "name": skill_name,
                    "value": value
                })
            
            stage_data.append({
                "name": stage["name"],
                "months": stage["months"],
                "skills": skills
            })
        
        logging.debug(f"生成したテストデータ: {stage_data}")
        return stage_data
"""
        
        # メソッド追加
        content = content[:class_end] + test_data_method + content[class_end:]
    
    # show_radar_chartメソッドにテストデータ使用コードを追加
    chart_pos = content.find("def show_radar_chart")
    if chart_pos >= 0:
        # テストデータの使用部分を見つける
        data_pos = content.find("stages = ", chart_pos)
        if data_pos >= 0:
            # 既存のステージ取得コードを探す
            stage_end = content.find("\n", data_pos)
            
            # テストデータ使用コードを作成
            test_data_code = """
        # テストデータを使用
        use_test_data = True
        if use_test_data:
            logging.debug("テストデータを使用します")
            stages = self.generate_test_data(num_skills=5)
        else:
            logging.debug("実データを使用します")
            stages = self.get_stage_skills()
        """
            
            # 既存コードを置換
            content = content[:data_pos] + test_data_code + content[stage_end:]
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にテストデータ生成メソッドを追加しました")
    return True

if __name__ == "__main__":
    fix_radar_chart_dialog()
    add_test_data_to_staged_target()
