#!/usr/bin/env python
# codeing=utf-8 
#-----------------------------------------------------------------
# WiFi logger
#	This script gather MAC address of Access points & Stations.
# 	Ver 1.0 	2018/04/12	T.WATAHIKI
#-----------------------------------------------------------------
from subprocess import check_output
from collections import deque
from datetime import datetime as dt
import os
import commands
import redis
import time
from scapy.all import *

#-----------------------------------------------------------------
# GPS data DB
#-----------------------------------------------------------------
gpsinfo = redis.StrictRedis(
	host='127.0.0.1',
	port=6379,
	db=0
)

#-----------------------------------------------------------------
# logger for AP & ST
#-----------------------------------------------------------------
def	wlogger(mode, bssid, ssid, pkt, gps_d) :
	extra = pkt.notdecoded
	rssi = -(256-ord(extra[-4:-3]))

	# Station infomation
	if mode == 1:
		tstr = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
		pstr = "%s,<=>%s,%s,,,%s,%s,%s,%s,%s" %(bssid, ssid, rssi, gps_d[0], gps_d[1],gps_d[2], gps_d[3], tstr)
		fst.write(pstr + "\n")
		fst.flush()
#		print pstr

	# AccessPoint infomation
	elif mode == 3:
		crypto = set()
		#
		# Get crypto type
		ssid, channel = None, None
		p = pkt[Dot11Elt]
		while isinstance(p, Dot11Elt):
			if p.ID == 0:
				ssid = p.info
			elif p.ID == 3:
				channel = ord(p.info)
			elif p.ID == 48:
				crypto.add("WPA2")
			elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\0x1\x00'):
				crypto.add("WPA")
			p = p.payload
		if not crypto:
			cap = (str(pkt.cap)).split('+')
			if 'privacy' in cap:
				crypto.add("WEP")
			else:
				crypto.add("OPN")
		tstr = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
		pstr = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(bssid, ssid, rssi, channel, '/'.join(crypto), gps_d[0], gps_d[1],gps_d[2], gps_d[3], tstr)
		fap.write(pstr + "\n")
		fap.flush()
#		print pstr


#-----------------------------------------------------------------
# Handler for packet
#-----------------------------------------------------------------
def PacketHandler (pkt) :
	hwaddr = get_if_hwaddr('wlan0')
	gps = gpsinfo.get('gps')
	gps_s = gps.split(',')
	pstr = ""
	if pkt.haslayer(Dot11):
		#
		# Authentication
		if pkt.type == 1 and pkt.subtype == 11 :
			if q.count(pkt.addr1.upper()) == 0:
				wlogger(1, pkt.addr1.upper(), pkt.addr2.upper(), pkt, gps_s)
		#
		# Probe request
		if pkt.type == 0 and pkt.subtype == 4 and hwaddr != pkt.addr2 :
			wlogger(1, pkt.addr2.upper(), 'X', pkt, gps_s)
		#
		# Beacon
		if pkt.type == 0 and pkt.subtype == 8 :
			q.append(pkt.addr3.upper())
			if len(q) > 10:
				q.popleft()
			wlogger(3, pkt.addr3.upper(), pkt.addr2.upper(), pkt, gps_s)
 
#-----------------------------------------------------------------
# main
#-----------------------------------------------------------------
q = deque()
try:
	i = 0
	fname_ap = '/mnt/usb/CSV/ap_' + dt.now().strftime("%Y%m%d%H%M%S") + '.csv'
	fname_st = '/mnt/usb/CSV/st_' + dt.now().strftime("%Y%m%d%H%M%S") + '.csv'
	fap = open( fname_ap, 'a' )
	fst = open( fname_st, 'a' )

	while 1:

		time.sleep(0.1)
                sniff(iface="mon0", prn=PacketHandler, count=5, timeout=1, store=0)

		
except KeyboardInterrupt :
	print("keyboardinterrupt\n") 
	raise

except Exception as e:
	print "type " + str(type(e))
	print "message " + e.message
	print "e " + str(e)
	pass
finally:
	fst.close()
	fap.close()
	time.sleep(3.0)
	print "shutdown start!"
#	os.system("sudo shutdown -h now")

