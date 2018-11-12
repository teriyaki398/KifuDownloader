# using:utf-8

import shogi
import os
from tqdm import tqdm
from pymongo import MongoClient
from Kifu.Downloader import ShogiwarsDownloader

user_name = input("user name : ")
rules = ["10m", "3m", "10s"]

if os.path.exists("./ShogiwarsKifu") == False:
    os.mkdir("./ShogiwarsKifu")
if os.path.exists("./ShogiwarsKifu/" + user_name) == False:
    os.mkdir("./ShogiwarsKifu/" + user_name)


# 取得できる分の棋譜を取得する
shogiwars = ShogiwarsDownloader(user_name)
for i in rules:
    shogiwars.saveAllDataLocal(i)




