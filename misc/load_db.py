import pandas as pd
import numpy as np
import os
import sqlite3

def all_df_list():
    df_list = []
    # path = 'C:\\Users\\mutya\\OneDrive\\Documents\\startup-projects\\inventory_management\\misc\\op'
    path = 'op'
    for file in os.listdir(path):
        pd_items = pd.read_csv(os.path.join(path, file), index_col=0)
        cat_name = file.split('.')[0]
        pd_items['category'] = cat_name
        pd_items.rename(columns={'weight':'size',
                                 'actual_price':'retail_price',
                                 'striked_price':'max_retail_price'}, inplace=True)
        print(pd_items.shape)
        df_list.append(pd_items)
        # print(pd_items.head().values)

    df = pd.concat(df_list)
    df = df[['name', 'weight', 'retail_price', 'max_retail_price','category', 'url']]
    df.to_csv('final_df.csv')
    print(df.shape, pd_items.columns)
    return df_list, df


final_df = pd.read_csv('final_df.csv')
print(np.unique([val.strip('Size: ') for val in final_df['weight'].values]))

# address = f"sqlite:///{os.path.join(os.getcwd(),'data.db')}"
address = "C:\\Users\\mutya\\OneDrive\\Documents\\startup-projects\\inv_management_v1\\misc\\data.db"
conn = sqlite3.connect(address)
cur = conn.cursor()
# id INTEGER NOT NULL,
# 	name VARCHAR(80),
# 	category VARCHAR(40) NOT NULL,
# 	actual_price FLOAT NOT NULL,
# 	wholesale_price FLOAT NOT NULL,
# 	retail_price FLOAT NOT NULL,
# 	quantity INTEGER NOT NULL,
# 	PRIMARY KEY (id)

for df in final_df:
    # cur.executemany("select count(*) from products;")
    pass

for row in cur.fetchall():
    print(row)