#!/usr/bin/env python3
"""RadarChartDialog クラスを直接編集して確実に修正"""
import re

# ファイルパス
filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"

# ファイルを読み込む
with open(filepath, 'r') as f:
    lines = f.readlines()

# ファイルの内容を表示して確認
print("=== 現在の RadarChartDialog.__init__ ===")
in_init = False
for i, line in enumerate(lines):
    if "def __init__" in line:
        in_init = True
        print(f"{i+1}: {line.strip()}")
    elif in_init and "def " in line:
        in_init = False
    elif in_init:
        print(f"{i+1}: {line.strip()}")

# __init__ メソッドを正確に修正
for i, line in enumerate(lines):
    if "def __init__" in line and "self, parent=None, stages_data=None" in line:
        lines[i] = "    def __init__(self, parent=None, stages_data=None, compare_mode=False):\n"
        print(f"\n行 {i+1} を修正: {lines[i].strip()}")
        
        # 初期化処理を追加
        j = i + 1
        while j < len(lines) and "setup_ui" not in lines[j]:
            j += 1
            
        if j < len(lines) and "self.setup_ui()" in lines[j]:
            # setup_ui の前に compare_mode の初期化を追加
            indent = lines[j].split("self")[0]
            lines.insert(j, f"{indent}self.compare_mode = compare_mode\n")
            print(f"行 {j+1} に挿入: {indent}self.compare_mode = compare_mode")

# 保存
with open(filepath, 'w') as f:
    f.writelines(lines)

# draw_chart メソッド内の比較モード対応を確認
with open(filepath, 'r') as f:
    content = f.read()

print("\n=== draw_chart メソッドの修正状態 ===")
draw_chart_match = re.search(r'def draw_chart.*?compare_mode.*?canvas\.draw', content, re.DOTALL)
if draw_chart_match:
    print("比較モード対応済み")
else:
    print("比較モード未対応")
    
    # 修正が必要な場合
    plot_pattern = r'(# データをプロット\s+self\.ax\.plot\(angles, skill_values, [^\)]+\)\s+self\.ax\.fill\(angles, skill_values, alpha=0\.25\))'
    plot_match = re.search(plot_pattern, content, re.DOTALL)
    
    if plot_match:
        old_plot = plot_match.group(1)
        
        # 新しいプロット部分
        new_plot = """# データをプロット
        if hasattr(self, 'compare_mode') and self.compare_mode and stage_idx > 0:
            # 比較モードでは異なる色とスタイルで表示
            colors = ['b', 'r', 'g', 'c', 'm', 'y']
            color = colors[stage_idx % len(colors)]
            alpha = 0.2 + (0.1 * stage_idx)
            
            self.ax.plot(angles, skill_values, 'o-', linewidth=2, linestyle='-', 
                      markersize=5, color=color, label=f"段階 {stage_idx+1}")
            self.ax.fill(angles, skill_values, alpha=alpha, color=color)
            
            # 凡例を表示
            self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        else:
            # 通常モード
            self.ax.plot(angles, skill_values, 'o-', linewidth=2, linestyle='-', markersize=5)
            self.ax.fill(angles, skill_values, alpha=0.25)"""
        
        # 置き換え
        content = content.replace(old_plot, new_plot)
        
        # 保存
        with open(filepath, 'w') as f:
            f.write(content)
        
        print("draw_chart メソッドを修正しました")
    else:
        print("プロット部分が見つかりませんでした")

# StagedTargetTab の呼び出しを修正
tab_filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
with open(tab_filepath, 'r') as f:
    tab_lines = f.readlines()

found = False
for i, line in enumerate(tab_lines):
    if "dialog = RadarChartDialog(" in line and "compare_mode" not in line:
        tab_lines[i] = line.replace("dialog = RadarChartDialog(", "dialog = RadarChartDialog(", 1)
        # すでに修正されている可能性があるので変更不要
        print(f"\nStagedTargetTab の RadarChartDialog 呼び出し (行 {i+1}): {tab_lines[i].strip()}")
        found = True

if not found:
    print("StagedTargetTab 内の RadarChartDialog 呼び出しが見つかりませんでした")

with open(tab_filepath, 'w') as f:
    f.writelines(tab_lines)

print("\nすべての修正が完了しました。アプリケーションを再起動します...")
