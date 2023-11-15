# 量子五目並べ

QuizKnockさんが紹介されていた量子五目並べを，粗雑なプログラムですが作ってみました．

元動画はこちら：[【理解不能】何色になるか分からない量子で五目並べやってみた【でも楽しそう】 - YouTube](https://www.youtube.com/watch?v=mitAxA3f4U4&t=17s&ab_channel=QuizKnock)

![Gameplay Example](https://raw.githubusercontent.com/shunya28/quantum-gomoku/master/sample/samlpe.png)

## 遊び方

- 現状，コンピュータ上のアプリケーションとしてのみ遊ぶことができます．
- 遊ぶためには「Python」というソフトウェアが必要です．このソフトのインストール方法は割愛します．以下，Windowsを前提とします．
  - 参考：[Windows 環境のPython: Python環境構築ガイド - python.jp](https://www.python.jp/install/windows/index.html)
  - Pythonのバージョンは 3.11.なんとか のものを選んでください．
- Pythonをインストールしたら，このページのやや右上辺りにある緑色の「Code」というボタンをクリックし，「Download ZIP」を押して，プログラムをダウンロードします．
- ダウンロードしたZIPファイルを解凍して，「run.py」があるところまでフォルダを開きます．
- フォルダの画面の上部にある，横長の「... > quantum-gomoku-master > ...」のように書かれているバーをクリックして，「cmd」と入力してEnterを押し，コマンドプロンプトと呼ばれる画面を開きます．
- 表示された黒い画面に「python run.py」と入力してEnterを押すと，量子五目並べの画面が表示されます．

## 操作説明

- Reset: 盤面をリセットします．手番は常に黒が最初です．
- Measure: 「観測」を行います．「観測」したい場合は，コマを置いた直後にこのボタンを押してください．
  - つまり，黒手番の人が「観測」を行いたい場合は，右上に「White's turn」と書かれているときにこのボタンを押します（分かりづらい実装ですみません）
- Restore: 「観測」後勝敗が付かなかった場合は，このボタンを押すことで観測前の盤面に戻ります．
- Remaining measurement: あと何回「観測」できるかが書かれています．
  - 両者が「観測」を使い切ってもなお勝敗が付かなかった場合，引き分けになるようにしています．
- Change stone: 置く石の種類を変えます．直前に強い石（黒手番なら90，白手番なら10の石）を置いていた場合は，種類の変更はできません（自動的に弱い石が選択されます）．
- Stone: 現在選択している石の種類を表します．石に書かれている数字は，「観測」したときに石が黒色になる確率を表しています．

---

# Quantum Gomoku

This is a game of Quantum Gomoku (Quantum Five in a Row / Quantum Omok) developed in Python 3.11.
AI and the web version has not been implemented yet.

- reference: [【理解不能】何色になるか分からない量子で五目並べやってみた【でも楽しそう】 - YouTube](https://www.youtube.com/watch?v=mitAxA3f4U4&t=17s&ab_channel=QuizKnock)
- how to play: run `python run.py`

<!--
# Five in a Row (Omok; Gomoku)

![Gameplay Example](https://raw.githubusercontent.com/StuartSul/Five_in_a_Row/master/sample/MainScreen.png)

## Overview
This is a game of five in a row (Korean: Omok; Japanese: Gomoku) developed in Python 3.8. It supports CLI & GUI, and an artificial intelligence module which can play against a player or against itself.

You can start playing with the following command:
```
python3 run.py
```

To play against another person, or make AI fight against itself, modify omok.py in omok folder.

## Web Version
JavaScript version of the game engine is available in the directory `web_release/` and it is live here (https://stuartsul.github.io/Five_in_a_Row/) without support for artificial intelligence.
-->
