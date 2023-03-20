

class DataBase():
    
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
            telegram_id INTEGER UNIQUE NOT NULL,
            role TEXT DEFAULT 'intern',
            full_name TEXT,
            phone_number INTEGER,
            career_start_date TEXT,
            career_close_date TEXT DEFAULT NULL,
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orders
        (
            id INTEGER,
            staff_id INTEGER NOT NULL,
            bbi INTEGER,
            tv INTEGER,
            mvno INTEGER,
            cctv INTEGER,
            ss INTEGER,
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        );""")
        self.con.commit()

    
    def add_new_staff(self, telegram_username) -> int:
        self.cur.execute("INSERT INTO staff (telegram_username) VALUES (?);", (telegram_username,))
        self.con.commit()
        return self.cur.lastrowid
    
    def add_new_order(self, telegram_id, bbi, tv, mvno, cctv, ss):
        self.cur.execute("""
            INSERT INTO orders (staff_id, bbi, tv, mvno, cctv, ss)
            SELECT staff.id, ?, ?, ?, ?, ?
            FROM info
            JOIN staff ON info.staff_id = staff.id
            WHERE info.telegram_id = ?
        """, (bbi, tv, mvno, cctv, ss, telegram_id))
        self.con.commit()

    def add_new_staff_info(self, data):
        self.cur.execute("INSERT INTO info (telegram_id, full_name, phone_number, career_start_date) VALUES (?, ?, ?, ?)", 
                         (data["telegram_id"], data["full_name"], data["phone_number"], data["career_start_date"]))
        self.con.commit()