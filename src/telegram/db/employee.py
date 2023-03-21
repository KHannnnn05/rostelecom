import sqlite3
import datetime

class DataBase:
    
    def __init__(self, con, cur):
        self.cur = cur
        self.con = con
        self.cur.execute("PRAGMA foreign_keys=on;")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS staff
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            telegram_username TEXT NOT NULL
        );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS info
        (   
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            full_name TEXT,
            phone_number TEXT,
            career_start_date DATE,
            career_close_date DATE DEFAULT NULL,
            telegram_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orders
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            staff_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            bbi INTEGER,
            tv INTEGER,
            mvno INTEGER,
            cctv INTEGER,
            ss INTEGER,
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        );""")
        self.con.commit()

    
    def add_new_staff(self, telegram_username) -> int:
        self.cur.execute("INSERT INTO staff (telegram_username) VALUES (?);", (telegram_username, ))
        self.con.commit()
        return self.cur.lastrowid
    
    def add_new_order(self, telegram_id, bbi, tv, mvno, cctv, ss, date=datetime.datetime.now().strftime("%d.%m.%Y")):
        self.cur.execute("""
            INSERT INTO orders (staff_id, date, bbi, tv, mvno, cctv, ss)
            SELECT info.staff_id, ?, ?, ?, ?, ?, ?
            FROM info
            WHERE info.telegram_id = ?
        """, (date, bbi, tv, mvno, cctv, ss, telegram_id))
        self.con.commit()

    def add_new_staff_info(self, data):
        self.cur.execute("INSERT INTO info (full_name, phone_number, career_start_date, telegram_id) VALUES (?, ?, ?, ?)", 
                         (data["full_name"], data["phone_number"], data["career_start_date"], data["telegram_id"]))
        self.con.commit()

    def get_rezult(self):
        current_date = (datetime.datetime.now().strftime('%d.%m.%Y'))
        self.cur.execute(f"""
                            SELECT info.full_name, sum(orders.bbi), sum(orders.tv), sum(orders.mvno), sum(orders.cctv), sum(orders.ss)
                            FROM orders 
                            JOIN info ON orders.staff_id = info.staff_id
                            WHERE orders.date = '{current_date}'
                            GROUP BY info.full_name
                            ORDER BY info.full_name
                        """)
        rows = self.cur.fetchall()
        result = []
        for row in rows:
            result.append([row[0].split()[0], row[1], row[2], row[3], row[4], row[5]])
        return result

    def get_staff_id(self, telegram_id):
        self.cur.execute("SELECT telegram_id FROM info WHERE telegram_id = ?", (telegram_id, ))
        return self.cur.fetchone()

    def get_staff_username(self, telegram_username):
        if self.cur.execute("SELECT telegram_username FROM staff WHERE = ?", (telegram_username, )):
            return True
        else:
            return False

    def get_full_name(self, telegram_id):
        self.cur.execute("SELECT full_name FROM info WHERE telegram_id = ?", (telegram_id, ))
        return self.cur.fetchone()[0]