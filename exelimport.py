import sqlite3
import pandas as pd

con = sqlite3.connect('items.db')
wb = pd.read_excel('test.xlsx', sheet_name=None)

for sheet in wb:
    wb[sheet].to_sql(sheet, con, index=False)
con.commit()
con.close()