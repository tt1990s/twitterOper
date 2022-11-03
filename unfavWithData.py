#coding:utf-8

"""アンファボ(ツイートデータ使用)
"""

# ==== ライブラリ ====
import tweepy
import json
import re

# ==== 定数 ====
# APIキー設定ファイルパス
APIKEYFP = "sett\\apiKey.json"

# アクセストークン設定ファイルパス
ACCTOKENFP = "sett\\accToken.json"

# ファボデータファイルパス
LIKEDATAFP = "data\\like.js"

# ==== 処理 ====
if __name__ == "__main__":

    # APIキーJSON -> 辞書型配列
    apiKeyJson = open(APIKEYFP, "r")
    apiKeyDic = json.load(apiKeyJson)

    # アクセストークンJSON -> 辞書型配列
    accTokenJson = open(ACCTOKENFP, "r")
    accTokenDic = json.load(accTokenJson)

    # tweepy API設定
    tweepyauth = tweepy.OAuthHandler(apiKeyDic["apiKey"], apiKeyDic["apiSecretKey"])
    tweepyauth.set_access_token(accTokenDic["oauth_token"], accTokenDic["oauth_token_secret"])
    tweepyapi = tweepy.API(tweepyauth)

    # ファボデータファイル読み込み
    likef = open(LIKEDATAFP, 'r',encoding="utf-8")
    likedatastr = likef.read()

    # 空白削除
    likedatastr = likedatastr.replace(" ", "")

    # 改行削除
    likedatastr = likedatastr.replace("\r", "")
    likedatastr = likedatastr.replace("\n", "")

    # 以下の形式の文字列を抜き出す
    # {"like":{"tweetId":"「ツイートID」",
    tarstrre = r"\{\"like\":\{\"tweetId\":\"\d{3,}\","
    targetstrlist = re.findall(tarstrre, likedatastr)

    # 抜き出した文字列からツイートIDだけを抜き出す
    exclstr = "{\"like\":{\"tweetId\":\""
    targetstrlist = [targetstr.replace(exclstr, "") for targetstr in targetstrlist]
    exclstr = "\","
    targetstrlist = [targetstr.replace(exclstr, "") for targetstr in targetstrlist]

    # ツイートIDを数値にする
    targetintlist = [int(targetstr) for targetstr in targetstrlist]

    # ツイート削除
    for targetint in targetintlist:
        try:
            print("Deleting:", str(targetint))
            tweepyapi.destroy_favorite(targetint)
        except:
            print("Could not delete:", str(targetint))