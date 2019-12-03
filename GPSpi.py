# coding=utf-8
import serial
import os
import redis
import time
import datetime

firstFixFlag = False
# will go true at first fix
firstFixDate = ""

# Set up serial:
ser = serial.Serial( port='/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,  timeout=1)


def lat_degree_convert(p_time):
  val = float(p_time[:2]) + float(p_time[2:])/60
  return val


def lon_degree_convert(p_time):
  val = float(p_time[:3]) + float(p_time[3:])/60
  return val

#-----------------------------------------------------------------
# main
#-----------------------------------------------------------------
gpsinfo = redis.StrictRedis(
	host='127.0.0.1',
	port=6379,
	db=0
)

while 1:
  try:
    time.sleep(0.25)
    print(time.ctime())
    line = ser.readline()
    items = line.split(',')

    if items[0] == "$GPRMC":
#      print "gps line",line
      print("gps line" + line)
      if items[2] == 'A':
#        print  items[2],",", lat_degree_convert(items[3]),",", lon_degree_convert(items[5])
        gpsinfo.set('gps', items[2],",", lat_degree_convert(items[3]),",", lon_degree_convert(items[5]),",",datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print gpsinfo
      else:
        print  items[2],',-,-'
        gpsinfo.set('gps',  items[2],',-,-,' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        print gpsinfo
      break
  except:
    print  '=V,-,-'
    gpsinfo.set('gps',  'V,-,-,' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print 'redis=',gpsinfo.get('gps')
    pass

ser.close()

