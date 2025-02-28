#!/bin/bash
# バックアップの作成

# ファイルパス
STAGED_TAB="src/skill_matrix_manager/ui/components/skill_gap_tab/staged_target_tab.py"
RADAR_DIALOG="src/skill_matrix_manager/ui/components/skill_gap_tab/radar_chart_dialog.py"

# バックアップ作成
cp "$STAGED_TAB" "${STAGED_TAB}.impl.bak"
cp "$RADAR_DIALOG" "${RADAR_DIALOG}.impl.bak"

echo "バックアップ作成完了:"
echo "- ${STAGED_TAB}.impl.bak"
echo "- ${RADAR_DIALOG}.impl.bak"
