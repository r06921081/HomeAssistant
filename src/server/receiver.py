from kafka import KafkaConsumer
from kafka.errors import KafkaError
#from query import *
#import wav
import pyaudio
import pickle
import threading


class receiver():
  def __init__(self):
    self.consumer = None#KafkaConsumer('remote',bootstrap_servers=['140.112.41.94:9092'])
    self.playBuffer = []
    self.fmt = 2
    self.channels = 1
    self.rate = 22000
    self.timeout = 15
    self.sour = ''
    self.dest = ''
    self.topic = 'todolist'

  def play(self, sour, dest, topic):
    self.sour = sour
    self.dest = dest
    self.topic = topic
    recvthr = threading.Thread(target=self.receive)
    recvthr.setDaemon(True)
    recvthr.start()
    
    p = pyaudio.PyAudio()
    #open stream  
    stream = p.open(format = p.get_format_from_width(self.fmt),  
                  channels = self.channels,  
                  rate = self.rate,  
                  output = True)  
    print('start')  
    lastdata = b''
  
    while self.timeout > 0:
      if len(self.playBuffer) > 1:
        toplay = self.playBuffer.pop(0)
        stream.write(toplay)  
        lastdata = toplay
      elif len(self.playBuffer) == 1:
        stream.write(self.playBuffer[0]) 
        self.timeout -= 1

    print('end')
    self.consumer.close()
    stream.stop_stream()  
    stream.close()  
    self.timeout = 0
    #close PyAudio  
    p.terminate()
    print('displayer close')
    return
    
  def receive(self):
    #playthr = threading.Thread(target=self.play)
    #playthr.setDaemon(True)
    #playthr.start()
    self.consumer = KafkaConsumer(self.topic, bootstrap_servers=['140.112.41.94:9092'])
    for message in self.consumer:
      #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,len(message.value)))
      try:
        unpkl = pickle.loads(message.value)
        #print(unpkl[:5])
        if unpkl[:4] == ['talker', self.sour, self.dest, 'speaker']:# and unpkl[1] ==  and unpkl[2] ==  and unpkl[3] == 'speaker':
          #print('-----------------')          
          self.playBuffer.append(unpkl[5])
        #break
      except Exception as e:
        print(e)
        
    #playthr.join()
    print('disconection')
if __name__ == '__main__':
  r = receiver()
  r.play('johome','pi')
  #for message in consumer:
  #  print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,len(message.value)))
  #  try:
  #    unpkl = pickle.loads(message.value)
  #    if unpkl[0] == 'talker' and unpkl[2] == 'pi' and unpkl[3] == 'speaker':
  #      playBuffer.append(unpkl[5])

  #  except Exception as e:
  #    print(e)
  #    exit()
  #playthr.join()
    #print(unpkl)
  #if str(message.value, encoding='utf-8') == 'searchPeople':
  #  searchPeople()
  
