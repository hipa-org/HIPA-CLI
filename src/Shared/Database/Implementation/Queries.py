DB_INS_UPDATE = """INSERT INTO updates (name, hash, state, timestamp, speed) VALUES(%s,%s,%s,%s,%s)"""

DB_SEL_UPDATE = """SELECT count(name) FROM updates WHERE name = %s"""
