"""
# File       : mongo_class.py
# Time       ：2022/2/25 12:40 PM
# Author     ：Andy
# version    ：python 3.9
# Description：
"""

import pymongo
import json
from pandas import DataFrame

class my_mongo:

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.client = pymongo.MongoClient(self.host, self.port)


    def df_to_bson(self, data):
        data = json.loads(data.T.to_json()).values()
        return data

    def df_to_mongodb(self, db_name, col_name, data):
        col = self.client[db_name][col_name]
        bson_data = self.df_to_bson(data)
        col.insert_many(bson_data)

    def col_to_df(self, db_name, col_name, query={}, return_col={'_id': 0}):
        col = self.client[db_name][col_name]
        cursor = col.find(query, return_col)
        df = DataFrame(list(cursor))
        return df

    def get_distinct(self, db_name, col_name, key='token'):
        col = self.client[db_name][col_name]
        return col.distinct(key)

if __name__ == '__main__':
    my_mongo = my_mongo(host='127.0.0.1', port=27017)