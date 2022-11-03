#coding:utf-8

"""ツイート全消し
"""

# ==== ライブラリ ====
import tweepy
import json

# ==== 定数 ====
# APIキー設定ファイルパス
APIKEYFP = "sett\\apiKey.json"

# アクセストークン設定ファイルパス
ACCTOKENFP = "sett\\accToken.json"

# 削除件数
DELTWEETS = 3000

# ==== 処理 ====
if __name__ == "__main__":

    # APIキーJSON -> 辞書型配列
    apiKeyJson = open(APIKEYFP, "r")
    apiKeyDic = json.load(apiKeyJson)

    # アクセストークンJSON -> 辞書型配列
    accTokenJson = open(ACCTOKENFP, "r")
    accTokenDic = json.load(accTokenJson)

    # tweepy API設定
    auth = tweepy.OAuthHandler(apiKeyDic["apiKey"], apiKeyDic["apiSecretKey"])
    auth.set_access_token(accTokenDic["oauth_token"], accTokenDic["oauth_token_secret"])
    api = tweepy.API(auth)

    # ツイート削除
    for tweet in tweepy.Cursor(api.user_timeline).items(DELTWEETS):
        try:
            print("Deleting:", str(tweet.id))
            api.destroy_status(tweet.id)
        except:
            print("Could not delete:", str(tweet.id))
