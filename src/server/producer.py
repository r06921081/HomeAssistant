from kafka import KafkaProducer
from kafka.errors import KafkaError
import wav
import wave
import pickle
def nocall():
  producer = KafkaProducer(bootstrap_servers=['140.112.41.94:9092'])

  l = ['ss',11,10,11.11,['rr',1]]

  f = wave.open("fart.wav","rb")
  chunk = 1024
  databuffer = []
  data = f.readframes(chunk)
  print(data)
  exit()
  while data != b'':
    databuffer.append(data)
    data = f.readframes(chunk)

  send = [databuffer,f.getsampwidth(),f.getnchannels(),f.getframerate()]
  p = pickle.dumps(send)
  # Asynchronous by default
  future = producer.send('todolist', p)
  print(p)
  un = pickle.loads(p)
  print(un)
  try:
    record_metadata = future.get(timeout=10)
  except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

def response(prog, sour, dest, action, args, data):
  producer = KafkaProducer(bootstrap_servers=['140.112.41.94:9092'])

  send = [prog, sour, dest, action, args, data]
  p = pickle.dumps(send)
  # Asynchronous by default
  future = producer.send('todolist', p)
  try:
    record_metadata = future.get(timeout=10)
  except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass
    
if __name__ == '__main__':
  sendmsg('monitorhome', 'recv', None, (), None)

