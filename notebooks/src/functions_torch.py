"""
Series of classes for data transformation in LSTM-TORCH module
"""
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class  TransformLag:
    """
    Series of transformation from DataFrame tu numpy with all their variances

    Returns:
        _type_: Different set of values from pandas tu numpy
    """
    @staticmethod
    def transform_df(df:pd.DataFrame,n_steps:int)->pd.DataFrame:
        """
        Create lags from the 'Value' column to pass in a regressive way to the model

        Args:
            df (pd.DataFrame): Pandas DataFrame
            n_steps (int): Number of lags to create

        Returns:
            _type_: Pandas DataFrame with lags
        """

        for i in range(1,n_steps+1):
            df[f'Value (t-{i})']= df.iloc[:,0].shift(i)

        df.dropna(inplace=True)
        return df

    @staticmethod
    def lag_numpy(df:pd.DataFrame)-> np.ndarray:
        """
        Takes a Pandas DataFrame and make transformations to 
        return a numpy array of numbers

        Args:
            df (pd.DataFrame): Pandas DataFrame

        Returns:
            np.ndarray: Matrix with array of numbers
        """
        df=df.asfreq('D')
        df.ffill(inplace=True)
        data_array= df.to_numpy()
        return data_array

  
    @staticmethod
    def lag_transform(df:pd.DataFrame,n_steps:int)->pd.DataFrame:

        for i in range(1,n_steps+1):
            df[f'Value (t-{i})']= df.iloc[:,0].shift(i)

        df.dropna(inplace=True)
        df=df.asfreq('D')
        df.ffill(inplace=True)
        # data_array= df.to_numpy()
        return df

class TimeSeries(Dataset):
    def __init__(self,X,y):
        self.X= X
        self.y= y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self,i):
        return self.X[i],self.y[i]

def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    
class LSTM(nn.Module):

    def __init__(self,input_size,hidden_size,num_stacked_layers):
        super().__init__()
        self.hidden_size= hidden_size
        self.num_stacked_layers= num_stacked_layers
        
        self.lstm= nn.LSTM(input_size,hidden_size,num_stacked_layers,
                           batch_first=True,dropout= 0.05)
        self.fc= nn.Linear(hidden_size,1)
        
    def forward(self,x):
        batch_size= x.size(0)
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        h0= torch.zeros(self.num_stacked_layers,batch_size,self.hidden_size).to(device)
        c0= torch.zeros(self.num_stacked_layers,batch_size,self.hidden_size).to(device)
        
        out,_ = self.lstm(x,(h0,c0))
        out= self.fc(out[:,-1,:])
        return out
    
def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2