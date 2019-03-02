from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
#import wav
import pickle
import threading
import time
import sys
#import test_cloudspeech_openyoutube
class sender():
  def __init__(self, prog, user, dest, action, args, data, topic):
    self.prog = prog
    self.user = user
    self.dest = dest
    self.action = action
    self.args = args
    self.data = data
    self.topic = topic
    self.msg = []
  def getmsg(self):
    consumer = KafkaConsumer(self.topic ,bootstrap_servers=['140.112.41.94:9092'])
    print('s')
    for m in consumer:
      unpkl = pickle.loads(m.value)
      #print(unpkl)
      print(self.user)
      if unpkl[2] == self.user and unpkl[3] == 'response':
        self.msg.append(m)
        return
    print('e')
    
  def sendmsg(self):
    #consumer = KafkaConsumer('todolist',bootstrap_servers=['140.112.41.94:9092'])
    #print(msg)
    listenthreading = threading.Thread(target=self.getmsg)
    listenthreading.setDaemon(True)
    listenthreading.start()
    time.sleep(1)
    producer = KafkaProducer(bootstrap_servers=['140.112.41.94:9092'])
  
    send = [self.prog, self.user, self.dest, self.action, self.args, self.data, self.topic]
    p = pickle.dumps(send)
    # Asynchronous by default
    future = producer.send(self.topic, p)

    try:
      record_metadata = future.get(timeout=10)
    except KafkaError:
      # Decide what to do if produce request failed...
      log.exception()
      pass
    time.sleep(1)
    print('getting')
    waiting = 0
    while len(self.msg) == 0:
      time.sleep(1)
      waiting += 1
      #print(msg)
      if waiting > 10:
        return [self.prog, self.dest, self.user, 'error', self.args, {}, self.topic]
    for m in self.msg:
      try:
        unpkl = pickle.loads(m.value)
        #wav.play(unpkl[0],unpkl[1],unpkl[2],unpkl[3])
        print(unpkl)
        #    th.join()
      except Exception as e:
        print(e)
    #listenthreading.join()
    print('response waiting timeout')
    return unpkl
    #getResponse.getmsg()
if __name__ == '__main__':
  sender(sys.argv[1], 'pi', 'home', sys.argv[2], (), None, 'todolist').sendmsg()
  #sendmsg('monitorhome', 'pi', 'recv', 'request', (), None)
