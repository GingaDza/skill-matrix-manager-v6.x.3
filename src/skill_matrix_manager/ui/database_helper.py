#!/usr/bin/env python3
"""データベースアクセスヘルパー"""

import os
import sqlite3

def get_connection(db_path="skill_matrix.db"):
    """データベース接続を取得"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_groups():
    """グループ一覧を取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT group_name FROM members WHERE group_name IS NOT NULL AND group_name != ''")
    groups = [row['group_name'] for row in cursor.fetchall()]
    conn.close()
    return groups

def get_members(group=None):
    """メンバー一覧を取得"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if group and group != "すべて":
        cursor.execute(
            "SELECT id, name, email, group_name FROM members WHERE group_name = ?",
            (group,)
        )
    else:
        cursor.execute("SELECT id, name, email, group_name FROM members")
    
    members = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return members

def get_member_by_name(name):
    """名前からメンバー情報を取得"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, group_name FROM members WHERE name = ?",
        (name,)
    )
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def add_member(name, email="", group_name=""):
    """メンバーを追加"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO members (name, email, group_name) VALUES (?, ?, ?)",
        (name, email, group_name)
    )
    member_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return member_id
