import sqlite3 

database = sqlite3.connect('datebase.db')
cursor = database.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
Username text,
Surname text,
Password text
)
""")