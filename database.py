import sqlite3
import json
from datetime import datetime

DB_NAME = 'dodo_bot.db'

def init_db():
    """Создаёт таблицы, если их нет"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Таблица пользователей
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 2000,
            last_bonus TEXT,
            last_robbery TEXT,
            lost_total INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            games_won INTEGER DEFAULT 0,
            username TEXT,
            first_name TEXT,
            referrals INTEGER DEFAULT 0,
            referral_bonus INTEGER DEFAULT 0,
            used_promos TEXT DEFAULT '[]',
            turnover INTEGER DEFAULT 0,
            dmp INTEGER DEFAULT 0
        )
    ''')
    
    # Таблица промокодов
    cur.execute('''
        CREATE TABLE IF NOT EXISTS promocodes (
            code TEXT PRIMARY KEY,
            amount INTEGER,
            uses_left INTEGER,
            created_by INTEGER,
            created_at TEXT
        )
    ''')
    
    # Таблица банов
    cur.execute('''
        CREATE TABLE IF NOT EXISTS banned_users (
            user_id INTEGER PRIMARY KEY,
            until TEXT,
            reason TEXT,
            banned_by INTEGER,
            banned_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получить данные пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    
    if not user:
        # Создаём нового пользователя
        cur.execute('''
            INSERT INTO users (user_id, balance) 
            VALUES (?, ?)
        ''', (user_id, 2000))
        conn.commit()
        
        cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cur.fetchone()
    
    conn.close()
    
    # Преобразуем кортеж в словарь
    columns = ['user_id', 'balance', 'last_bonus', 'last_robbery', 'lost_total', 
               'games_played', 'games_won', 'username', 'first_name', 'referrals', 
               'referral_bonus', 'used_promos', 'turnover', 'dmp']
    
    user_dict = dict(zip(columns, user))
    
    # Преобразуем JSON строки обратно в списки
    user_dict['used_promos'] = json.loads(user_dict['used_promos'])
    
    return user_dict

def update_user(user_id, data):
    """Обновить данные пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Преобразуем списки в JSON
    if 'used_promos' in data:
        data['used_promos'] = json.dumps(data['used_promos'])
    
    # Строим запрос
    set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
    values = list(data.values()) + [user_id]
    
    cur.execute(f'''
        UPDATE users 
        SET {set_clause} 
        WHERE user_id = ?
    ''', values)
    
    conn.commit()
    conn.close()

# Аналогичные функции для промокодов и банов...
