# Follows https://www.dataquest.io/blog/python-pandas-databases/

import sqlite3
import pandas as pd

# Forcibly display all columns when using PyCharm
# See https://stackoverflow.com/a/50947606/2176546
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)

conn = sqlite3.connect('../flights.db')

df = pd.read_sql_query('select * from airlines limit 5;', conn)
print(df)


# cur = conn.cursor()
# cur.execute('select * from airlines limit 5;')

# coords = cur.execute("""
# select cast(longitude as float),
#        cast(latitude as float)
# from airports;
# """).fetchall()

# print(coords)

# cur.close()
conn.close()
