#coding:utf-8

"""アンファボ
"""

# ==== ライブラリ ====
import tweepy
import json

import datetime

# ==== 定数 ====
# APIキー設定ファイルパス
APIKEYFP = "sett\\apiKey.json"

# アクセストークン設定ファイルパス
ACCTOKENFP = "sett\\accToken.json"

# 削除件数
DELTWEETS = 100

# ==== 処理 ====
if __name__ == "__main__":

    print("start: ", datetime.datetime.now())

    # APIキーJSON -> 辞書型配列
    apiKeyJson = open(APIKEYFP, "r")
    apiKeyDic = json.load(apiKeyJson)

    # アクセストークンJSON -> 辞書型配列
    accTokenJson = open(ACCTOKENFP, "r")
    accTokenDic = json.load(accTokenJson)

    # tweepy API設定
    auth = tweepy.OAuthHandler(apiKeyDic["apiKey"], apiKeyDic["apiSecretKey"])
    auth.set_access_token(accTokenDic["oauth_token"], accTokenDic["oauth_token_secret"])
    tweepyapi = tweepy.API(auth)

    # ツイート削除
    for tweet in tweepyapi.get_favorites(count=DELTWEETS):
        try:
            print("Deleting:", str(tweet.id))
            tweepyapi.destroy_favorite(tweet.id)
        except:
            print("Could not delete:", str(tweet.id))

    print("End: ", datetime.datetime.now())