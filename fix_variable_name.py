#!/usr/bin/env python3
"""変数名の不一致を修正"""

import os

def fix_radar_chart_dialog_param():
    """radar_chart_dialog.pyの変数名を修正"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # バックアップ作成
    backup_file = filepath + ".var_fix.bak"
    with open(filepath, 'r') as src:
        with open(backup_file, 'w') as dst:
            dst.write(src.read())
    print(f"バックアップ作成: {backup_file}")
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # __init__メソッドのパラメータ名を確認
    init_method = "def __init__(self, parent=None, stage_data=None):"
    if init_method in content:
        # インスタンス変数として保存
        if "self.stage_data = stage_data" in content:
            print("初期化メソッドのパラメータとインスタンス変数の宣言を修正します")
            
            # パラメータ名を修正
            content = content.replace(
                "def __init__(self, parent=None, stage_data=None):", 
                "def __init__(self, parent=None, stages_data=None):"
            )
            
            # インスタンス変数宣言も修正
            content = content.replace(
                "self.stage_data = stage_data", 
                "self.stage_data = stages_data  # 内部では stage_data として使用"
            )
        else:
            print("初期化メソッドのパラメータのみ修正します")
            content = content.replace(
                "def __init__(self, parent=None, stage_data=None):", 
                "def __init__(self, parent=None, stages_data=None):"
            )
    
    # デバッグコードのパラメータ名修正
    if "self.logger.debug(f\"RadarChartDialog初期化: {len(stage_data)}個のステージデータ\")" in content:
        content = content.replace(
            "self.logger.debug(f\"RadarChartDialog初期化: {len(stage_data)}個のステージデータ\")", 
            "self.logger.debug(f\"RadarChartDialog初期化: {len(stages_data)}個のステージデータ\")"
        )
    
    # for ループのパラメータ名修正
    if "for i, stage in enumerate(stage_data):" in content:
        content = content.replace(
            "for i, stage in enumerate(stage_data):", 
            "for i, stage in enumerate(stages_data):"
        )
    
    # ファイル保存
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"{filepath}の変数名を修正しました")
    return True

def check_staged_target_tab():
    """staged_target_tab.pyの変数名を確認"""
    filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
    
    if not os.path.exists(filepath):
        print(f"エラー: {filepath}が見つかりません")
        return False
    
    # ファイル読み込み
    with open(filepath, 'r') as f:
        content = f.read()
    
    # RadarChartDialogの呼び出し部分を見つける
    dialog_line = None
    for line in content.split('\n'):
        if "RadarChartDialog" in line and "dialog =" in line:
            dialog_line = line.strip()
            print(f"RadarChartDialogの呼び出し: {dialog_line}")
            break
    
    # 渡される変数名を確認
    if dialog_line:
        if "stages_data" in dialog_line:
            print("変数名 'stages_data' が渡されています")
        else:
            print("別の変数名が渡されています")
    
    return True

if __name__ == "__main__":
    fix_radar_chart_dialog_param()
    check_staged_target_tab()
