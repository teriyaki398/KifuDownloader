# using:utf-8

import shogi
from tqdm import tqdm
from pymongo import MongoClient
from Kifu.Player import KifuPlayer

"""
棋譜を進めながら、盤面を保存していく。
"""

class SituationDB:
    
    def __init__(self, user_name):
        self.user_name = user_name

        self.client = MongoClient("localhost", 27017)
        self.db = self.client["Shogiwars"]
        self.situation_collection = self.db[user_name + "_situation"]
        self.kif_collection = self.db[user_name + "_games"]

    def registerSituation(self, game):
        """
        game : dict 

        データベースに登録してあるJSONのゲーム情報を受け取り、
        盤面を進めながら盤面を登録してゆく
        """

        # 盤面
        board = shogi.Board()

        # ゲーム情報から棋譜を取得し、sfen形式に変換する
        kifu = game["kifu"]
        converter = KifuPlayer(kifu)
        kifu = converter.warsToSfen()

        for i in range(len(kifu)):
            # 一手進める
            board.push(shogi.Move.from_usi(kifu[i]))

            sfen = board.sfen().split(" ")
            situation = sfen[0] + " " + sfen[1] + " " + sfen[2]

            # 未登録の盤面なら追加する
            if self.situation_collection.find_one({"situation": situation}) == None:
                post = {
                    "situation": situation,
                    "file_list": [[game["file_name"], i+1]]
                }
                self.situation_collection.insert_one(post)
            # 同一盤面が発見できたら
            else:
                s = self.situation_collection.find_one({"situation": situation})
                file_list = s["file_list"]
                
                # もし過去に追加したことのない情報なら追加する
                new_situ = [game["file_name"], i+1]
                if new_situ not in file_list:
                    file_list.append([game["file_name"], i+1])
                    self.situation_collection.update({"situation": situation}, {"$set": {"file_list": file_list}})
            
