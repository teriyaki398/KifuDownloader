# coding: utf-8

from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import requests
import re

class ShogiwarsKifuDL:
        """
        将棋ウォーズの棋譜をダウンロードする．
        
        user_name : string
                将棋ウォーズのユーザID
        """

        def __init__(self, user_name):
                self.url = "https://shogiwars.heroz.jp/users/history/"+user_name+"/web_app"

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
                        date = date[0][-1*(len("XXXX/XX/XX XX")):] + ":" + date[1][:len("XX")]

                        url = i.find(class_="game_replay").find("a").get("href")

                        tag = i.find_all(class_="hashtag_badge")
                        tag = [j.text for j in tag]

                        print(date)
                        print(url)
                        print(tag)
                        print()
                        
                        log.append({"date":date, "url":url, "tag":tag})

                return log

