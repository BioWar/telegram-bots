import sqlite3
import logging

USED = 1
UNUSED = 0

class SQLighter:
    def __init__(self, database):
        try:
            self.connection = sqlite3.connect(database)
        except Exception as err:
            print(f'[Error] {err}.')
            exit(1)
        self.cursor = self.connection.cursor()
        
    def create_article(self, article):
        sql = '''INSERT INTO ARTICLES(Article_Name, Used_in_channel)
                 VALUES(?,?)'''
        all_articles = [article[1] for article in self.cursor.execute("SELECT * FROM ARTICLES").fetchall()]
        if article in all_articles:
            logging.info('[INFO] Article already exist: %s' % (article))
            return
        else:
            logging.info('[INFO] Article created: %s' % (article))
            self.cursor.execute(sql, (article, False))
            self.connection.commit()
            return self.cursor.lastrowid

    def select_all(self):
        """Get all rows"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM ARTICLES").fetchall()

    def select_last(self):
        """Get last row"""
        last = len(self.select_all())
        with self.connection:
            return self.cursor.execute("SELECT * FROM ARTICLES WHERE generated_id = ?",
                                       (last,)).fetchall()

    def select_last_unused(self):
        """Get last unused row"""
        all_articles = self.cursor.execute("SELECT * FROM ARTICLES").fetchall()
        for article in all_articles:
            if article[2] == 0:
                return article 
        
    def select_all_used(self):
        """Get all used row"""
        all_articles = self.cursor.execute("SELECT * FROM ARTICLES").fetchall()
        used_articles = []
        for article in all_articles:
            if article[2] == 1:
                used_articles.append(article)
        return used_articles
        
    def set_all_to_unused(self):
        sql = '''UPDATE ARTICLES SET Used_in_channel = 0'''
        self.cursor.execute(sql)
        self.connection.commit()
        return 
    
    def change_status(self, row, status):
        """Change status to used"""
        sql = '''UPDATE ARTICLES SET Used_in_channel = ? WHERE generated_id = ?'''
        self.cursor.execute(sql, (status, row,))
        self.connection.commit()
        logging.info('[INFO] Status of article changed: %s' % (self.select_single(row)))
        return 
    
    def select_single(self, rownum):
        """Get one row by rownum"""
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM ARTICLES WHERE generated_id = ?", (rownum,)
            ).fetchall()

    def count_rows(self):
        """Count amount or rows"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM ARTICLES").fetchall()
            return len(result)

    def close(self):
        """Close db connection"""
        self.connection.close()
        logging.info('[INFO] Conection closed.')
        
