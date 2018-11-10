# using:utf-8

import shogi
from tqdm import tqdm
from pymongo import MongoClient
from KifuPlayer import KifuPlayer
from KifuDownloader import ShogiwarsKifuDL


user_name = input("user name : ")
rules = ["10m", "3m", "10s"]

# もし新規に対局データがあればDBに追加しておく
shogiWarsKifuDL = ShogiwarsKifuDL(user_name)
for i in rules:
    shogiWarsKifuDL.saveAllDataDB(i)

# 棋譜データベースへアクセス
client = MongoClient("localhost", 27017)
db = client["Shogiwars"]
collection = db[user_name + "_games"]

