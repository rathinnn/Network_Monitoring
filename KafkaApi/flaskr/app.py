from flask import Flask, render_template, request, url_for, redirect,jsonify
from KafkaProducer.kafkaLogger import sendToTopic
import logging
import sys

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send',methods=['POST'])
def getData():
    content = request.json
    sendToTopic(content)
    #app.logger.info(content)
    #app.logger.info('Hi')
    print(content)
    return jsonify({"Status":True})

if __name__ == '__main__':
    app.run(debug=True)