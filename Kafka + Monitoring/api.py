from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask import Blueprint
from KafkaProducer.kafkaLogger import sendToTopic

api = Blueprint('api', __name__)
ver = 1
updates = []
servers = [{'id':1, 'coor':[17.38,78.48], 'hostname': ' '},
{'id':2, 'coor':[17.1,79.48], 'hostname': ' '}, {'id':3, 'coor':[16.38,78.48], 'hostname': ' '},
{'id':4, 'coor':[17.38,79.48], 'hostname': ' '}] 

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

@api.route('/updatesAvailable',methods = ['GET'])
def update2():
    return jsonify({"hostnames":updates})

@api.route('/servers',methods = ['GET'])
def getServers():
    return jsonify(servers)


