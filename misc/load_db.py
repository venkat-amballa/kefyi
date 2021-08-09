import pandas as pd
import numpy as np
import os
import sqlite3

COLS = [
    "name",
    "unit",
    "retail_price",
    "actual_price",
    "wholesale_price",
    "category",
    "description",
    "quantity",
    "url",
]


def all_df_list():
    df_list = []
    # path = 'C:\\Users\\mutya\\OneDrive\\Documents\\startup-projects\\inventory_management\\misc\\op'
    path = "op"
    save_path = "op_refactored"
    for file in os.listdir(path):
        pd_items = pd.read_csv(os.path.join(path, file), index_col=0)
        cat_name = file.split(".")[0]

        pd_items["category"] = cat_name

        pd_items.rename(
            columns={
                "weight": "unit",
                "actual_price": "retail_price",
                "striked_price": "actual_price",
            },
            inplace=True,
        )
        pd_items["description"] = "this item is " + pd_items["name"]
        pd_items["wholesale_price"] = pd_items["retail_price"]
        pd_items["quantity"] = 20
        pd_items.to_csv(os.path.join(save_path, file))
        df_list.append(pd_items)

    df = pd.concat(df_list)
    df = df[COLS]
    df.loc[df['actual_price'].isna(), "actual_price"] = 0
    df.to_csv("final_df1.csv", index=False)
    print(df.shape, pd_items.columns)
    return df_list, df


all_df_list()


def load():
    final_df = pd.read_csv("final_df.csv")
    print(np.unique([val.strip("Size: ") for val in final_df["weight"].values]))

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
