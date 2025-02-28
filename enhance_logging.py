#!/usr/bin/env python3
"""ロギングを強化してデバッグしやすくする"""

import os

def add_debug_logging():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    # __init__メソッドにデバッグ出力を追加
    if "def __init__" in content:
        init_part = content.split("def __init__")[1].split("def")[0]
        modified_init = init_part.replace(
            "self.stages_data = stages_data", 
            "self.stages_data = stages_data\n        self.logger.debug(f\"受け取ったデータ: {stages_data}\")\n        # データ構造を確認\n        for i, stage in enumerate(stages_data):\n            self.logger.debug(f\"  ステージ {i}: {stage.keys()}\")"
        )
        content = content.replace(init_part, modified_init)
        
    # draw_radar_chartメソッドにエラーキャッチを追加
    if "def draw_radar_chart" in content:
        method_part = content.split("def draw_radar_chart")[1].split("def")[0]
        new_method = """    def draw_radar_chart(self):
        """レーダーチャートを描画"""
        try:
            self.logger.debug("レーダーチャートの描画開始")
            
            # データ構造を確認
            if not self.stages_data:
                self.logger.warning("stages_dataがありません")
                return
                
            self.logger.debug(f"stages_dataの長さ: {len(self.stages_data)}")
            self.logger.debug(f"最初のステージのキー: {self.stages_data[0].keys() if self.stages_data else '空'}")
            
            # 'skills'キーを使用
            if not self.stages_data or 'skills' not in self.stages_data[0]:
                self.logger.warning("skillsキーが見つかりません - 描画をスキップします")
                return
            
            skills_data = self.stages_data[0]['skills']
            self.logger.debug(f"スキルデータ: {skills_data}")
            
            # 各ステージのタブを作成
            for i, stage in enumerate(self.stages_data):
                self.logger.debug(f"ステージ{i+1}のタブを準備")
                
                # タブ内にキャンバスを配置
                tab = QWidget()
                layout = QVBoxLayout()
                
                # ステージ名を表示
                stage_name = stage.get('name', f'Stage {i+1}')
                label = QLabel(stage_name)
                label.setAlignment(Qt.AlignCenter)
                layout.addWidget(label)
                
                # キャンバスを配置
                canvas = self.canvas_list[i]
                layout.addWidget(canvas)
                
                tab.setLayout(layout)
                self.tabs.addTab(tab, stage_name)
                
                # チャートを描画
                skills = stage.get('skills', [])
                self.draw_chart(i, skills)
                
            self.logger.debug("レーダーチャートの描画完了")
        except Exception as e:
            self.logger.error(f"レーダーチャート描画でエラー: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
"""
        # docstringのエスケープ
        new_method = new_method.replace('"""レーダーチャートを描画"""', '\"\"\"レーダーチャートを描画\"\"\"')
        
        content = content.replace("def draw_radar_chart" + method_part, new_method)
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}にデバッグロギングを追加しました")
    return True

add_debug_logging()
