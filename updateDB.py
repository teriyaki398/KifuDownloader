# using:utf-8

import shogi
from tqdm import tqdm
from pymongo import MongoClient
from Kifu.Downloader import ShogiwarsDownloader
from Kifu.SituationDB import SituationDB

user_name = input("user name : ")
rules = ["10m", "3m", "10s"]

# もし新規に対局データがあればDBに追加しておく
shogiwars = ShogiwarsDownloader(user_name)
for i in rules:
    print("Searching " + i)
    shogiwars.saveAllDataDB(i)


# 棋譜データベースへアクセス
client = MongoClient("localhost", 27017)
db = client["Shogiwars"]
games_collection = db[user_name + "_games"]
situation_collection = db[user_name + "_situation"]

games = []
for i in games_collection.find():
    games.append(i)

situationDB = SituationDB(user_name)
for i in tqdm(games):
    situationDB.registerSituation(i)


