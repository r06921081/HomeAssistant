from kafka import KafkaConsumer
from kafka.errors import KafkaError
import pickle
def getmsg(msg):
  consumer = KafkaConsumer('todolist',bootstrap_servers=['140.112.41.94:9092'])
  print(msg)
  for message in consumer:
    msg.append(message.value)
    #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,len(message.value)))
