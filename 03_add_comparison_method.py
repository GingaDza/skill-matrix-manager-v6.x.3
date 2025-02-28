#!/usr/bin/env python3
"""比較チャート表示メソッドを追加"""
import os

filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"

# ファイルを読み込む
with open(filepath, 'r') as f:
    content = f.read()

# 比較チャート表示メソッドを追加
comparison_method = """
    def show_comparison_chart(self):
        \"\"\"現在値と目標値を比較するレーダーチャートを表示\"\"\"
        try:
            self.logger.debug("比較チャート表示")
            
            # 選択された段階を取得
            selected_stages = []
            for i, checkbox in enumerate(self.stage_checkboxes):
                if checkbox.isChecked():
                    selected_stages.append(i)
            
            if not selected_stages:
                QMessageBox.warning(self, "警告", "表示する段階を1つ以上選択してください")
                return
            
            # テストデータを使用
            stages = self.generate_test_data()
            
            # 選択された段階のみを抽出
            selected_data = [stages[i] for i in selected_stages]
            
            self.logger.info(f"比較チャートダイアログの表示: {len(selected_data)}ステージ")
            dialog = RadarChartDialog(self, selected_data, compare_mode=True)
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"比較チャート表示エラー: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "エラー", f"比較チャート表示中にエラーが発生しました: {str(e)}")
"""

# ファイルの末尾に追加
content += comparison_method

# 保存
with open(filepath, 'w') as f:
    f.write(content)

print("比較チャート表示メソッドの追加が完了しました。")
