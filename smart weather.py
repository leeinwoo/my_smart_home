# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from gtts import gTTS
from urllib2 import urlopen
from pygame import mixer
import time

def get_current_weather(city):
  if(len(weatherInfo)>0):
    weatherInfo.clear()
  page = urlopen('http://www.kma.go.kr/weather/observation/currentweather.jsp')
  text = str(page.read().decode("euckr").encode("utf8"))  
  text = text[text.find(">"+city):]  
  for i in range(12):
    text = text[text.find("<td>")+1:]
    start = 3
    end = text.find("</td>")
    weatherInfo.append(text[start:end])
    print(text[start:end])
  return

def set_gTTS(weather):  
  if("맑" in weather):
    sound = ("현재 날씨는 {0}입니다. ".format(weather))
  elif("비" in weather):
    sound = ("현재 날씨는 {0}입니다. 외출 시 우산 챙겨가세요. ".format(weather))
  elif("눈" in weather):
    sound = ("현재 날씨는 {0}입니다. 미끄럼 조심하세요.".format(weather))
  else:
    sound = ("Failed get weather!")
  tts = gTTS(text=sound, lang='ko')
  tts.save("weather.mp3")

def play_sound():
  mixer.init()
  mixer.music.load('weather.mp3')
  mixer.music.play()
  time.sleep(5)

def set_led(weather):
  if("맑" in weather):
    GPIO.output(24, False)
    GPIO.output(23, True)
  elif("비" in weather or "눈" in weather):
    GPIO.output(23, False)
    GPIO.output(24, True)
  else:
    GPIO.output(23, False)
    GPIO.output(24, False)

def get_localtime():
  t = time.localtime()
  return t
    
    
weatherInfo = []

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

locate="부산"
alarm_h=7
alarm_m=0

while 1:
  t = get_localtime()
  
  if t.tm_hour==alarm_h and t.tm_min==alarm_m:
    get_current_weather(locate)
    set_gTTS(weatherInfo[0])
    set_led(weatherInfo[0])
    play_sound()
    time.sleep(60)
      
  if t.tm_min == 0:
    get_current_weather(locate)
    set_led(weatherInfo[0])    
    time.sleep(60)
    
