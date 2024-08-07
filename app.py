from flask import Flask, render_template, request

import os
import numpy as np  
import pandas as pd   
from pathlib import Path
import torch
from TimeSeriesForecast.pipeline.predictionpipeline import PredictionPipeline


app= Flask(__name__)

@app.route('/',methods=['GET'])
def HomePage():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)