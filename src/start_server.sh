#!bin/basH
cd kafka_2.12-0.11.0.2/
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
