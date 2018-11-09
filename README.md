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

2. mongodb の起動
```bash
$ brew services start mongodb
```

3. 起動しているかどうかの確認
```bash
$ brew services list
```

4. mongodb の停止
```bash
$ brew services stop mongodb
```

|コマンド | 操作 |
|:---|:---|
| `mongo` | mongoDB のシェルを起動 | 
| `show dbs` | データベース一覧を表示 | 
| `use [name]` | 使用するデータベースを変更 | 
| `show collections` | コレクション一覧を表示 |


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

