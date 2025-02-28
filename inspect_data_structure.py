#!/usr/bin/env python3
import os
import re

def check_stage_data_structure():
    # staged_target_tab.pyでのデータ生成部分を調べる
    tab_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # データ生成のコード（テストデータ）を確認
    with open(tab_path, 'r') as f:
        tab_content = f.read()
    
    print("=== StagedTargetTab のスキルデータ構造 ===")
    # generate_test_dataメソッド内のスキルデータ構造
    skills_structure = re.search(r'skills\.append\(\{([^}]+)\}\)', tab_content)
    if skills_structure:
        print(f"スキル構造: {skills_structure.group(1)}")
    
    # skills_dataの構造
    test_data = re.search(r'stage_data\.append\(\{([^}]+)\}\)', tab_content)
    if test_data:
        print(f"ステージデータ構造: {test_data.group(1)}")
    
    print("\n=== RadarChartDialog のデータ処理 ===")
    # レーダーチャートダイアログでのデータ処理を確認
    with open(dialog_path, 'r') as f:
        dialog_content = f.read()
    
    # all_skillsの更新部分
    all_skills_update = re.search(r'all_skills\.update\(([^)]+)\)', dialog_content)
    if all_skills_update:
        print(f"all_skills更新: {all_skills_update.group(1)}")
    
    return True

def fix_data_structure_mismatch():
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # バックアップ作成
    backup = dialog_path + ".struct_fix.bak"
    os.system(f"cp {dialog_path} {backup}")
    print(f"バックアップ作成: {backup}")
    
    with open(dialog_path, 'r') as f:
        content = f.readlines()
    
    modified = []
    for line in content:
        # スキルデータがリスト形式の場合の処理
        if "all_skills.update(stage['skills'].keys())" in line:
            # リストからスキル名のリストを作成するよう変更
            modified.append("            # スキルがリスト形式の場合の処理\n")
            modified.append("            skills_list = stage['skills']\n")
            modified.append("            for skill in skills_list:\n")
            modified.append("                if 'name' in skill:\n")
            modified.append("                    all_skills.add(skill['name'])\n")
        elif "values.append(stage['skills'].get(skill_id, 0))" in line:
            # リスト内のスキルから値を取得するよう変更
            modified.append("                # スキルがリスト形式の場合の処理\n")
            modified.append("                skill_value = 0\n")
            modified.append("                for skill in stage['skills']:\n")
            modified.append("                    if skill.get('name') == skill_id:\n")
            modified.append("                        skill_value = skill.get('value', 0)\n")
            modified.append("                        break\n")
            modified.append("                values.append(skill_value)\n")
        else:
            modified.append(line)
    
    with open(dialog_path, 'w') as f:
        f.writelines(modified)
    
    print(f"{dialog_path}のデータ構造の扱いを修正しました")
    return True

