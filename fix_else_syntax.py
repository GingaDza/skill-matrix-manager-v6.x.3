#!/usr/bin/env python3
"""else構文エラーを修正するスクリプト"""

import os

def fix_syntax_error():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップを作成
    backup = filepath + ".else_fix.bak"
    with open(filepath, 'r') as f:
        content = f.read()
        
    with open(backup, 'w') as f:
        f.write(content)
    print(f"バックアップ作成: {backup}")
    
    # 行ごとに読み込み
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # エラー行の前後を確認
    error_line = 466 - 1  # 0ベース
    
    if 0 <= error_line < len(lines):
        print(f"エラー行 ({error_line+1}): '{lines[error_line].strip()}'")
        
        # 前後の行を確認
        start = max(0, error_line - 5)
        end = min(len(lines), error_line + 5)
        
        print("\nエラー周辺の行:")
        for i in range(start, end):
            prefix = ">" if i == error_line else " "
            print(f"{prefix} {i+1}: '{lines[i].strip()}'")
        
        # 単純な修正方法: elseブロック全体を削除するか、対応するifを挿入
        # ここでは、問題のあるelse行から適切な位置までを削除する
        # 約450〜470行あたりにshow_radar_chartメソッドがあると仮定
        
        # show_radar_chartメソッドを探す
        method_start = -1
        for i, line in enumerate(lines):
            if "def show_radar_chart" in line:
                method_start = i
                break
        
        if method_start >= 0:
            # 次のメソッドを探す
            method_end = len(lines)
            for i in range(method_start + 1, len(lines)):
                if line.strip().startswith("def "):
                    method_end = i
                    break
            
            # メソッドの全体を取得
            method_lines = lines[method_start:method_end]
            method_content = ''.join(method_lines)
            
            print(f"\nshow_radar_chartメソッド: 行 {method_start+1} - {method_end}")
            
            # 整形済みの代替メソッド
            fixed_method = """    def show_radar_chart(self):
        \"\"\"レーダーチャートを表示するダイアログを開く\"\"\"
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
            
            self.logger.info(f"チャートダイアログの表示: {len(stages_data)}ステージ")
            dialog = RadarChartDialog(self, stages_data)
            dialog.exec_()
        except Exception as e:
            self.logger.error(f"レーダーチャート表示エラー: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"レーダーチャート表示中にエラーが発生しました: {str(e)}")
"""
            
            # メソッドを置き換え
            new_content = ''.join(lines[:method_start]) + fixed_method + ''.join(lines[method_end:])
            
            # 保存
            with open(filepath, 'w') as f:
                f.write(new_content)
            
            print(f"{filepath}のshow_radar_chartメソッドを修正しました")
            return True
        else:
            print("show_radar_chartメソッドが見つかりませんでした")
    else:
        print("指定された行番号が範囲外です")
    
    return False

if __name__ == "__main__":
    fix_syntax_error()
