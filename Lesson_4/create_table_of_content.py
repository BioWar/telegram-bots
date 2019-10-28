import sqlite3
import os
import bot_for_medium

if not "ArticleMedium.db" in os.listdir("."):
    conn = sqlite3.connect("ArticleMedium.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE ARTICLES ([generated_id] INTEGER PRIMARY KEY, [Article_Name] text, [Used_in_channel] BOOLEAN)"""
    )
    conn.commit()
    c.close()
else:
    conn = sqlite3.connect("ArticleMedium.db")
    c = conn.cursor()
