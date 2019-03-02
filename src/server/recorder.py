# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16 
from kafka import KafkaProducer
from kafka.errors import KafkaError
import pickle
import threading
import numpy as np 
from datetime import datetime 
import time
import sys


class recoder:
  def __init__(self):
    self.samples = 2048      #pyaudio内置缓冲大小
    self.rate = 22000    #取样频率
    self.threshold = 1000         #声音保存的阈值
    self.COUNT_NUM = 20      #samples个取样之内出现COUNT_NUM个大于threshold的取样则记录声音
    self.save_length = 1         #声音记录的最小长度：save_length * NUM_SAMPLES 个取样
    self.time_count = 1     #录音时间，单位s
    self.sendingBuffer = []
    self.stop = False
    self.sour = ''
    self.dest = ''
    self.topic = 'todolist'

  def send(self):
    producer = KafkaProducer(bootstrap_servers=['140.112.41.94:9092'])
    time.sleep(1)
    while not self.stop:
      if len(self.sendingBuffer) > 0:
        tosend = self.sendingBuffer.pop(0)
        l = ['talker', self.sour, self.dest, 'speaker', (2,1,self.rate), np.array(tosend).tostring()]
        #l = [[np.array(self.Voice_String[self.nowBuffer]).tostring()],2,1,s$
        #print(type(np.array(self.Voice_String[self.nowBuffer]).tostring()))
        p = pickle.dumps(l)
        future = producer.send(self.topic, p)
        #print(']]')
        try:
          record_metadata = future.get(timeout=10)
        except KafkaError:
          # Decide what to do if produce request failed...
          log.exception()
          pass

  def recoder(self, sour, dest, topic):
    self.sour = sour
    self.dest = dest
    self.topic = topic
    sender = threading.Thread(target=self.send)
    sender.setDaemon(True)
    sender.start()
    pa = PyAudio() 
    stream = pa.open(format=paInt16, channels=1, rate=self.rate, input=True, 
            frames_per_buffer=self.samples) 
    save_count = 0 
    save_buffer = [] 
    time_count = self.time_count

    while not self.stop:
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            try:
              string_audio_data = stream.read(self.samples) 
            except:
              print('except:string_audio_data = stream.read(self.samples)')
              stream.close()
              stream = pa.open(format=paInt16, channels=1, 
                                rate=self.rate, input=True,
                                frames_per_buffer=self.samples)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于threshold的取样的个数
            large_sample_count = np.sum( audio_data > self.threshold )
            #print(np.max(audio_data), flush=True)
            # 如果个数大于COUNT_NUM，则至少保存save_length个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.save_length 
            else: 
                save_count -= 1

            if save_count < 0:
                save_count = 0 

            save_buffer.append( string_audio_data )
            #print('--------------',save_count, flush=True) 
            if time_count==0: 
                #if len(save_buffer)>0:
                    #self.Voice_String[self.nowBuffer] = save_buffer
                    self.sendingBuffer.append(save_buffer) 
                    save_buffer = []
                    #print("Recode a piece of  voice successfully!", flush=True)
                    
                    time_count = self.time_count
                    
                #else:
                #    return False
            sys.stdout.flush()
    sender.join()
if __name__ == "__main__":
    #thr1 = threading.Thread(target=send, name='ttt', args=())
    #thr1.start()
    r = recoder()
    r.recoder('johome','pi')
    sendover = True
    #thr1.join()
