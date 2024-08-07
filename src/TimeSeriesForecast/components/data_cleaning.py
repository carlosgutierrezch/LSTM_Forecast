"""
Script where the data is transformed and splittee in Train and Test, the data needs to be passed
to Numpy and flip the columns to train the Torch
"""
import os
from TimeSeriesForecast.constants import *
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast import logger
from pathlib import Path
from TimeSeriesForecast.entity.config_entity import DataCleaningConfig
import pandas as pd

class DataCleaning:
    def __init__(self, config: DataCleaningConfig):
        self.config = config
        self.df = None

    def read_and_prepare_data(self):
        try:
            self.df = pd.read_csv(self.config.data_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df.sort_values(by='Date', inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.df.set_index('Date', inplace=True)
            return self
        except Exception as e:
            raise Exception(f"Error in read_and_prepare_data: {str(e)}")

    def clean_data(self):
        try:
            self.df.columns = self.df.columns.str.strip()
            for column in self.df.columns:
                if self.df[column].dtype == 'object' and column != 'Date':
                    self.df[column] = self.df[column].str.replace('$', '', regex=False).astype(float)
            if 'Close/Last' in self.df.columns:
                self.df.rename(columns={'Close/Last': 'Value'}, inplace=True)
            return self
        except Exception as e:
            raise Exception(f"Error in clean_data: {str(e)}")

    def filter_data(self):
        try:
            self.df = self.df[['Value']]
            self.df = self.df.loc['2021':'2023'].copy()
            return self
        except Exception as e:
            raise Exception(f"Error in filter_data: {str(e)}")

    def transform_data(self):
        try:
            for i in range(1, 1 + 1):
                self.df[f'Value (t-{i})'] = self.df['Value'].shift(i)
            self.df.dropna(inplace=True)
            self.df = self.df.asfreq('D')
            self.df.ffill(inplace=True)

            output_path = os.path.join(self.config.root_dir, 'data.csv')
            self.df.to_csv(output_path, index=False)
            
            logger.info('Train and test data prepared and saved.')
            logger.info(f'Data shape after transformation: {self.df.shape}')

            return self.df
        except Exception as e:
            raise Exception(f"Error in transform_data: {str(e)}")