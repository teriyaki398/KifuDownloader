# using:utf-8

import shogi
import json
from time import sleep

class KifuPlayer:
    """
    将棋ウォーズ形式の棋譜を動かしてみる

    kifu : list<string>
        将棋ウォーズ形式の棋譜のリスト
    """

    kifu = []

    def __init__(self, kifu):
        """
        kifu : list<string>
            将棋ウォーズ形式の棋譜リスト

        pieces : dict<string: list<string>>
            将棋ウォーズ形式の駒記号とsfen形式の駒記号の対応辞書
            sfen形式では先後を大文字・小文字で区別するのでリストにして持たせる
        """

        # 時間情報は余分なので削る
        self.kifu = [i.split(",")[0] for i in kifu]

        self.pieces_table = {
                "FU": ["P", "p"], "KY": ["L", "l"], "KE": ["N", "n"], "GI": ["S", "s"],
                "KI": ["G", "g"], "KA": ["B", "b"], "HI": ["R", "r"], "OU": ["K", "k"],
                "TO": ["+P", "+p"], "NY": ["+L", "+l"], "NK": ["+N", "+n"], "NG": ["+S", "+s"],
                "UM": ["+B", "+b"], "RY": ["+R", "+r"]
        }

        self.narigoma = ["TO", "NY", "NK", "NG", "UM", "RY"]

        self.column_symbol = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i"]


    def play(self):
        """
        ウォーズの棋譜を再生する
        """
        
        kifu = self.warsToSfen()
        board = shogi.Board()
        print(board.kif_str())
        for i in kifu:
            sleep(0.5)
            board.push(shogi.Move.from_usi(i))
            print(board.kif_str())
        return 

        
    
    def warsToSfen(self):
        """
        将棋ウォーズの棋譜をsfen形式に変換して，リストで返す
        kifu : list<string>
            変換したい棋譜のリスト
        """
        # 変換後の棋譜を格納するリスト
        ans = []

        # 棋譜をシミュレートする将棋盤
        board = shogi.Board()

        # 一手一手変換する
        # 最後の一行は勝敗に関する情報なので取り除く
        kifu = self.kifu[:-1]

        # 一手も指さずに接続切れ勝ち（負け）になった時は、
        # kifuの長さが0になるので変換しない
        if len(kifu) == 1:
            return ans

        for move in kifu:

            teban       = move[0]
            wars_from   = move[1:3]
            wars_to     = move[3:5]
            wars_piece  = move[5:7]

            # リストに格納する手
            sfen_move = ""

            # 打ち駒の場合
            if wars_from == "00":
                sfen_to     = wars_to[0]    + self.column_symbol[int(wars_to[1])]
                
                # 打った駒の sfenシンボルを調べる
                piece = ""
                if teban == "+":
                    piece = self.pieces_table[wars_piece][0]
                elif teban == "-":
                    piece = self.pieces_table[wars_piece][1]
                
                sfen_move = piece + "*" + sfen_to

            # 駒の移動の場合
            else:
                sfen_from   = wars_from[0]  + self.column_symbol[int(wars_from[1])]
                sfen_to     = wars_to[0]    + self.column_symbol[int(wars_to[1])]
                sfen_move   = sfen_from + sfen_to

                # 移動後のピースが成駒かどうかを調べる
                # もしこの移動で成っていたら成りの操作を追記する必要がある
                if wars_piece in self.narigoma:
                    current_piece = self.retPosPiece(board, wars_from)
                    # もし既に成駒なら + がついてるはず
                    if current_piece[0] != "+":
                        sfen_move += "+"

            # 答えに格納し，将棋盤の手を進める
            ans.append(sfen_move)
            board.push(shogi.Move.from_usi(sfen_move))
            
        return ans

    def retPosPiece(self, board, pos):
        """
        指定した座標に現在存在している駒が何かを調べる

        board : python-shogi の将棋盤インスタンス
        
        pos : string
            ウォーズ形式の座標
            ７六 なら "76"
        """
        # 盤面情報の部分だけを抜き出し，行ごとに分割する
        board = board.sfen().split(" ")[0].split("/")

        # 列情報は pos の左， 行情報は pos の右側に該当する
        # ただし，二次元配列上では行の番号は 0からなので デクリメントしておく
        # 列に関しても同じだが，列は番号付けの方向が逆なので -1 * c で参照することでうまくいく
        c = int(pos[0])
        r = int(pos[1]) - 1

        row = board[r]
        col = []
        while len(col) < 9:
            if row[0] == "+":
                col.append(row[:2])
                row = row[2:]
            elif row[0].isdecimal():
                n = int(row[0])
                for i in range(n):
                    col.append(" ")
                row = row[1:]
            else:
                col.append(row[:1])
                row = row[1:]
        return col[-1 * c]
        

