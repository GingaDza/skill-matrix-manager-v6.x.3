"""段階的な目標値設定 - スキルの段階別目標を設定するタブ"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QMessageBox, QGroupBox, QFormLayout, QDoubleSpinBox,
    QRadioButton, QButtonGroup, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal

class StagedTargetTab(QWidget):
    """段階的な目標値設定タブ"""
    
    # データ変更通知用シグナル
    data_changed = pyqtSignal()
    
    def __init__(self, data_model=None, parent=None):
        super().__init__(parent)
        self.data_model = data_model or {}  # データモデルが与えられない場合は空の辞書を使用
        self.stage_rows = []
        self.staged_targets = {}  # 段階的目標のデータ
        self.hierarchy = {}  # スキル階層データ
        
        # テストデータの読み込み
        self.load_test_data()
        
        self.setup_ui()
    
    def load_test_data(self):
        """テスト用データの読み込み"""
        # グループ、カテゴリ、スキルの階層データ
        self.hierarchy = {
            "prog": {
                "name": "プログラミング",
                "categories": {
                    "lang": {
                        "name": "言語",
                        "skills": {
                            "python": {"name": "Python", "current": 3, "target": 5},
                            "java": {"name": "Java", "current": 2, "target": 4},
                            "js": {"name": "JavaScript", "current": 4, "target": 5}
                        }
                    },
                    "db": {
                        "name": "データベース",
                        "skills": {
                            "mysql": {"name": "MySQL", "current": 4, "target": 5},
                            "mongodb": {"name": "MongoDB", "current": 2, "target": 4}
                        }
                    },
                    "frame": {
                        "name": "フレームワーク",
                        "skills": {
                            "django": {"name": "Django", "current": 3, "target": 5},
                            "react": {"name": "React", "current": 2, "target": 4},
                            "vue": {"name": "Vue.js", "current": 1, "target": 3}
                        }
                    }
                }
            },
            "design": {
                "name": "デザイン",
                "categories": {
                    "ui": {
                        "name": "UI/UX",
                        "skills": {
                            "figma": {"name": "Figma", "current": 3, "target": 5},
                            "xd": {"name": "Adobe XD", "current": 2, "target": 4}
                        }
                    },
                    "graphic": {
                        "name": "グラフィック",
                        "skills": {
                            "ps": {"name": "Photoshop", "current": 4, "target": 5},
                            "ai": {"name": "Illustrator", "current": 3, "target": 4}
                        }
                    }
                }
            },
            "business": {
                "name": "ビジネススキル",
                "categories": {
                    "mgmt": {
                        "name": "マネジメント",
                        "skills": {
                            "project": {"name": "プロジェクト管理", "current": 3, "target": 5},
                            "team": {"name": "チームリーダーシップ", "current": 2, "target": 4}
                        }
                    },
                    "comm": {
                        "name": "コミュニケーション",
                        "skills": {
                            "presentation": {"name": "プレゼンテーション", "current": 4, "target": 5},
                            "writing": {"name": "文書作成", "current": 3, "target": 4}
                        }
                    }
                }
            }
        }
        
        # 段階的目標のテストデータ
        self.staged_targets = {
            "prog": {
                "lang": [
                    {"time": 3, "unit": "月", "targets": {"Python": 2, "Java": 1, "JavaScript": 2}},
                    {"time": 6, "unit": "月", "targets": {"Python": 3, "Java": 2, "JavaScript": 3}},
                    {"time": 12, "unit": "月", "targets": {"Python": 4, "Java": 3, "JavaScript": 4}}
                ]
            }
        }
    
    def setup_ui(self):
        """UIの初期設定"""
        main_layout = QVBoxLayout(self)
        
        # タイトル
        title_label = QLabel("段階的な目標値設定")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # 説明
        desc_label = QLabel("各スキルの習得目標を複数の段階に分けて設定します。")
        desc_label.setStyleSheet("font-size: 10pt; margin-bottom: 10px;")
        main_layout.addWidget(desc_label)
        
        # 時間単位選択
        time_unit_group = QGroupBox("時間単位")
        time_unit_layout = QHBoxLayout(time_unit_group)
        
        self.time_unit_group = QButtonGroup(time_unit_group)
        units = ["時間", "日", "週", "月", "年"]
        
        for i, unit in enumerate(units):
            radio = QRadioButton(unit)
            if i == 3:  # デフォルトで「月」を選択
                radio.setChecked(True)
            self.time_unit_group.addButton(radio, i)
            time_unit_layout.addWidget(radio)
        
        main_layout.addWidget(time_unit_group)
        
        # スキル選択
        skill_selection_group = QGroupBox("スキル選択")
        skill_selection_layout = QVBoxLayout(skill_selection_group)
        
        # グループ・カテゴリ選択
        selection_form = QFormLayout()
        
        self.staged_group_combo = QComboBox()
        for group_id, group_data in self.hierarchy.items():
            self.staged_group_combo.addItem(group_data["name"], group_id)
        
        self.staged_category_combo = QComboBox()
        
        selection_form.addRow("グループ:", self.staged_group_combo)
        selection_form.addRow("カテゴリ:", self.staged_category_combo)
        skill_selection_layout.addLayout(selection_form)
        
        # スキル選択テーブル
        self.skill_selection_table = QTableWidget()
        self.skill_selection_table.setColumnCount(2)
        self.skill_selection_table.setHorizontalHeaderLabels(["スキル名", "選択"])
        self.skill_selection_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.skill_selection_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        skill_selection_layout.addWidget(self.skill_selection_table)
        
        # グループ選択時の処理を設定
        self.staged_group_combo.currentIndexChanged.connect(self.update_staged_category_combo)
        self.staged_category_combo.currentIndexChanged.connect(self.update_skill_selection_table)
        
        main_layout.addWidget(skill_selection_group)
        
        # 段階設定 - 各段階でのレベルを設定する
        self.stages_group = QGroupBox("段階的目標設定")
        self.stages_layout = QGridLayout(self.stages_group)
        
        # ヘッダー
        self.stages_layout.addWidget(QLabel("<b>段階</b>"), 0, 0)
        self.stages_layout.addWidget(QLabel("<b>時間</b>"), 0, 1)
        self.stages_layout.addWidget(QLabel("<b>目標レベル</b>"), 0, 2)
        self.stages_layout.addWidget(QLabel(""), 0, 3)  # 削除ボタン用の列
        
        # 段階の行を追加
        for i in range(1, 4):  # 初期段階は3つ
            self.add_stage_row(i)
        
        # 段階追加ボタン
        add_stage_btn = QPushButton("段階を追加")
        add_stage_btn.clicked.connect(self.add_stage)
        self.stages_layout.addWidget(add_stage_btn, len(self.stage_rows) + 1, 0, 1, 4)
        
        main_layout.addWidget(self.stages_group)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        
        # レーダーチャート確認ボタン
        self.chart_btn = QPushButton("レーダーチャートで確認")
        self.chart_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 15px;")
        self.chart_btn.clicked.connect(self.show_radar_chart)
        button_layout.addWidget(self.chart_btn)
        
        button_layout.addStretch(1)
        
        # 保存ボタン
        self.save_btn = QPushButton("目標値を保存")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 15px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_targets)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # 段階的目標用のカテゴリコンボとスキル選択テーブルを初期化
        self.update_staged_category_combo()
    
    def add_stage_row(self, row_num):
        """段階的目標の行を追加"""
        # 段階ラベル
        stage_label = QLabel(f"段階 {row_num}")
        
        # 時間入力
        time_spin = QDoubleSpinBox()
        time_spin.setMinimum(1)
        time_spin.setMaximum(1000)
        time_spin.setValue(row_num * 3)  # デフォルト値 (3, 6, 9, 12...)
        time_spin.setSingleStep(1)
        
        # 目標レベル
        level_combo = QComboBox()
        for i in range(1, 6):
            level_combo.addItem(f"レベル {i}", i)
        
        # 最後の行の場合はレベル5をデフォルトに、それ以外は段階に合わせて設定
        default_level = min(row_num, 5)
        level_combo.setCurrentIndex(default_level - 1)
        
        # 削除ボタン
        delete_btn = QPushButton("削除")
        delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        delete_btn.clicked.connect(lambda: self.delete_stage_row(row_num))
        
        # 行にウィジェットを追加
        self.stages_layout.addWidget(stage_label, row_num, 0)
        self.stages_layout.addWidget(time_spin, row_num, 1)
        self.stages_layout.addWidget(level_combo, row_num, 2)
        self.stages_layout.addWidget(delete_btn, row_num, 3)
        
        # 管理用に行データを保存
        self.stage_rows.append({
            "label": stage_label,
            "time": time_spin,
            "level": level_combo,
            "delete": delete_btn
        })
    
    def add_stage(self):
        """新しい段階を追加"""
        # 追加ボタンの位置を取得
        btn_row = len(self.stage_rows) + 1
        
        # 新しい行を追加
        row_num = btn_row
        self.add_stage_row(row_num)
        
        # ボタンの位置を更新
        add_stage_btn = self.stages_layout.itemAtPosition(btn_row, 0).widget()
        if add_stage_btn:
            self.stages_layout.removeWidget(add_stage_btn)
            self.stages_layout.addWidget(add_stage_btn, btn_row + 1, 0, 1, 4)  # 削除ボタン列も含める
    
    def delete_stage_row(self, row_num):
        """段階行を削除"""
        # 少なくとも1つの段階は残す
        if len(self.stage_rows) <= 1:
            QMessageBox.warning(self, "削除エラー", "少なくとも1つの段階が必要です。")
            return
        
        # 指定された行を削除
        actual_idx = row_num - 1  # インデックスは0から始まるため調整
        
        if 0 <= actual_idx < len(self.stage_rows):
            # 行のウィジェットを削除
            row_data = self.stage_rows[actual_idx]
            for key in ["label", "time", "level", "delete"]:
                widget = row_data[key]
                self.stages_layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()
            
            # リストから削除
            self.stage_rows.pop(actual_idx)
            
            # 残りの行を再配置
            for i, row_data in enumerate(self.stage_rows, start=1):
                row_data["label"].setText(f"段階 {i}")
                self.stages_layout.addWidget(row_data["label"], i, 0)
                self.stages_layout.addWidget(row_data["time"], i, 1)
                self.stages_layout.addWidget(row_data["level"], i, 2)
                self.stages_layout.addWidget(row_data["delete"], i, 3)
            
            # 追加ボタンの位置を更新
            add_btn_row = len(self.stage_rows) + 1
            add_stage_btn = self.stages_layout.itemAtPosition(add_btn_row + 1, 0).widget()
            if add_stage_btn:
                self.stages_layout.removeWidget(add_stage_btn)
                self.stages_layout.addWidget(add_stage_btn, add_btn_row, 0, 1, 4)
    
    def update_staged_category_combo(self):
        """段階的目標タブ用のカテゴリコンボボックスを更新"""
        self.staged_category_combo.clear()
        
        group_id = self.staged_group_combo.currentData()
        if group_id in self.hierarchy:
            group_data = self.hierarchy[group_id]
            for cat_id, cat_data in group_data["categories"].items():
                self.staged_category_combo.addItem(cat_data["name"], cat_id)
        
        self.update_skill_selection_table()
    
    def update_skill_selection_table(self):
        """スキル選択テーブルを更新"""
        self.skill_selection_table.setRowCount(0)
        
        group_id = self.staged_group_combo.currentData()
        cat_id = self.staged_category_combo.currentData()
        
        if group_id in self.hierarchy and cat_id and cat_id in self.hierarchy[group_id]["categories"]:
            skills = self.hierarchy[group_id]["categories"][cat_id]["skills"]
            
            self.skill_selection_table.setRowCount(len(skills))
            for row, (skill_id, skill_data) in enumerate(skills.items()):
                # スキル名
                self.skill_selection_table.setItem(row, 0, QTableWidgetItem(skill_data["name"]))
                
                # 選択チェックボックス
                checkbox = QComboBox()
                checkbox.addItem("含める", True)
                checkbox.addItem("含めない", False)
                checkbox.setProperty("skill_id", skill_id)
                self.skill_selection_table.setCellWidget(row, 1, checkbox)
    
    def get_staged_data(self):
        """段階的目標データを収集して返す"""
        # 選択されたグループとカテゴリ
        group_id = self.staged_group_combo.currentData()
        cat_id = self.staged_category_combo.currentData()
        
        if not (group_id and cat_id):
            return None
        
        # 時間単位
        time_unit_id = self.time_unit_group.checkedId()
        time_units = ["時間", "日", "週", "月", "年"]
        time_unit = time_units[time_unit_id] if 0 <= time_unit_id < len(time_units) else "月"
        
        # 選択されたスキル
        selected_skills = {}
        for row in range(self.skill_selection_table.rowCount()):
            checkbox = self.skill_selection_table.cellWidget(row, 1)
            if checkbox and checkbox.currentData():
                skill_id = checkbox.property("skill_id")
                skill_name = self.skill_selection_table.item(row, 0).text()
                selected_skills[skill_id] = skill_name
        
        if not selected_skills:
            return None
        
        # 段階データの収集
        stages_data = []
        for i, row_data in enumerate(self.stage_rows):
            time_value = row_data["time"].value()
            level = row_data["level"].currentData()
            
            # 各スキルのターゲット設定
            targets = {}
            for skill_id, skill_name in selected_skills.items():
                targets[skill_name] = level
            
            stages_data.append({
                "time": time_value,
                "unit": time_unit,
                "targets": targets
            })
        
        # 時間順にソート
        stages_data.sort(key=lambda x: x["time"])
        
        return stages_data
    
    def save_targets(self):
        """段階的な目標値を保存"""
        stages_data = self.get_staged_data()
        
        if not stages_data:
            QMessageBox.warning(self, "データエラー", "保存するデータがありません。\nグループ、カテゴリ、スキルを正しく選択してください。")
            return
        
        # 選択されたグループとカテゴリ
        group_id = self.staged_group_combo.currentData()
        cat_id = self.staged_category_combo.currentData()
        
        # データモデルに保存
        if group_id not in self.staged_targets:
            self.staged_targets[group_id] = {}
        
        self.staged_targets[group_id][cat_id] = stages_data
        
        # 保存成功メッセージ
        group_name = self.hierarchy[group_id]["name"]
        cat_name = self.hierarchy[group_id]["categories"][cat_id]["name"]
        time_unit = stages_data[0]["unit"]  # 全ての段階で同じ単位を使用
        
        message = f"以下の段階的目標を保存しました:\n\n"
        message += f"グループ: {group_name}\n"
        message += f"カテゴリ: {cat_name}\n"
        message += f"時間単位: {time_unit}\n\n"
        
        # 選択されたスキル名のリスト
        skill_names = list(stages_data[0]["targets"].keys())
        message += f"対象スキル: {', '.join(skill_names[:3])}"
        if len(skill_names) > 3:
            message += f" 他{len(skill_names) - 3}件"
        
        message += "\n\n段階設定:\n"
        for i, stage in enumerate(stages_data):
            message += f"段階 {i+1}: {stage['time']} {time_unit}後 → レベル {list(stage['targets'].values())[0]}\n"
        
        QMessageBox.information(self, "段階的目標保存", message)
        
        # 変更通知
        self.data_changed.emit()
    
    def show_radar_chart(self):
        """レーダーチャート表示ダイアログの表示"""
        from .radar_chart_dialog import RadarChartDialog
        
        stages_data = self.get_staged_data()
        
        if not stages_data:
            QMessageBox.warning(self, "データ不足", "表示可能なデータがありません。\n段階的な目標値を正しく設定してください。")
            return
            
        # レーダーチャートダイアログを表示
        dialog = RadarChartDialog(self, stages_data, compare_mode=False)
        dialog.exec_()

    def add_staged_targets_tab(self):
        """段階的な目標設定タブを追加"""
        # 段階的目標タブ
        staged_tab = QWidget()
        staged_layout = QVBoxLayout()
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # 内部コンテンツウィジェット
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # タイトルとヘルプテキスト
        title_label = QLabel("段階的な目標設定")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        content_layout.addWidget(title_label)
        
        help_text = QLabel("各段階でのスキル目標値を設定します。現在値と目標値を比較表示できます。")
        help_text.setWordWrap(True)
        content_layout.addWidget(help_text)
        
        # スキル段階選択
        stages_layout = QHBoxLayout()
        stages_layout.addWidget(QLabel("表示する段階:"))
        
        # 段階の選択（チェックボックス）
        stages = self.generate_test_data()
        self.stage_checkboxes = []
        
        for i, stage in enumerate(stages):
            stage_name = stage.get('name', f'段階{i+1}')
            checkbox = QCheckBox(stage_name)
            checkbox.setChecked(True)  # デフォルトでは全て選択
            stages_layout.addWidget(checkbox)
            self.stage_checkboxes.append(checkbox)
        
        content_layout.addLayout(stages_layout)
        
        # コンテンツをセット
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        staged_layout.addWidget(scroll)
        
        # ボタン配置
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        # 比較チャート表示ボタン
        compare_button = QPushButton("比較チャート表示")
        compare_button.clicked.connect(self.show_comparison_chart)
        button_layout.addWidget(compare_button)
        
        staged_layout.addLayout(button_layout)
        staged_tab.setLayout(staged_layout)
        
        # タブに追加
        self.tabs.addTab(staged_tab, "段階的目標")

    def add_staged_targets_tab(self):
        """段階的な目標設定タブを追加"""
        # 段階的目標タブ
        staged_tab = QWidget()
        staged_layout = QVBoxLayout()
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # 内部コンテンツウィジェット
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        # タイトルとヘルプテキスト
        title_label = QLabel("段階的な目標設定")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        content_layout.addWidget(title_label)
        
        help_text = QLabel("各段階でのスキル目標値を設定します。現在値と目標値を比較表示できます。")
        help_text.setWordWrap(True)
        content_layout.addWidget(help_text)
        
        # スキル段階選択
        stages_layout = QHBoxLayout()
        stages_layout.addWidget(QLabel("表示する段階:"))
        
        # 段階の選択（チェックボックス）
        stages = self.generate_test_data()
        self.stage_checkboxes = []
        
        for i, stage in enumerate(stages):
            stage_name = stage.get('name', f'段階{i+1}')
            checkbox = QCheckBox(stage_name)
            checkbox.setChecked(True)  # デフォルトでは全て選択
            stages_layout.addWidget(checkbox)
            self.stage_checkboxes.append(checkbox)
        
        content_layout.addLayout(stages_layout)
        
        # コンテンツをセット
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        staged_layout.addWidget(scroll)
        
        # ボタン配置
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        # 比較チャート表示ボタン
        compare_button = QPushButton("比較チャート表示")
        compare_button.clicked.connect(self.show_comparison_chart)
        button_layout.addWidget(compare_button)
        
        staged_layout.addLayout(button_layout)
        staged_tab.setLayout(staged_layout)
        
        # タブに追加
        self.tabs.addTab(staged_tab, "段階的目標")

    def show_comparison_chart(self):
        """現在値と目標値を比較するレーダーチャートを表示"""
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
