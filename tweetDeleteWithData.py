#coding:utf-8

"""ツイート全消し(ツイートデータ使用)
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

# ツイートデータファイルパス
TWEETDATAFP = "data\\tweets.js"

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

    # ツイートデータファイル読み込み
    tweetf = open(TWEETDATAFP, 'r',encoding="utf-8")
    tweetdatastr = tweetf.read()

    # 空白削除
    tweetdatastr = tweetdatastr.replace(" ", "")

    # 改行削除
    tweetdatastr = tweetdatastr.replace("\r", "")
    tweetdatastr = tweetdatastr.replace("\n", "")

    # 以下の形式の文字列を抜き出す
    # {"tweet":{"edit_info":{"initial":{"editTweetIds":["「ツイートID」"]
    tarstrre = r"\{\"tweet\":\{\"edit_info\":\{\"initial\":\{\"editTweetIds\":\[\"\d{3,}\"\]"
    targetstrlist = re.findall(tarstrre, tweetdatastr)

    # 抜き出した文字列からツイートIDだけを抜き出す
    exclstr = "{\"tweet\":{\"edit_info\":{\"initial\":{\"editTweetIds\":[\""
    targetstrlist = [targetstr.replace(exclstr, "") for targetstr in targetstrlist]
    exclstr = "\"]"
    targetstrlist = [targetstr.replace(exclstr, "") for targetstr in targetstrlist]

    # ツイートIDを数値にする
    targetintlist = [int(targetstr) for targetstr in targetstrlist]

    # ツイート削除
    for targetint in targetintlist:
        try:
            print("Deleting:", str(targetint))
            tweepyapi.destroy_status(targetint)
        except:
            print("Could not delete:", str(targetint))