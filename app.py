from flask import Flask, render_template, request

import os
import numpy as np  
import pandas as pd   
from pathlib import Path
# import torch
from TimeSeriesForecast.pipeline.predictionpipeline import PredictionPipeline


app= Flask(__name__)

@app.route('/',methods=['GET'])
def HomePage():
    return render_template('index.html')
@app.route('/train',methods=['GET'])
def training():
    os.system('python main.py')
    return 'Training succesfull'
@app.route('/predict',methods=['GET','POST'])
def index():
    try: 
        days= request.form['predictions']
        
if __name__=='__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
    
