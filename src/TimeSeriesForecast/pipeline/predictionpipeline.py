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

    # def predict(self,num_days:5):

    #     predictions= []
        
    #     for _ in range(num_days):
    #         data= torch.tensor(last_know_data).float().to(self.device).unsqueeze(0)
            
    #         with torch.no_grad():
    #             prediction= self.model(data)
    #             predictions.append(prediction)
    #     return predictions

    