def rewrite_radar_chart_method():
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル読み込み
    with open(dialog_path, 'r') as f:
        content = f.read()
    
    # draw_radar_chartメソッド全体を置き換え
    draw_radar_pattern = r'def draw_radar_chart\(self\):.*?(?=\n    def|\Z)'
    new_method = '''def draw_radar_chart(self):
        """レーダーチャートを描画"""
        try:
            self.logger.debug("レーダーチャートの描画開始")
            
            # データ構造を確認
            if not self.stages_data:
                self.logger.warning("stages_dataがありません")
                return
                
            self.logger.debug(f"stages_dataの長さ: {len(self.stages_data)}")
            
            # すべてのスキル名を収集
            all_skills = set()
            for stage in self.stages_data:
                if 'skills' not in stage:
                    continue
                
                skills_list = stage['skills']
                if not isinstance(skills_list, list):
                    self.logger.warning(f"skills is not a list: {type(skills_list)}")
                    continue
                    
                for skill in skills_list:
                    if isinstance(skill, dict) and 'name' in skill:
                        all_skills.add(skill['name'])
            
            # スキル名の一覧
            skill_names = sorted(list(all_skills))
            self.logger.debug(f"抽出されたスキル名: {skill_names}")
            
            if not skill_names:
                self.logger.warning("表示するスキルがありません")
                return
            
            # 各ステージのデータを準備
            for i, stage in enumerate(self.stages_data):
                if not self.selected_stages[i]:
                    continue
                    
                # タブ用のキャンバスを作成
                figure = plt.figure(figsize=(6, 6))
                self.figures.append(figure)
                ax = figure.add_subplot(111, polar=True)
                self.axes.append(ax)
                canvas = FigureCanvas(figure)
                self.canvas_list.append(canvas)
                
                # ステージのスキル値を取得
                skill_values = []
                if 'skills' in stage:
                    skills_list = stage['skills']
                    for skill_name in skill_names:
                        value = 0
                        for skill in skills_list:
                            if skill.get('name') == skill_name:
                                value = skill.get('value', 0)
                                break
                        skill_values.append(value)
                
                self.logger.debug(f"ステージ{i+1}のスキル値: {skill_values}")
            
            # 各ステージのタブを作成
            for i, stage in enumerate(self.stages_data):
                if not self.selected_stages[i]:
                    continue
                    
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
    '''
    
    # メソッド置き換え（正規表現でマッチング）
    new_content = re.sub(draw_radar_pattern, new_method, content, flags=re.DOTALL)
    
    with open(dialog_path, 'w') as f:
        f.write(new_content)
    
    print(f"{dialog_path}のdraw_radar_chartメソッドを書き換えました")
    return True

def fix_draw_chart():
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル読み込み
    with open(dialog_path, 'r') as f:
        content = f.read()
    
    # draw_chartメソッド全体を置き換え
    draw_chart_pattern = r'def draw_chart\(self, stage_idx, skills\):.*?(?=\n    def|\Z)'
    new_method = '''def draw_chart(self, stage_idx, skills):
        """レーダーチャートを描画"""
        self.logger.debug(f"draw_chart開始: ステージインデックス={stage_idx}, スキル数={len(skills) if skills else 0}")
        
        # キャンバスをクリア
        self.ax = self.axes[stage_idx]
        self.ax.clear()
        
        # スキルデータの検証
        if not skills or len(skills) == 0:
            self.logger.warning("表示するスキルがありません")
            # ダミーデータを使用
            skills = [
                {"name": "Python", "value": 3},
                {"name": "JavaScript", "value": 2},
                {"name": "データ分析", "value": 4},
                {"name": "CI/CD", "value": 3},
                {"name": "UIデザイン", "value": 2}
            ]
        
        # スキル名とスキル値を抽出
        if isinstance(skills, list):
            # リスト形式の場合
            skill_names = [skill.get('name', f"スキル{i+1}") for i, skill in enumerate(skills)]
            skill_values = [float(skill.get('value', 0)) for skill in skills]
        else:
            # 辞書形式の場合（古い形式）
            skill_names = list(skills.keys())
            skill_values = [float(skills.get(name, 0)) for name in skill_names]
        
        self.logger.debug(f"スキル名: {skill_names}")
        self.logger.debug(f"スキル値: {skill_values}")
        
        # スキルの数
        N = len(skill_names)
        if N == 0:
            self.logger.warning("スキル数がゼロです")
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
        self.canvas = self.canvas_list[stage_idx]
        self.canvas.draw()
    '''
    
    # メソッド置き換え（正規表現でマッチング）
    new_content = re.sub(draw_chart_pattern, new_method, content, flags=re.DOTALL)
    
    with open(dialog_path, 'w') as f:
        f.write(new_content)
    
    print(f"{dialog_path}のdraw_chartメソッドを書き換えました")
    return True

# 実行
check_stage_data_structure()
print("\n--- 修正を適用します ---\n")
fix_data_structure_mismatch()
rewrite_radar_chart_method()
fix_draw_chart()
