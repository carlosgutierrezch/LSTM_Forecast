import os
import numpy as np  
import pandas as pd   
from pathlib import Path
import torch

class PredictionPipeline:
    def __init__(self):
        self.device= 'cpu:0' if torch.cuda.is_available() else 'cpu'
        self.model= torch.load(Path('artifacts/model_trainer/model.pt'))
        self.model= self.model.to(self.device)
        self.model.eval()
        
    def predict(self,data):
        data= data.to(self.device)
        with torch.no_grad():
            prediction= self.model(data)
            return prediction.cpu().numpy()