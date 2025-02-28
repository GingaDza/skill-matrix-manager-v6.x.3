#!/usr/bin/env python3
"""draw_chartメソッドに比較モード対応を追加"""
import os
import re

filepath = "src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"

# ファイルを読み込む
with open(filepath, 'r') as f:
    content = f.read()

# プロット部分を置き換え
plot_pattern = r'(# データをプロット\s+self\.ax\.plot\(angles, skill_values, [^\)]+\)\s+self\.ax\.fill\(angles, skill_values, alpha=0\.25\))'
plot_match = re.search(plot_pattern, content)

if plot_match:
    old_plot = plot_match.group(1)
    
    # 新しいプロット部分
    new_plot = """# データをプロット
        if hasattr(self, 'compare_mode') and self.compare_mode and stage_idx > 0:
            # 比較モードでは異なる色とスタイルで表示
            colors = ['b', 'r', 'g', 'c', 'm', 'y']
            color = colors[stage_idx % len(colors)]
            alpha = 0.2 + (0.1 * stage_idx)  # 重なりを見やすくするため透明度を変える
            
            self.ax.plot(angles, skill_values, 'o-', linewidth=2, linestyle='-', 
                        markersize=5, color=color, label=f"段階 {stage_idx+1}")
            self.ax.fill(angles, skill_values, alpha=alpha, color=color)
            
            # 凡例を表示
            self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        else:
            # 通常モード
            self.ax.plot(angles, skill_values, 'o-', linewidth=2, linestyle='-', markersize=5)
            self.ax.fill(angles, skill_values, alpha=0.25)"""
    
    content = content.replace(old_plot, new_plot)
    print("プロット部分を比較モード対応に更新しました")
else:
    print("プロット部分が見つかりませんでした")

# 保存
with open(filepath, 'w') as f:
    f.write(content)

print("draw_chartメソッドの更新が完了しました。")
