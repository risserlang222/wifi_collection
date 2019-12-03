#!Python3
# coding=utf-8
#Windowsにおいて、cmdでコマンドを実行して、接続中のBSSID（MAC）アドレスなどを取得するプログラム
import subprocess
import sqlite3

# netsh wlan show interface

db_path = r'C:\Users\PC-Admin\Documents\ラズパイ\wifi.db'
db_connection = sqlite3.connect(db_path)
db_cursor = db_connection.cursor()
cmd1 = 'chcp 65001'
#cmd2では、接続中のwifiアクセスポイントのみ取得可能
cmd2 = 'netsh wlan show interface'
#cmd3では、電波が届く範囲の全てのwifiアクセスポイントを取得
cmd3 = 'netsh wlan show networks mode=bssid'
#cmd4では、cmd3のうち"BSSID"の行だけを抽出
cmd4 = 'netsh wlan show networks mode=bssid | find "BSSID"'

#runcode = subprocess.call(cmd, shell= True)
#TODO: cmd4の結果のうち、BSSIDの行だけを変数に格納して、DBにinsertしたい。

#runcode1 = subprocess.call(cmd1, shell=True)

#runcode2 = subprocess.call(cmd2, shell=True)

#runcode3 = subprocess.call(cmd3, shell=True)

#runcode4 = subprocess.call(cmd4, shell=True)
output = str(subprocess.check_output(cmd4, shell=True))
output_strip = output.strip()
#output_kaigyou = output.split(sep="\\n")
#output_kaigyou = [output.strip() for x in output.split(sep="\\n")]

print(output_kaigyou)