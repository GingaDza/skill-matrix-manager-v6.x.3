#!/usr/bin/env python3
"""構文エラーの修正"""

import os

def fix_staged_target_tab_syntax():
    """staged_target_tab.pyの構文エラーを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ
    backup = filepath + ".syntax.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ: {backup}")
    
    # ファイルを行ごとに読み込む
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 括弧の不一致を修正
    # ここでは簡単な修正方法としてファイル全体を確認
    bracket_count = 0  # カウンターで括弧のバランスをチェック
    problem_lines = []
    
    for i, line in enumerate(lines):
        for char in line:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count < 0:
                    # 閉じ括弧が多すぎる場合
                    problem_lines.append((i, line))
                    bracket_count = 0  # リセット
    
    # 問題がある場合、generate_test_dataメソッド全体を置き換える
    if problem_lines:
        print(f"構文エラーが見つかりました: {len(problem_lines)}行")
        
        # generate_test_dataメソッドの開始と終了を見つける
        start_line = -1
        end_line = -1
        
        for i, line in enumerate(lines):
            if "def generate_test_data" in line:
                start_line = i
            elif start_line >= 0 and line.strip().startswith("def "):
                end_line = i
                break
        
        if start_line >= 0:
            if end_line < 0:
                end_line = len(lines)
            
            # 修正済みのメソッドを作成
            fixed_method = """    def generate_test_data(self, num_skills=5):
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
            
            # メソッドを置き換える
            lines[start_line:end_line] = fixed_method.splitlines(True)
    
    # show_radar_chartメソッドのテストデータ使用部分を修正
    for i, line in enumerate(lines):
        if "use_test_data = True" in line:
            # このブロックの開始行を見つける
            start_block = i
            # ブロックの終了を見つける
            for j in range(i, len(lines)):
                if "stages = self.get_stage_skills()" in lines[j]:
                    end_block = j + 1
                    break
            else:
                end_block = i + 10  # 安全のための制限
            
            # 修正されたブロックを作成
            fixed_block = """        # テストデータを使用
        use_test_data = True
        if use_test_data:
            logging.debug("テストデータを使用します")
            stages = self.generate_test_data(num_skills=5)
        else:
            logging.debug("実データを使用します")
            stages = self.get_stage_skills()
"""
            
            # ブロックを置き換える
            lines[start_block:end_block] = fixed_block.splitlines(True)
            break
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.writelines(lines)
    
    print(f"{filepath}の構文エラーを修正しました")
    return True

def check_all_files():
    """すべての関連ファイルをチェック"""
    files = [
        "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py",
        "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    ]
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"エラー: {filepath}が見つかりません")
            continue
        
        # ファイルの構文をチェック
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Pythonで構文チェック（コンパイルのみ）
            compile(content, filepath, 'exec')
            print(f"{filepath}の構文は正常です")
        except SyntaxError as e:
            print(f"{filepath}に構文エラーがあります: {e}")
            
            # バックアップ作成
            backup = filepath + ".error.bak"
            with open(filepath, 'r') as src:
                with open(backup, 'w') as dst:
                    dst.write(content)
            print(f"エラーファイルをバックアップ: {backup}")
            
            # エラー行の前後を表示
            lines = content.splitlines()
            error_line = e.lineno - 1
            start = max(0, error_line - 5)
            end = min(len(lines), error_line + 5)
            
            print("エラー周辺の行:")
            for i in range(start, end):
                prefix = ">" if i == error_line else " "
                print(f"{prefix} {i+1:4d}: {lines[i]}")

if __name__ == "__main__":
    fix_staged_target_tab_syntax()
    check_all_files()
