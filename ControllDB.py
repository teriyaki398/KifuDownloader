# using:utf-8

from pymongo import MongoClient
import shogi

client = MongoClient('localhost', 27017)

user_name = input("user_name : ")

db = client["Shogiwars"]
collection = db[user_name + "_games"]

games = []
for i in collection.find():
    games.append(i)

# 日付け順にソート
games = sorted(games, key=lambda x:x["date"])


board = shogi.Board()

class KifuPlayer():

    kifu = []

    def __init__(self, kifu):
        self.board = shogi.Board()
        self.kifu = kifu

    
    def play(self):
        

