from flask import Flask
from flask import request
from flask import json

import os
import json
import sys


import src.MLapp.DataIO as DataIO
import src.MLapp.AnalyzeData as AnalyzeData

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/initModel')
def initModel():
    DataIO.appendStrData("", "importTmpAllData", None)
    AnalyzeData.initialClusteringAndBuildCLF()
    label = AnalyzeData.predict()
    return "init successfully"

@app.route('/retriveAllData')
def retriveAllData():
    sData = DataIO.getAllOriginalData()
    return sData

@app.route('/commitData', methods = ['POST'])
def commitData():
    if request.headers['Content-Type'] == 'application/json':
        sList = DataIO.getStrFromJSON(request.json)
        return AnalyzeData.commitData(sList)

    else:
        return "415 Unsupported Media Type ;)"

@app.route('/messages', methods = ['POST'])
def messages():
    if request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    else:
        return "415 Unsupported Media Type ;)"



if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'src' + os.sep + 'MLapp')
    app.run()
