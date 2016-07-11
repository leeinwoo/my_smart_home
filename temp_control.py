#!/usr/bin/env python
import socket, threading, time, subprocess, Adafruit_DHT

HOST = ''
PORT = 5000
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sensor = Adafruit_DHT.DHT22
pin = 18

temperature = 0
humidity = 0
AC_Flag=False
CONN_Flag=False
AUTO_Flag=False
conn=0


def read_temp():
    print("read_temp()")
    global humidity, temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}%C Humidity={1:0.1f}%'.format(temperature, humidity)
    else:
        print 'Failed to get reading. Try again!'
def init_socket():
    print("init_socket()")
    s.bind((HOST,PORT))
    s.listen(1)
    threading._start_new_thread(connect,())

def connect():
    print("connect()")
    global s, conn, CONN_Flag
    while 1:
        conn, addr=s.accept()
        CONN_Flag=True
        threading._start_new_thread(recv_msg,())
        print("connect success :", addr)
def send_msg():
    print("send_msg()")
    if CONN_Flag == True and humidity is not None and temperature is not None:            
        msg = str('{0:0.2f}'.format(temperature)) + "," + str('{0:0.2f}'.format(humidity))
        conn.send(msg.encode('utf-8'))
        print("send success :", msg)
        time.sleep(0.3)
        
def recv_msg():
    while 1:        
        data = conn.recv(1024)
        data.strip()
        print data
        if('request' in data):            
            send_msg()
        elif('ac' in data):
            print data
            ac_onoff()
        elif('auto' in data):
            print data           
            
def ac_onoff():
    global AC_Flag
    print "ac_onoff"
    if AC_Flag==False:
        subprocess.call(["irsend", "SEND_ONCE", "myRemote.conf", "KEY_1"])
        AC_Flag=True
    else:
        subprocess.call(["irsend", "SEND_ONCE", "myRemote.conf", "KEY_4"])
        AC_Flag=False

def automode_onoff():
    global AUTO_Flag
    if AUTO_Flag==False:
        AUTO_Flag=True
    elif AUTO_Flag==True:
        AUTO_Flag=False
        
    
init_socket()
while True:
    read_temp()
    if temperature is not None and temperature > 25.0 and AC_Flag == False:
        print("script start")        
    time.sleep(1)
