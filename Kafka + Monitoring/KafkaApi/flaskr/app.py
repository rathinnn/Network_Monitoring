from flask import Flask, render_template, request, url_for, redirect,jsonify
from KafkaProducer.kafkaLogger import sendToTopic
import logging
import sys

app = Flask(__name__)
ver = 1
updates = []
#logging.basicConfig(level=logging.DEBUG)
@app.route("/")
def home():

    return render_template(
        "index.html",
        title="Introduction to Networks Project Homepage",
        
    )
@app.route('/send',methods=['POST'])
def getData():
    content = request.json
    sendToTopic(content)
    #app.logger.info(content)
    #app.logger.info('Hi')
    #print(content)
    return jsonify({"Status":True})

@app.route('/update',methods = ['POST'])
def update():
    content = request.json
    #print(content['hostname'])
    updates.append(content['hostname'])
    #print(updates)
    return jsonify({"Status":True})

@app.route('/getupdate',methods = ['GET'])
def update2():

    return jsonify({"hostnames":updates})


#if __name__ == '__main__':
#    app.run(debug=True,port = 8000)

