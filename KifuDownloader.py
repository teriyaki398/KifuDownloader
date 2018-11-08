# coding: utf-8

from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from glob import glob
import requests
import re
import os

class ShogiwarsKifuDL:
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
                self.folder_path = "../ShogiwarsKifu/" + user_name + "/"
                self.file_lis = glob(self.folder_path + "*")

                # 指定したユーザー名のフォルダが存在していなければ作成する
                if os.path.exists(self.folder_path) == False:
                        os.mkdir(self.folder_path)


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
                rules = {"10m": "", "3m":"sb", "10s":"s1"}
                payload = {"gtype": rules[rule], "locale":"ja", "v":"0.0.0", "page":page}
                res = requests.get(self.url, params=payload)

                return res.text


        def extractURL(self, text):
                """
                HTML から日付，URL，対局内容のハッシュタグを取得し，辞書のリストで返す

                text : string
                        HTML の文字列
                """
                soup = BeautifulSoup(text.replace("\\", ""))
                lis = soup.find_all(class_ = re.compile("contents.*"))

                log = []
                for i in lis:
                        date = i.find(class_="game_date").text
                        date = date.split(":")
                        date = date[0][-1*(len("XXXX/XX/XX XX")):] + "-" + date[1][:len("XX")]
                        date = date.replace("/", "-")
                        date = date.replace(" ", "-")
                        
                        players = i.find(class_="players").find_all("a")
                        players = [j.text[18:].replace("\u2009", " ")[:-1] for j in players]

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
                将棋ウォーズの棋譜URL から棋譜の部分だけを抽出し，文字列で返す

                url : string
                        棋譜のURL
                """
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "lxml")
                
                kifu = soup.find_all("script")[13].text
                kifu = kifu.split("receiveMove(")[1].split(");")[0][1:-1]
                kifu = kifu.replace("\t", "\n")
                
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
        

        def saveAllData(self, rule):
                """
                取得できる棋譜をローカルに保存していく
                
                rule : string
                        10分切れ負け 10m
                        3分切れ負け 3m
                        10秒将棋 10s
                """

                data = []
                page = 1
                flag = True

                while flag:
                        sleep(2)
                        res = self.getHTML(rule, page)
                        page += 1

                        data = self.extractURL(res)

                        # 最後のページの抽出なら，終了
                        if len(data) != 10:
                                flag = False

                        for i in tqdm(data):
                                # もしすでにファイルが存在していたらbreak して終了
                                file_name = self.folder_path + i["date"] + "-" + i["sente"].split(" ")[0] + "-" + i["gote"].split(" ")[0]
                                if os.path.exists(file_name):
                                        flag = False
                                        break
                                
                                with open(file_name, "w") as f:
                                        text = ""
                                        text += "date " + i["date"] + "\n"
                                        text += "rule " + rule + "\n"
                                        text += "sente " + i["sente"] + "\n"
                                        text += "gote " + i["gote"] + "\n"
                                        text += "url " + i["url"] + "\n"
                                        text += "tag "
                                        for j in range(len(i["tag"])):
                                                text += i["tag"][j] + " "
                                        text += "\n"
                                        
                                        text += self.extractKifu(i["url"])

                                        f.write(text)
        
                                
                        