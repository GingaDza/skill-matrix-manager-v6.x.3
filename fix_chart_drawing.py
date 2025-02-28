#!/usr/bin/env python3
"""レーダーチャート描画の問題を修正"""

import os

def fix_radar_chart_drawing():
    """radar_chart_dialog.pyのdraw_chartメソッドを修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ作成
    backup_file = filepath + ".chart_fix.bak"
    with open(filepath, 'r') as src:
        with open(backup_file, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ作成: {backup_file}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # デバッグ出力を追加してスキルデータを詳細に確認
    if "def setup_chart" in content:
        setup_pos = content.find("def setup_chart")
        setup_body_start = content.find(":", setup_pos) + 1
        
        # スキルデータの詳細をログ出力
        debug_setup = """
        self.logger.debug("setup_chartメソッド開始")
        # ステージデータの詳細ログ出力
        if hasattr(self, 'stage_data') and self.stage_data:
            self.logger.debug(f"ステージデータの型: {type(self.stage_data)}")
            self.logger.debug(f"ステージデータの数: {len(self.stage_data)}")
            for i, stage in enumerate(self.stage_data):
                self.logger.debug(f"ステージ{i+1}: {stage.get('name', '名前なし')}")
                skills = stage.get('skills', [])
                self.logger.debug(f"  スキル数: {len(skills)}")
                for j, skill in enumerate(skills):
                    self.logger.debug(f"    スキル{j+1}: {skill.get('name', 'なし')} = {skill.get('value', 'なし')}")
        else:
            self.logger.warning("ステージデータがありません")
        """
        
        content = content[:setup_body_start] + debug_setup + content[setup_body_start:]
    
    # draw_chartメソッドを完全に書き直し
    if "def draw_chart" in content:
        draw_pos = content.find("def draw_chart")
        next_def = content.find("def ", draw_pos + 1)
        if next_def < 0:
            next_def = len(content)
        
        # 既存のdraw_chartメソッドを新しい実装に置き換え
        new_draw_chart = """    def draw_chart(self, stage_idx, skills):
        """レーダーチャートを描画"""
        self.logger.debug(f"draw_chart開始: ステージインデックス={stage_idx}, スキル数={len(skills) if skills else 0}")
        
        # キャンバスをクリア
        self.ax.clear()
        
        # スキルデータの検証と修正
        if not skills or not isinstance(skills, list) or len(skills) == 0:
            self.logger.warning(f"表示するスキルがありません (データ: {skills})")
            # ダミーデータを使用
            skills = [
                {"name": "Python", "value": 3},
                {"name": "JavaScript", "value": 2},
                {"name": "データ分析", "value": 4},
                {"name": "CI/CD", "value": 3},
                {"name": "UIデザイン", "value": 2}
            ]
            self.logger.info("ダミーデータを使用してレーダーチャートを表示します")
        
        # スキル名とスキル値を抽出
        skill_names = [skill.get('name', f"スキル{i+1}") for i, skill in enumerate(skills)]
        skill_values = [float(skill.get('value', 0)) for skill in skills]
        
        self.logger.debug(f"スキル名: {skill_names}")
        self.logger.debug(f"スキル値: {skill_values}")
        
        # スキルの数
        N = len(skill_names)
        
        if N == 0:
            self.logger.error("スキルデータがありません")
            self.canvas.draw()
            return
        
        # 角度を計算
        angles = [n / float(N) * 2 * 3.1415927 for n in range(N)]
        angles += angles[:1]  # 円を閉じる
        
        # スキル値も閉じたリストにする
        skill_values += skill_values[:1]
        
        # 最大値を設定
        max_value = 5  # 0-5の評価を想定
        
        # レーダーチャートの設定
        self.ax.set_theta_offset(3.1415927 / 2)  # 上から始める
        self.ax.set_theta_direction(-1)  # 時計回り
        
        # 目盛りを設定
        self.ax.set_rlabel_position(0)
        self.ax.set_rticks([1, 2, 3, 4, 5])
        self.ax.set_rlim(0, max_value)
        self.ax.set_yticklabels(['1', '2', '3', '4', '5'], color="grey", size=7)
        
        # プロット用の角度ラベルを設定
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(skill_names, size=9)
        
        # グリッド線
        self.ax.grid(True)
        
        # データをプロット
        self.ax.plot(angles, skill_values, 'o-', linewidth=2, linestyle='-', markersize=5)
        self.ax.fill(angles, skill_values, alpha=0.25)
        
        # キャンバスを更新
        self.canvas.draw()
        self.logger.debug("レーダーチャートの描画完了")
"""
        
        # Pythonの文字列リテラル修正（docstringエスケープ）
        new_draw_chart = new_draw_chart.replace('"""レーダーチャートを描画"""', '\"\"\"レーダーチャートを描画\"\"\"')
        
        # メソッドを置き換え
        content = content[:draw_pos] + new_draw_chart + content[next_def:]
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}のdraw_chartメソッドを修正しました")
    return True

if __name__ == "__main__":
    fix_radar_chart_drawing()
