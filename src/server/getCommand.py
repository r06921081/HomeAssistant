from kafka import KafkaConsumer
from kafka.errors import KafkaError
#from query import *
import time
import pyaudio
import pickle
import threading
import darknet
import sys
import producer
import recorder
import receiver as recv
from multiprocessing import Process, Manager, Queue
consumer = KafkaConsumer('todolist',bootstrap_servers=['140.112.41.94:9092'])
nowBuffer = 0
playBuffer = []
#user = sys.argv[1]

threads = []

#progdict = {}
def getthread(prog, sour, dest, action, args, data):
  global progdict
  thr = threading.Thread(target=progdict[prog],args=(prog, sour, dest, action, args, data))
  return thr

threads = []
if __name__ == '__main__':
  global user
  user = sys.argv[1]
  global progdict
  import services
  progdict = services.getProgram(user)
  #user
  for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,len(message.value)))
    try:
      unpkl = pickle.loads(message.value)
      #wav.play(unpkl[0],unpkl[1],unpkl[2],unpkl[3])
      prog = unpkl[0]
      sour = unpkl[1]
      dest = unpkl[2]

      action = unpkl[3]
      if action == 'update_services' and prog == 'main':
        import services2
        d = services2.getter(user)
        progdict = d.getProgram()#{}
        print(progdict)
        print('service update')
        continue
      if dest != user or action != 'request':
        continue
      args = unpkl[4]
      data = [unpkl[5]]
      print(prog, sour, dest, action, args, len(data))
      if progdict.get(prog) == None:
        print('call for service error: no such service')
        continue
      progthr = getthread(prog, sour, dest, action, args, data)
      progthr.start()
      threads.append(progthr)
    except Exception as e:
      print(e)

      #exit()
    for t in threads:
      print(t,'------------------------------')
      if not t.is_alive():
        print(t,'+')
        
        threads.pop(threads.index(t)).join()
        
  #progthr.join()
    #print(unpkl)
  #if str(message.value, encoding='utf-8') == 'searchPeople':
  #  searchPeople()
  
