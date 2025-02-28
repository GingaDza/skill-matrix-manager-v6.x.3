#!/usr/bin/env python3
import os

def check_syntax(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        compile(content, filepath, 'exec')
        print(f"{filepath}の構文は正常です")
        return True
    except SyntaxError as e:
        print(f"{filepath}に構文エラーがあります: {e}")
        return False

check_syntax("src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py")
check_syntax("src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py")
