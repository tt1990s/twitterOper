#coding:utf-8

"""アクセストークン取得
"""

# ==== ライブラリ ====
import shutil
import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from requests_oauthlib import OAuth1Session
import webbrowser
import socketserver
import threading
import time

# ==== 定数 ====
# ポート番号
PORTNO = 8000

# コールバックURL
CALLBACKURL = "http://localhost:8000/"

# リクエストエンドポイントURL
REQENDPOINTURL = "https://api.twitter.com/oauth/request_token"

# 認証URL
AUTHURL = "https://api.twitter.com/oauth/authenticate"

# アクセスエンドポイントURL
ACCENDPOINTURL = "https://api.twitter.com/oauth/access_token"

# APIキー設定ファイルパス
APIKEYFP = "sett\\apiKey.json"

# アクセストークン設定ファイルパス
ACCTOKENFP = "sett\\accToken.json"

# index.htmlファイルパス
INDEXFP = "web\\index.html"

# ==== メソッド ====
def oper_browser():
    """Webブラウザ操作メソッド
    """

    # ブラウザで認証画面URLを開く
    webbrowser.open(authUrl)

# ==== クラス ====
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTPリクエストハンドラ
    """

    def do_GET(self):
        """Getリクエストが来た際の処理メソッド
        """

        try:

            # レスポンスヘッダ
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            # 遷移先ページ指定
            indexf = open(os.path.join(os.getcwd(), INDEXFP), 'rb')
            shutil.copyfileobj(indexf, self.wfile)
            indexf.close()

            # リクエストクエリをパース
            parsed_path = urlparse(self.path)
            query_dict = parse_qs(parsed_path.query)
            oauth_verifier = query_dict["oauth_verifier"][0]

            # 取得した認証文字列を用いてアクセストークンを取得
            sessionAcc = OAuth1Session(gl_api_key, gl_api_secret_key, gl_oauth_token, oauth_verifier)
            responseAcc = sessionAcc.post(ACCENDPOINTURL, params={"oauth_verifier": oauth_verifier})

            # 取得したアクセストークンをパース
            responseAccText = responseAcc.text
            accessTokenList = responseAccText.split("&")
            accTokenDict = {accessTokenStr.split("=")[0]: accessTokenStr.split("=")[1] for accessTokenStr in accessTokenList}
            print("")
            print("--------------------------")
            print("* Screen Name         :", accTokenDict["screen_name"])
            print("* User ID             :", accTokenDict["user_id"])
            print("* Access Token        :", accTokenDict["oauth_token"])
            print("* Access Token Secret :", accTokenDict["oauth_token_secret"])
            print("--------------------------")
            print("")

            # 辞書型配列 -> アクセストークン設定ファイル(JSON)
            accTokenF = open(ACCTOKENFP, mode="w")
            json.dump(accTokenDict, accTokenF, indent=2, ensure_ascii=False)
            accTokenF.close()

        except:
            pass

# ==== 処理 ====
if __name__ == "__main__":

    # 既存のアクセストークン設定ファイルを削除
    try:
        os.remove(ACCTOKENFP)
    except:
        pass

    # APIキーJSON読み込み -> 辞書型配列
    apiKeyJson = open(APIKEYFP, "r")
    apiKeyDic = json.load(apiKeyJson)

    # リクエストトークン取得
    sessionReq = OAuth1Session(apiKeyDic["apiKey"], apiKeyDic["apiSecretKey"])
    responseReq = sessionReq.post(REQENDPOINTURL, params={"oauth_callback": CALLBACKURL})

    # 取得したリクエストトークンをパース -> 辞書型配列
    responseReqText = responseReq.text
    oauthTokenList = responseReqText.split("&")
    oauthTokenDict = {oauthTokenStr.split("=")[0]: oauthTokenStr.split("=")[1] for oauthTokenStr in oauthTokenList}

    # 取得した情報をグローバル変数に格納
    gl_api_key = apiKeyDic["apiKey"]
    gl_api_secret_key = apiKeyDic["apiSecretKey"]
    gl_oauth_token = oauthTokenDict["oauth_token"]

    # 取得したリクエストトークンを用いて認証画面URL作成
    authUrl = AUTHURL + "?oauth_token=" + oauthTokenDict["oauth_token"]

    # Webブラウザ操作スレッド
    oper_browser_thread = threading.Thread(target=oper_browser)

    # ローカルWebサーバスレッド
    httpd = socketserver.TCPServer(("", PORTNO), MyHTTPRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)

    # ローカルWebサーバスレッドをデーモンスレッドにする
    # -> メインスレッドが終了すると、ローカルWebサーバスレッドも同時に停止される様になる
    server_thread.daemon = True

    # ローカルWebサーバスレッド開始
    server_thread.start()
    print("")
    print("===== Web server started =====")

    # 1秒待機
    time.sleep(1)

    # Webブラウザ操作スレッド開始
    oper_browser_thread.start()

    # アクセストークン設定ファイルが作成されていることを確認し、処理を終了
    while True:
        if os.path.isfile(ACCTOKENFP):
            time.sleep(2)
            print("* Access token set")
            break
        else:
            time.sleep(2)

    print("===== Web server stopped =====")