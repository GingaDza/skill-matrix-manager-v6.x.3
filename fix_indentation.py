#!/usr/bin/env python3
"""インデントエラーを修正"""

import os

def fix_indentation_error():
    """staged_target_tab.pyのインデントエラーを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ作成
    backup = filepath + ".indent.bak"
    with open(filepath, 'r') as src:
        with open(backup, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ作成: {backup}")
    
    # 行ごとに読み込み
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # エラー行を特定
    error_line = None
    for i, line in enumerate(lines):
        if "dialog.exec_()" in line.strip():
            error_line = i
            break
    
    if error_line is not None:
        print(f"エラー行 {error_line + 1}: {lines[error_line].rstrip()}")
        
        # エラー前後の行を分析してインデントを修正
        before = error_line - 1
        while before >= 0 and not lines[before].strip():
            before -= 1
        
        if before >= 0:
            # 正しいインデントを特定
            current_indent = len(lines[error_line]) - len(lines[error_line].lstrip())
            correct_indent = len(lines[before]) - len(lines[before].lstrip())
            
            print(f"現在のインデント: {current_indent}, 正しいインデント: {correct_indent}")
            
            # インデントを修正
            lines[error_line] = ' ' * correct_indent + lines[error_line].lstrip()
            
            print(f"修正後: {lines[error_line].rstrip()}")
    
    # 修正を保存
    with open(filepath, 'w') as f:
        f.writelines(lines)
    
    print(f"{filepath}のインデントを修正しました")
    
    # 構文チェック
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        compile(content, filepath, 'exec')
        print(f"{filepath}の構文チェック成功")
        return True
    except SyntaxError as e:
        print(f"構文エラー: {e}")
        return False

# show_radar_chartメソッド全体の整形
def format_radar_chart_method():
    """show_radar_chartメソッド全体を整形"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # show_radar_chartメソッドの位置を特定
    method_start = content.find("def show_radar_chart")
    if method_start < 0:
        print("show_radar_chartメソッドが見つかりません")
        return False
    
    # 次のメソッドまでの範囲を取得
    next_method = content.find("\n    def ", method_start + 1)
    if next_method < 0:
        next_method = len(content)
    
    # メソッド全体を取得
    method_content = content[method_start:next_method]
    
    # メソッドの修正版を作成
    corrected_method = """    def show_radar_chart(self):
        """レーダーチャートを表示するダイアログを開く"""
        try:
            self.logger.debug("チャートデータ取得開始")
            
            # テストデータを使用
            use_test_data = True
            if use_test_data:
                logging.debug("テストデータを使用します")
                stages = self.generate_test_data(num_skills=5)
            else:
                logging.debug("実データを使用します")
                stages = self.get_stage_skills()
                
            self.logger.debug(f"ステージデータ: {len(stages)}段階")
            
            # ステージデータの変換
            stages_data = []
            
            for i, stage in enumerate(stages):
                stage_name = stage.get('name', f'段階{i+1}')
                stage_skills = stage.get('skills', [])
                
                self.logger.debug(f"  段階{i+1}: {stage_name} ({len(stage_skills)}スキル)")
                
                stages_data.append({
                    'name': stage_name,
                    'skills': stage_skills
                })
            
            # スキルデータのデバッグ出力
            logging.debug(f"RadarChartDialogに渡すデータ: {len(stages_data)}ステージ")
            
            # データ確認
            for i, stage in enumerate(stages_data):
                skills = stage.get('skills', [])
                logging.debug(f"渡すステージ{i+1}: {stage.get('name', '名前なし')} - スキル数: {len(skills)}")
                if not skills:
                    logging.warning(f"ステージ{i+1}のスキルが空です")
            
            self.logger.info(f"チャートダイアログの表示: {len(stages_data)}ステージ")
            dialog = RadarChartDialog(self, stages_data)
            dialog.exec_()
        except Exception as e:
            self.logger.error(f"レーダーチャート表示エラー: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"レーダーチャート表示中にエラーが発生しました: {str(e)}")
"""
    
    # docstringのエスケープ
    corrected_method = corrected_method.replace('"""レーダーチャートを表示するダイアログを開く"""', '\"\"\"レーダーチャートを表示するダイアログを開く\"\"\"')
    
    # メソッドを置き換え
    new_content = content[:method_start] + corrected_method + content[next_method:]
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"{filepath}のshow_radar_chartメソッドを全体的に修正しました")
    return True

if __name__ == "__main__":
    # まずはインデントのみ修正
    if fix_indentation_error():
        # さらに全体的に整形（オプション）
        format_radar_chart_method()
    
    print("\nアプリケーションを再起動してください。")
