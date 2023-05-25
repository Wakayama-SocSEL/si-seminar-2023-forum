# NG-embedded Forum

## これは何？
- 対話型ゲームをする匿名掲示板です。プレイヤは一般的な匿名掲示板と同様に、自由な文章を発信することができます。
- ただし、プレイヤにはそれぞれNG行動が設定されています。NG行動をしたプレイヤは敗北となります。
- 他のプレイヤのNG行動を知ることはできますが、自分のNG行動が何かは分かりません。


## 動かすには？
1. Goole Cloud Shellでこのリポジトリを開きます。
[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/Wakayama-SocSEL/si-seminar-2023-forum.git)

2. コマンドを実行してサーバを起動します。（URLが出力されます）

```sh
python3 server.py
```

3. URLに移動します。


## 「NG行動」リスト
一部は実装途中です。（あなたの協力が必要です！　新しいアイデアも歓迎します）

- 30文字以上の文章
- 素数を含む文章（実装されていますが、動作が遅いです）
- 十二支の動物を含む文章（まだ実装されていません）


## 開発者の方へ
NG行動の実装のほか、HTML&CSSやJavaScriptの編集も歓迎します。

```sh
.
├── README.md # このファイル
├── judge.py # NG行動を判定するプログラム
├── server.py # サーバを起動するプログラム
└── page # Webページを構成するファイル群
     ├── index.html
     ├── main.js
     └── style.css
```
