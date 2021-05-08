from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def sendToTopic(app_json):
    producer.send('test2' , app_json)
    