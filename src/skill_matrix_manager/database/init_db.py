#!/usr/bin/env python3
"""データベース初期化スクリプト"""

from src.skill_matrix_manager.database import SkillMatrixDatabase

def init_database():
    """データベースを初期化"""
    db = SkillMatrixDatabase()
    db.connect()
    
    # メンバーテーブルの作成
    db.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        group_name TEXT
    )
    ''')
    
    # カテゴリテーブルの作成
    db.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # スキルテーブルの作成
    db.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    # スキルレベルテーブルの作成
    db.execute('''
    CREATE TABLE IF NOT EXISTS skill_levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        skill_id INTEGER,
        level INTEGER DEFAULT 1,
        FOREIGN KEY (member_id) REFERENCES members (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id)
    )
    ''')
    
    db.commit()
    db.close()
    
    print("データベースの初期化が完了しました")

if __name__ == "__main__":
    init_database()
