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

url = "https://shogiwars.heroz.jp/users/history/"+"t3rry"+"/web_app"

def getHTML(rule, page):
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
    payload = {"gtype": rules[rule], "locale":"ja", "page":page, "locale":"ja"}

    try:
            res = requests.get(url, params=payload)
    except:
            print("Request Error")
            sys.exit()

    return res.text

def extractURL(text):
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
