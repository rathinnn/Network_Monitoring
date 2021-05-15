from kafka import KafkaProducer
import numpy as np
import time
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def sendToTopic(app_json):
    producer.send('test2' , app_json)

ids = [1,2,3,4]
stat = ['ALLOWED' , 'BLOCKED']
method = ['GET','POST','CONNECT']
url = ['www.google.com','www.youtube.com','www.linuxmint.com', 'aums.amrita.edu' , 'firefox.com']


try:
    i = 0
    while True:
        save = int(np.random.choice(ids,1)[0])
        jsons = {
           'server_id' : save,
           'status' : str(np.random.choice(stat,1)[0]),
           'method' : str(np.random.choice(method,1)[0]),
           'url' : str(np.random.choice(url,1)[0])
           #'Lat' : coormap[save][0]
           #'Lon' : coormap[save][1]
       }

        i+=1
        
        sendToTopic(jsons)

        if(i%5 == 0):
            h = 0
            #time.sleep(1)
       
except KeyboardInterrupt:

    print("Press Ctrl-C to terminate while statement")

    pass