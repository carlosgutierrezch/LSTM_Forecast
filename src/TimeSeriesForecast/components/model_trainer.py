"""
Model trainer module
"""

from TimeSeriesForecast.entity.config_entity import ModelTrainerConfig
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from notebooks.src.functions_torch import TimeSeries
from notebooks.src.functions_torch import LSTM
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast.constants import *
from TimeSeriesForecast import logger

class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig):
        self.config= config
        self.tensor= None
        self.X_train= None
        self.X_test= None
        self.y_train= None
        self.y_test= None
    def tensor_loader(self):
        torch.manual_seed(self.config.seed)
        torch.cuda.manual_seed(self.config.seed)
        np.random.seed(self.config.seed)
        try:
            self.tensor= torch.load(self.config.data_path)
            self.X_train,self.X_test,self.y_train,self.y_test = self.tensor['X_train'],self.tensor['X_test'],\
                                                                self.tensor['y_train'],self.tensor['y_test']
            return self
        except Exception as e:
            raise Exception(f'Problem loading the tensors: {e}')
    def time_series_dataset(self):
        try:
            self.train_dataset= TimeSeries(self.X_train,self.y_train)
            self.test_dataset= TimeSeries(self.X_test,self.y_test)
            
            self.train_loader= DataLoader(self.train_dataset,batch_size=self.config.batch_size,shuffle=True)
            self.test_loader= DataLoader(self.test_dataset,batch_size=self.config.batch_size,shuffle=True)
        except Exception as e:
            raise Exception(f'Problem the class modules {e}')
        return self
    
    def training_torch(self):
        try:
            torch.manual_seed(self.config.seed)
            torch.cuda.manual_seed(self.config.seed)
            np.random.seed(self.config.seed)
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            model= LSTM(self.config.input_size,self.config.hidden_size,self.config.num_stacked_layers)
            model.to(device)
            loss_function = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=self.config.learning_rate)
            
            for epoch in range(self.config.num_epochs):
                model.train(True)
                running_loss = 0.0

                for _, batch in enumerate(self.train_loader):
                    x_batch, y_batch = batch[0].to(device), batch[1].to(device)

                    output = model(x_batch)
                    loss = loss_function(output, y_batch)
                    running_loss += loss.item()

                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    avg_train_loss= running_loss/len(self.train_loader)
                    torch.save(model,self.config.save_path)
                print(f'Epoch {epoch+1}/{self.config.num_epochs}, Train Loss: {avg_train_loss}')
                logger.info(f'Train loss from Torch Model{avg_train_loss}')
            torch.save(model,self.config.save_path)
        except Exception as e:
            raise Exception(f'Problem training the model {e}')