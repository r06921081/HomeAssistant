from kafka import KafkaProducer
from kafka.errors import KafkaError
import wav
import wave
import pickle
producer = KafkaProducer(bootstrap_servers=['140.112.41.94:9092'])

l = ['ss',11,10,11.11,['rr',1]]

send = ['monitorhome', 'jo', None, (), 'hello']
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
