# coding: utf-8

from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from glob import glob
from pymongo import MongoClient
import requests
import json
import re
import os
import sys

class ShogiwarsDownloader:
        """
        将棋ウォーズの棋譜をダウンロードする．
        
        user_name : string
                将棋ウォーズのユーザID
        """

        url = ""
        user_name = ""
        folder_path = ""
        file_lis = None

        def __init__(self, user_name):
                self.user_name = user_name
                self.url = "https://shogiwars.heroz.jp/users/history/"+self.user_name+"/web_app"


        def getHTML(self, rule, page):
                """
                対局履歴のHTMLを取得して，string で返す

                rule : string
                        10分切れ負け 10m
                        3分切れ負け 3m
                        10秒将棋 10s

                page : int
                        ページ番号 1 ~ n
                """
                sleep(2)
                rules = {"10m": "", "3m":"sb", "10s":"s1"}
                payload = {"gtype": rules[rule], "locale":"ja", "page":page}

                try:
                        res = requests.get(self.url, params=payload)
                except:
                        print("Request Error")
                        sys.exit()

                return res.text


        def extractURL(self, text):
                """
                HTML から日付，URL，対局内容のハッシュタグを取得し，辞書のリストで返す

                text : string
                        HTML の文字列
                """
                soup = BeautifulSoup(text.replace("\\", ""), "lxml")
                lis = soup.find_all(class_ = re.compile("contents.*"))

                log = []
                for i in lis:
                        date = i.find(class_="game_date").text
                        date = date.split(":")
                        date = date[0][-1*(len("XXXX/XX/XX XX")):] + "-" + date[1][:len("XX")]
                        date = date.replace("/", "-")
                        date = date.replace(" ", "-")
                        
                        players = i.find(class_="players").find_all("a")
                        players = [j.text.replace("\n", "").replace(" ", "") for j in players]

                        url = i.find(class_="game_replay").find("a").get("href")
                        url = "http:" + url

                        tag = i.find_all(class_="hashtag_badge")
                        tag = [j.text for j in tag]
                        
                        log.append({
                                "date":date, 
                                "sente":players[0], 
                                "gote":players[1], 
                                "url":url, 
                                "tag":tag
                                })

                return log

        
        def extractKifu(self, url):
                """
                将棋ウォーズの棋譜URL から棋譜の部分だけを抽出し，リストで返す

                url : string
                        棋譜のURL
                """
                sleep(2)
                try:
                        res = requests.get(url)
                except:
                        print("Request Error")
                        sys.exit()

                soup = BeautifulSoup(res.text, "lxml")
                
                kifu = soup.find_all("script")[13].text
                kifu = kifu.split("receiveMove(")[1].split(");")[0][1:-1]
                kifu = kifu.split("\t")
                
                return kifu

        
        def getAllData(self, rule):
                """
                指定されたルールで取得できる全てのデータを取得する
                ただしすでにローカルに保存されているものは弾く

                rule : string
                        10分切れ負け 10m
                        3分切れ負け 3m
                        10秒将棋 10s
                """
                data = []
                page = 1
                
                while True:
                        sleep(2)
                        res = self.getHTML(rule, page)
                        log = self.extractURL(res)
                        
                        data += log
                        page += 1

                        if len(log) != 10:
                                break

                return data
        

        def saveAllDataLocal(self, rule):
                """
                取得できる棋譜をローカルにJSON形式で保存していく
                
                rule : string
                        10分切れ負け 10m
                        3分切れ負け 3m
                        10秒将棋 10s
                """

                self.folder_path = "./ShogiwarsKifu/" + self.user_name + "/"
                self.file_lis = glob(self.folder_path + "*")

                # 指定したユーザー名のフォルダが存在していなければ作成する
                if os.path.exists(self.folder_path) == False:
                        os.mkdir(self.folder_path)

                data = []
                page = 1
                flag = True

                while flag:
                        res = self.getHTML(rule, page)
                        page += 1

                        data = self.extractURL(res)
                        # 最後のページの抽出なら，終了
                        if len(data) != 10:
                            flag = False

                        for i in tqdm(data):
                                # もしすでにファイルが存在していたらbreak して終了
                                file_name = self.folder_path + i["date"] + "-" + i["sente"].split(" ")[0] + "-" + i["gote"].split(" ")[0]+".json"
                                if os.path.exists(file_name):
                                        flag = False
                                        break

                                with open(file_name, "w") as f:
                                        kifu = self.extractKifu(i["url"])
                                        i["kifu"] = kifu
                                        json.dump(i, f)
        
        def saveAllDataDB(self, rule):
                """
                取得できる棋譜をデータベースに保存していく
                使用するデータベースはMongo DB

                データベース名は "Shogiwars"
                コレクション名は "[ユーザーID]_games"
                としている

                格納する形式は
                {
                        "date"          : 日付
                        "sente"         : 先手番のユーザー名 
                        "gote"          : 後手番のユーザー名
                        "url"           : 将棋ウォーズのURL
                        "tag"           : 戦型のハッシュタグ
                        "file_name"     : ローカルに保存する際のファイル名
                        "rule"          : 対局ルール
                        "kifu"          : 棋譜データ（ウォーズ形式）

                }
                
                rule : string
                        10分切れ負け 10m
                        3分切れ負け 3m
                        10秒将棋 10s
                """

                client = MongoClient("localhost", 27017)
                db = client["Shogiwars"]
                collection = db[self.user_name + "_games"]

                data = []
                page = 1
                flag = True

                while flag:
                        res = self.getHTML(rule, page)
                        page += 1

                        data = self.extractURL(res)
                        # 最後のページの抽出なら，終了
                        if len(data) != 10:
                            flag = False

                        for i in tqdm(data):
                                # DBを一意に検索できるように"ファイル名"を追加する
                                file_name = i["date"] + "-" + i["sente"].split(" ")[0] + "-" + i["gote"].split(" ")[0]+".json"
                                i["file_name"] = file_name
                                
                                # すでにDBに存在するファイル名ならbreak して終了
                                if collection.find_one({"file_name": file_name}) != None:
                                        flag = False
                                        break

                                # 棋譜データをDL
                                kifu = self.extractKifu(i["url"])
                                i["rule"] = rule
                                i["kifu"] = kifu

                                # DB に追加する
                                collection.insert_one(i)

                
