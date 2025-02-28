#!/usr/bin/env python3
"""コード構造の分析"""

import os
import re

def analyze_files():
    """ファイル構造の分析"""
    # 関連ファイルのパス
    tab_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    dialog_path = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    # ファイル内容を確認
    with open(tab_path, 'r') as f:
        tab_content = f.read()
    
    with open(dialog_path, 'r') as f:
        dialog_content = f.read()
    
    # クラスとメソッドの一覧を表示
    tab_classes = re.findall(r'class\s+(\w+)', tab_content)
    tab_methods = re.findall(r'def\s+(\w+)', tab_content)
    
    dialog_classes = re.findall(r'class\s+(\w+)', dialog_content)
    dialog_methods = re.findall(r'def\s+(\w+)', dialog_content)
    
    print("=== StagedTargetTab 分析 ===")
    print(f"クラス: {', '.join(tab_classes)}")
    print(f"メソッド: {', '.join(tab_methods)}")
    
    print("\n=== RadarChartDialog 分析 ===")
    print(f"クラス: {', '.join(dialog_classes)}")
    print(f"メソッド: {', '.join(dialog_methods)}")
    
    # データ構造の確認
    print("\n=== データ構造 ===")
    # generate_test_data メソッドの確認
    generate_test_data = re.search(r'def generate_test_data.*?return stage_data', tab_content, re.DOTALL)
    if generate_test_data:
        print("テストデータ生成が見つかりました")
    
    # draw_chart メソッドの確認
    draw_chart = re.search(r'def draw_chart.*?canvas\.draw', dialog_content, re.DOTALL)
    if draw_chart:
        print("チャート描画が見つかりました")
    
    return tab_content, dialog_content

# 実行
analyze_files()
