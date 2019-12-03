#!Python3
# coding=utf-8
#Windowsにおいて、cmdでコマンドを実行して、接続中のBSSID（MAC）アドレスなどを取得するプログラム
import subprocess


# netsh wlan show interface

cmd1 = 'chcp 65001'

cmd2 = 'netsh wlan show interface'

#runcode = subprocess.call(cmd, shell= True)

runcode1 = subprocess.call(cmd1, shell= True)

runcode2 = subprocess.call(cmd2, shell= True)
