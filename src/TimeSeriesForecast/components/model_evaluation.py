import pandas as pd
import numpy as np
import torch
from notebooks.src.functions_torch import eval_metrics
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast.constants import *
from TimeSeriesForecast import logger
from torch.utils.data import DataLoader
from notebooks.src.functions_torch import TimeSeries
import mlflow
from TimeSeriesForecast.entity.config_entity import ModelEvaluationConfig
import mlflow.sklearn
import dagshub
dagshub.init(repo_owner='carlosgutierrezch', repo_name='ml-flow', mlflow=True)



class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config= config
        self.tensor=None
        self.X_test= None
        self.y_test=None
    def tensor_loader(self):
        try:
            self.tensor= torch.load(self.config.test_data_path)
            self.X_test,self.y_test= self.tensor['X_test'],self.tensor['y_test']
            self.test_dataset= TimeSeries(self.X_test,self.y_test)
            self.test_loader= DataLoader(self.test_dataset,batch_size=self.config.batch_size,shuffle=False)
            return self
        except Exception as e:
            raise e
    def model_loader(self):
        try:
            device= 'cuda:0' if torch.cuda.is_available() else 'cpu'
            model= torch.load(self.config.model_path)
            model.to(device)
            test_data= self.test_loader
            num_epochs= self.config.num_epochs
            with mlflow.start_run():
                model.eval()

                for epoch in range(num_epochs):
                    
                    for _,batch in enumerate(test_data):
                        x_batch,y_batch=batch[0].to(device),batch[1].to(device)
                        with torch.no_grad():
                            predicted = model(x_batch).to('cpu').numpy()
                            y_batch= y_batch.to('cpu').numpy()
                            (rmse,mae,r2)= eval_metrics(predicted,y_batch)
                        
                print(f'epoch: {epoch+1}/{num_epochs},rmse :{rmse}, mae: {mae},r2: {r2}') 
                                       
                mlflow.log_params(self.config.all_params)
                mlflow.log_metric('rmse', rmse)
                mlflow.log_metric('mae',mae)
                mlflow.log_metric('r2',r2)
        except Exception as e:
            raise e