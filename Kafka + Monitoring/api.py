from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask import Blueprint
from KafkaProducer.kafkaLogger import sendToTopic

api = Blueprint('api', __name__)
ver = 1
updates = []

@api.route('/send',methods=['POST'])
def getData():
    content = request.json
    sendToTopic(content)
    return jsonify({"Status":True})

@api.route('/update',methods = ['POST'])
def update():
    content = request.json
    updates.append(content['hostname'])
    return jsonify({"Status":True})

@api.route('/getupdate',methods = ['GET'])
def update2():
    return jsonify({"hostnames":updates})


