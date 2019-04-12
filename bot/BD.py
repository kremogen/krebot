import sqlite3

conn = sqlite3.connect("players.db")
cursor = conn.cursor()

cursor.execute('CREATE TABLE players(id integer, '
               'bonus integer, '
               'balance integer, '
               'date text, '
               'profit integer,'
               ' activity integer,'
               ' farm_b integer,'
               ' farm_g integer,'
               ' farm_i integer, '
               'farm_l integer, '
               'farm_q integer)')

conn.commit()