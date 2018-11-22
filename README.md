# ローカルにダウンロードする方法
```python
% python downloadKifu.py
```

将棋ウォーズ側の仕様変更により使えなくなる可能性はある

# python-shogi についてのメモ
将棋のPython ライブラリ  
https://github.com/gunyarakun/python-shogi

1. pip を使ってインストール
```
$ pip install python-shogi
```

2. 将棋盤を描画するまで
```
>>> import shogi
>>> board = shogi.Board()
>>> print(board.kif_str())
後手の持駒：
  ９ ８ ７ ６ ５ ４ ３ ２ １
+---------------------------+
|v香v桂v銀v金v玉v金v銀v桂v香|一
| ・v飛 ・ ・ ・ ・ ・v角 ・|二
|v歩v歩v歩v歩v歩v歩v歩v歩v歩|三
| ・ ・ ・ ・ ・ ・ ・ ・ ・|四
| ・ ・ ・ ・ ・ ・ ・ ・ ・|五
| ・ ・ ・ ・ ・ ・ ・ ・ ・|六
| 歩 歩 歩 歩 歩 歩 歩 歩 歩|七
| ・ 角 ・ ・ ・ ・ ・ 飛 ・|八
| 香 桂 銀 金 玉 金 銀 桂 香|九
+---------------------------+
先手の持駒：
```

**ポイント**  
入出力はSFEN形式で行う．  
http://ch.nicovideo.jp/kifuwarabe/blomaga/ar795371

+ 駒を動かす
```
>>> board.push(shogi.Move.from_usi(["操作"]))
```

+ SFEN形式の文字列を取得
```
>>> board.sfen()
```

# 将棋ウォーズ独自の棋譜フォーマット
こちらを参考にしつつ推測した結果  
https://github.com/tosh1ki/shogiwars

以下のような形式になってる．
```bash
+7776FU,L3598
-8384FU,L3598
+6766FU,L3597
+8877KA,L3597
...
SENTE_WIN_CHECKMATE
```

**ポイント**

+ 先手の手には`+`，後手の手には`-`が先頭につく．
+ 前半4桁の数字XXYYは，XX -> YY に駒を移動したことを表す.
+ 数字の後に駒の種類を表す文字が来る．

| 記号 | 駒 |
|:---:|:---:|
| FU  | 歩  |
| KY  | 香  |
| KE  | 桂  |
| GI  | 銀  |
| KI  | 金  |
| KA  | 角  |
| HI  | 飛  |
| OU  | 玉  |
| TO  | と金|
| NY  | 成香|
| NK  | 成桂|
| NG  | 成銀|
| UM  | 馬  |
| RY  | 龍  |

例えば▲７六歩 は `+7776FU` となり，▲７二金打 は `+0072KI` となる．ちなみに駒を成る場合は記号を変えるだけ．例えば▲４六角〜▲１三角成は`+4613UM`で，不成は`+4613KA`となる．


# kivy - Installation on OS X
https://kivy.org/doc/stable/installation/installation-osx.html

1. homebew を使ってインストール
```bash
$ brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
```

2. pip で Cython と Kivy をインストール
```bash
pip install Cython==0.26.1
pip install kivy
```

# mongoDB - Installation on OS X

1. homebrew を使ってインストール
```bash
$ brew install mongodb
```

+ mongodb の起動
```bash
$ brew services start mongodb
```

+ 起動しているかどうかの確認
```bash
$ brew services list
```

+ mongodb の停止
```bash
$ brew services stop mongodb
```

+ 特定のコレクションに含まれているデータを全て表示する
```
$ mongo
> show dbs
> use [db name]
> show collections
> db.[collection name].find()
``` 

|コマンド | 操作 |
|:---|:---|
| `mongo` | mongoDB のシェルを起動 | 
| `show dbs` | データベース一覧を表示 | 
| `use [name]` | 使用するデータベースを変更 | 
| `show collections` | コレクション一覧を表示 |


# pymongo の使い方

1. pip を使ってインストール
```bash
pip install pymongodb
```

+ mongoDBへのアクセス
```
>>> from pymongo import MongoClient
>>> client = MongoClient("localhost", 27017)
```

+ データベースを使用（なければ作成）
```
>>> db = client["db_name"]
```

+ コレクションを使用（なければ作成）
```
>>> collection = db["collection_name"]
```

+ コレクションに追加
```
>>> type(post)
<class 'dict'>
>>> collection.insert_one(post)
```

複数追加したい場合は，辞書のリストを作成し，

```
>>> type(post)
<class 'list'>
>>> collection.insert_many(post)
```

+ コレクションを参照

全て取ってくる
```
>>> collection.find()
```

`Cursor` というイテレータオブジェクトが返ってくる．
for文などで回すことで一つずつ参照できる．

一つ取ってくる
```
>>> collection.find_one({"key": "000"})
```
引数として渡した条件に一致するデータが返ってくる
