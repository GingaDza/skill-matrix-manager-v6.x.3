#!/usr/bin/env python3
"""インデントだけを修正する最小限のスクリプト"""
import os
import re

def minimal_fix():
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル内容を読み込む
    with open(filepath, 'r') as f:
        content = f.read()
    
    # dialog.exec_()の行を見つけて修正
    pattern = r'(\s+)dialog = RadarChartDialog.*?\n(\s+)dialog\.exec_\(\)'
    if re.search(pattern, content, re.DOTALL):
        # マッチした場合、インデントを揃える
        fixed_content = re.sub(
            pattern, 
            lambda m: m.group(0).replace(m.group(2), m.group(1)), 
            content, 
            flags=re.DOTALL
        )
        
        # 修正を保存
        with open(filepath, 'w') as f:
            f.write(fixed_content)
        
        print(f"{filepath}のインデントを修正しました")
        return True
    else:
        print("dialog.exec_()の行が見つかりませんでした")
        return False

if __name__ == "__main__":
    minimal_fix()
