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
| `use [name] | 使用するデータベースを変更 | 
| `show collections` | コレクション一覧を表示 |


