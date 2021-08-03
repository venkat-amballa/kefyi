# import pandas as pd
# import os
# import sqlite3
# address = 'sqlite:///data.db'
# conn = sqlite3.connect(address)
# cur = conn.cursor()
#
# path = 'C:\\Users\\mutya\\OneDrive\\Documents\\startup-projects\\inventory_management\\misc\\op'
# for file in os.listdir(path)[:1]:
#     pd_items = pd.read_csv(os.path.join(path, file), index_col=0)
#
# print(pd_items.columns)
