import sqlite3
from threading import Lock


class BotDB:

    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = Lock()

    def user_exists(self, user_id):
        with self.lock:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                res = cursor.execute('SELECT `id` FROM `dbvisa` WHERE `user_id` = ?', (user_id,))
                conn.commit()
                return bool(len(res.fetchall()))
    
    def get_user_id(self, user_id):
        with self.lock:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                res = cursor.execute('SELECT `id` FROM `dbvisa` WHERE `user_id` = ?', (user_id,))
                return res.fetchone()[0]
    
    def add_user(self, user_id):
        with self.lock:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('REPLACE INTO `dbvisa` (`user_id`) VALUES (?)', (user_id,))
                conn.commit()
    
    def add_country(self, user_id, country):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO `dbcountry` (`user_id`, `country`) VALUES (?, ?)',
                                (self.get_user_id(user_id),
                                country))
            conn.commit()
    
    def get_country(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            res = cursor.execute('SELECT * FROM `dbcountry` WHERE `user_id` = ?',
                                (self.get_user_id(user_id),))
            return res.fetchone()[2]
    
    def add_type(self, user_id, type):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO `dbtype` (`user_id`, `type`) VALUES (?, ?)',
                                (self.get_user_id(user_id),
                                type))
            conn.commit()
        
    def get_type(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT * FROM `dbtype` WHERE `user_id` = ?',
                                    (self.get_user_id(user_id),))
            return res.fetchone()[2]
    
    def add_trip(self, user_id, trip):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO `dbtrip` (`user_id`, `trip`) VALUES (?, ?)',
                                (self.get_user_id(user_id),
                                trip))
            conn.commit()
    
    def get_trip(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT * FROM `dbtrip` WHERE `user_id` = ?',
                                    (self.get_user_id(user_id),))
            return res.fetchone()[2]
    
    def add_consulate(self, user_id, cosulate):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO `dbconsulate` (`user_id`, `consulate`) VALUES (?, ?)',
                                (self.get_user_id(user_id),
                                cosulate))
            conn.commit()
    
    def get_consulate(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT * FROM `dbconsulate` WHERE `user_id` = ?',
                                    (self.get_user_id(user_id),))
            return res.fetchone()[2]
    
    def get_bool_consulate(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT * FROM `dbconsulate` WHERE `user_id` = ?',
                                    (self.get_user_id(user_id),))
            return bool(res.fetchone()[2])
    
    def add_category(self, user_id, category):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('REPLACE INTO `dbcategory` (`user_id`, `category`) VALUES (?, ?)',
                                (self.get_user_id(user_id),
                                category))
            conn.commit()
    
    def get_category(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT * FROM `dbcategory` WHERE `user_id` = ?',
                                    (self.get_user_id(user_id),))
            return res.fetchone()[2]

