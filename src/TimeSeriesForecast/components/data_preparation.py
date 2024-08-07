"""
hola
"""
import os
from TimeSeriesForecast.constants import *
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast import logger
from pathlib import Path
from TimeSeriesForecast.entity.config_entity import DataPreparationConfig
import pandas as pd
from copy import deepcopy as dc
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import torch

class DataPreparation:
    def __init__(self,config:DataPreparationConfig):
        self.config= config
        self.df= None
        self.X_train= None
        self.X_test= None
        self.y_test= None
        self.y_train= None
        self.y_test= None

    def extract_data_for_preparation(self):
        try:
            self.df= pd.read_csv(self.config.data_path)
            self.df= self.df.to_numpy()
            return self
        except Exception as e:
            raise Exception(f'Problem loading the data: {e}')
    def scaling_data(self):
        try:
            scaler= MinMaxScaler(feature_range=(-1,1))
            transformed= scaler.fit_transform(self.df)
            self.transformed= transformed
            return self
        except Exception as e:
            raise Exception(f'Problem Scaling the data: {e}')
    def transform_split_data(self):
        try:
            X= self.transformed[:,1:]
            y= self.transformed[:,0]
            X= dc(np.flip(X,axis=1))
            split_index= int(len(X)*0.80)
            self.X_train= X[:split_index]
            self.X_test= X[split_index:]
            self.y_train= y[:split_index]
            self.y_test= y[split_index:]
            logger.info('Transform and split done!')
            return self
        except Exception as e:
            raise Exception(f'Problem transforming and splitting the data: {e}')
    def reshaping_data(self):
        try:
            self.X_train= self.X_train.reshape((-1,1,1))
            self.X_test= self.X_test.reshape((-1,1,1))
            self.y_train= self.y_train.reshape((-1,1))
            self.y_test= self.y_test.reshape((-1,1))
            self.X_train= torch.tensor(self.X_train).float()
            self.X_test= torch.tensor(self.X_test).float()
            self.y_train= torch.tensor(self.y_train).float()
            self.y_test= torch.tensor(self.y_test).float()
            return self
        except Exception as e:
            raise Exception(f'Problem reshaping and creating tensors {e}')
    def saving_tensors(self):
        try:
            torch.save({'X_train':self.X_train,'X_test':self.X_test,
                        'y_train':self.y_train,'y_test':self.y_test},self.config.save_path)
            print(f'Tensors have succesfuly saved in: {self.config.save_path}')
            logger.info(f'Tensors succesfully saved in: {self.config.save_path}')
        except Exception as e:
            raise Exception(f'Problem saving the tensors: {e}')