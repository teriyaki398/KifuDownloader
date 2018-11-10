import shogi

def warsToSfen(kifu):
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
    kifu = kifu[:-1]
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

            # 移動後のピースが成駒かどうかを調べる
            # もしこの移動で成っていたら成りの操作を追記する必要がある
            if wars_piece in self.narigoma:
                current_piece = self.retPosPiece(board, wars_from)
                # もし既に成駒なら + がついてるはず
                if current_piece[0] == "+":
                    sfen_move = sfen_from + sfen_to
                else:
                    sfen_move = sfen_from + sfen_to + "+"

        # 答えに格納し，将棋盤の手を進める
        ans.append(sfen_move)
        board.push(shogi.Move.from_usi(sfen_move))
        
    return ans

