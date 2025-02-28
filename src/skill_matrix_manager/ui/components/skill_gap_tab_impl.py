from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .skill_gap_tab.staged_target_tab import StagedTargetTab

class SkillGapTab(QWidget):
    """スキルギャップタブのメインクラス"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        
        # StagedTargetTabを初期化
        self.staged_target = StagedTargetTab()
        layout.addWidget(self.staged_target)
        
        self.setLayout(layout)
        
    def set_member(self, member_id, member_name, group_name):
        """メンバー情報を設定"""
        # 必要に応じてここにメンバー情報を使った処理を追加
        # 例: self.staged_target.load_member_data(member_id)
        pass
