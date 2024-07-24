"""
Script where the data is transformed and splittee in Train and Test, the data needs to be passed
to Numpy and flip the columns to train the Torch
"""
import os
from TimeSeriesForecast.constants import *
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast import logger
from pathlib import Path
from TimeSeriesForecast.entity.config_entity import DataTransformationConfig
import pandas as pd

class DataTransformation:
    def __init__(self,config: DataTransformationConfig):
        self.config = config

    def read_and_prepare_data(self):
        try:
            df= pd.read_csv(self.config.data_path)
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values(by='Date', inplace=True)
            df.reset_index(inplace=True, drop=True)
            df.set_index('Date', inplace=True)
            return df
        except Exception as e:
            raise e

    def rename_clean_data(self,df):
        for column in df.columns:
            if column != 'Date' and df[column].dtype == 'object':
                df[column] = df[column].str.replace('$', '', regex=False).astype(float)
                
        if 'Close/Last' in df.columns:
            df.rename(columns={'Close/Last':'Value'},inplace=True)       
        return df

    def loc_data(self,df):
        df= df[['Value']]
        df= df.loc['2023':'2024'].copy()
        return df

    def lag_transform_data(self,df,n_steps):
        try:
            for i in range(1,n_steps+1):
                df[f'Value (t-{i})']= df.iloc[:,0].shift(i)

            df.dropna(inplace=True)
            df=df.asfreq('D')
            df.ffill(inplace=True)
            
            split_index= int(len(df) * 0.90)
            train= df[:split_index]
            test= df[split_index:]
            train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
            test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)
            logger.info("Splitted data into train and test")
            logger.info(f"Train data shape: {train.shape}")
            logger.info(f"Test data shape: {test.shape}")
        except Exception as e:
            raise e