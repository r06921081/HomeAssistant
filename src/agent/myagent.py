#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import webbrowser
from gtts import gTTS
import tempfile
from pygame import mixer
import time
import voiceKit.receiver as recv
import voiceKit.recorder as recorder
import voiceKit.producer as msgsend
from multiprocessing import Process
from threading import Thread
from translate import trans
from assistant_library import main as ga
import voiceKit.uploadAndSendEmail as uploadAndSendEmail
id = 'pi'
serverid = 'home'
forceStop = False
status_ui = aiy.voicehat.get_status_ui()

def say(text, extrawating = 0):
  if len(text) == 0:
    return
  with tempfile.NamedTemporaryFile(delete=True) as fp:
    tts = gTTS(text=text, lang='zh-TW')
    tts.save("{}.mp3".format(fp.name))
    mixer.init()
    mixer.music.load('{}.mp3'.format(fp.name))
    mixer.music.play()
  time.sleep(len(text)*0.25+extrawating)
def on_button_press():
  print('button_press')
  global forceStop
  forceStop = True
  say('您按按鈕阿？')

def talker(serverid, id, talkto, listento):
  global forceStop
  rcdr = recorder.recoder()
  rcdrthr = Process(target=rcdr.recoder, args=(serverid,id,talkto),daemon=True)
  #rcdrthr.setDaemon(True)
  rcdrthr.start()
  receiver = recv.receiver()
  recvthr = Process(target=receiver.play, args=(serverid,id, listento),daemon=True)
  #recvthr.setDaemon(True)
  recvthr.start()
  #receiver.play('recv',id)
  recognizer = aiy.cloudspeech.get_recognizer()
  text = ''
  while text != '掛斷' and not forceStop:
    if not recvthr.is_alive():
      forceStop = True
    text = recognizer.recognize()
    print(text,forceStop)
  rcdrthr.terminate()
  recvthr.terminate()
  rcdrthr.join()
  recvthr.join()
  say('掛惹')

def callsubprog(progCmd):
  global forceStop
  global serverid
  global id
  global status_ui
  forceStop = False
  recognizer = aiy.cloudspeech.get_recognizer()
  if progCmd in ['冰箱有什麼','冰箱裡有什麼']:
    result = msgsend.sender('icebox', id, serverid, 'request', (), None, 'todolist').sendmsg()
    itemtext = ''
    for key, value in result[5].items():
      itemtext += str(value) + ' ' + str(key) + ','
    chitems = trans(itemtext)
    if chitems != '':
      say('冰箱裡有'+chitems)
    elif result[3] == 'error':
      say('遠端沒有回應')
    else:
      say('冰箱裡好像沒東西喔')  
    print(result)
  elif progCmd in ['有人在家嗎', '家裡有人嗎']:
    result = msgsend.sender('monitorhome', id, serverid, 'request', (), None, 'todolist').sendmsg()
    if result[5].get('person') != None:
      recognizer = aiy.cloudspeech.get_recognizer()
      say('家裡有' + str(result[5]['person'])+'個人, 要開啟對話嗎？')
      print('Listening...')      
      text = recognizer.recognize()
      while text is None:
        text = recognizer.recognize()
      print(text)
      if text not in ['不是','不好','不要','不用']:
        print('connecting')
        response = msgsend.sender('talker', id, serverid, 'request', (), None, 'todolist').sendmsg()
        if response[5] == 'connected':
          talker(serverid, id, id, serverid)
    elif result[3] == 'error':
      say('遠端沒有回應')
    else:
      say('我沒看到家裡有人喔')
  elif progCmd in ['打回家','大回家','帶回家','回家']:
    response = msgsend.sender('talker', id, serverid, 'request', (), None, 'todolist').sendmsg()
    if response[5] == 'connected':
      talker(serverid, id, id, serverid)
    elif response[3] == 'error':
      say('遠端沒有回應')
  elif progCmd.lower() in ['google', 'google小姐']:
    say('那接下來就交給google小姐了')
    recognizer = aiy.cloudspeech.get_recognizer()
    status_ui.status('ready')
    gathr = Thread(target=ga,args=(status_ui,))
    gathr.setDaemon(True)
    gathr.start()
    text = ''
    while text != '結束' and not forceStop:
      text = recognizer.recognize()
      time.sleep(1)
      print(text,forceStop)
    say('小助理回來了，想我嗎？')
    return
  elif progCmd in ['email']:
    say('想寄給誰呢?')
    text = None
    while text is None:
      text = recognizer.recognize()
    emaillist = {'自己':'windwaker1121@hotmail.com'}
    print(emaillist.items())
    if emaillist.get(text) == None:
      say(text+'不在通訊錄內')
    else:
      say('想對他說什麼呢?')
      content = None
      while content is None:
        content = recognizer.recognize()
      say('信件內容為:'+ content +'要寄出嗎?')
      text = None
      while text is None:
        text = recognizer.recognize()
      if text not in ['不是','不好','不要','不用']:
        send = uploadAndSendEmail.sendPic()
        send.uploadAndSendEmail(["clothg34569@gmail.com","windwaker1121@hotmail.com"], './README.md', content)
        say('已將信件送出')
      else:
        say('已取消')
  else:
    say('ba歉，我還不會'+progCmd)
  
def main():
    global status_ui
    sleep = False
    helplist = [['需要幫忙嗎?',0],['抱歉,可以再說一次嗎？',3],['我沒聽清楚，可以再說一次嗎？',3],['還有什麼需要嗎？',2]]
    mutelist = [['',0]]
    listpointer = 0
    
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()

    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    while True:
      button.on_press(on_button_press)
      print('Press the button and speak')
      say(helplist[listpointer][0])
      print('Listening...')
      if not sleep:
        status_ui.status('listening')
      text = recognizer.recognize()
      status_ui.status('thinking')
      if text is None:
        print('Sorry, I did not hear you.')
        listpointer = (listpointer+1)%len(helplist)
      elif text.lower() in ['google','小助理','小助手'] and sleep:
        tmp = helplist.copy()
        helplist = mutelist.copy()
        mutelist = tmp.copy()
        listpointer = 0
        say('好的,我醒了')
        time.sleep(1)
        sleep = False
      elif not sleep:
        if text in ['不用了','不用']:
          tmp = helplist.copy()
          helplist = mutelist.copy()
          mutelist = tmp.copy()
          listpointer = 0
          say('好的小助手睡覺惹,嘻嘻')
          status_ui.status('thinking')
          #time.sleep(5)
          sleep = True
        elif text in ['吵死了','不要吵']:
          tmp = helplist.copy()
          helplist = mutelist.copy()
          mutelist = tmp.copy()
          listpointer = 0
          say('嗚嗚嗚，好啦，不鬧')
          status_ui.status('thinking')
          #time.sleep(5)
          sleep = True
        else:
          say('好', extrawating=0.2)
          print(text)
          callsubprog(text)
          listpointer = -1
if __name__ == '__main__':    
    main()
