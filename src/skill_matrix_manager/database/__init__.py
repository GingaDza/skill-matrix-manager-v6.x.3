#!/usr/bin/env python3
"""スキルマトリックスデータベース"""

import sqlite3
import os
from datetime import datetime

class SkillMatrixDatabase:
    """スキルマトリックスデータベースクラス"""
    
    def __init__(self, db_path="skill_matrix.db"):
        """初期化"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """データベースに接続"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.connection
    
    def close(self):
        """接続を閉じる"""
        if self.connection:
            self.connection.close()
    
    def commit(self):
        """変更をコミット"""
        if self.connection:
            self.connection.commit()
    
    def execute(self, query, params=()):
        """クエリを実行"""
        if self.cursor:
            return self.cursor.execute(query, params)
        return None
    
    def get_groups(self):
        """グループ一覧を取得"""
        self.execute("SELECT DISTINCT group_name FROM members WHERE group_name IS NOT NULL AND group_name != ''")
        return [row['group_name'] for row in self.cursor.fetchall()]
    
    def get_members(self, group=None):
        """メンバー一覧を取得"""
        if group and group != "すべて":
            self.execute(
                "SELECT id, name, email, group_name FROM members WHERE group_name = ?",
                (group,)
            )
        else:
            self.execute("SELECT id, name, email, group_name FROM members")
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_member(self, member_id):
        """メンバー情報を取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE id = ?",
            (member_id,)
        )
        return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None
    
    def add_member(self, name, email="", group_name=""):
        """メンバーを追加"""
        self.execute(
            "INSERT INTO members (name, email, group_name) VALUES (?, ?, ?)",
            (name, email, group_name)
        )
        self.commit()
        return self.cursor.lastrowid
    
    def update_member(self, member_id, name, email="", group_name=""):
        """メンバー情報を更新"""
        self.execute(
            "UPDATE members SET name = ?, email = ?, group_name = ? WHERE id = ?",
            (name, email, group_name, member_id)
        )
        self.commit()
        return True
    
    def delete_member(self, member_id):
        """メンバーを削除"""
        self.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.commit()
        return True
    
    def get_member_by_name(self, name):
        """名前からメンバー情報を取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE name = ?",
            (name,)
        )
        result = self.cursor.fetchone()
        return dict(result) if result else None
