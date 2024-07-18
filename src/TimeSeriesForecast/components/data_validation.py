"""
Script where the data downloaded is validated using a bool conditional
"""
import os
from TimeSeriesForecast.constants import *
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast import logger
from pathlib import Path
from TimeSeriesForecast.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self,config: DataValidationConfig):
        self.config= config
    
    def validate_all_columns(self)->bool:
        try:
            validation_status = None
            data= pd.read_csv(self.config.unzip_data_dir)
            all_columns= list(data.columns)
            
            all_schema= self.config.all_schema.keys()
            
            for col in all_columns:
                if col not in all_schema:
                    validation_status= False
                    with open(self.config.STATUS_FILE,'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status=True
                    with open(self.config.STATUS_FILE,'w') as x:
                        x.write(f"Validation status: {validation_status}")
            return validation_status
        except Exception as e:
            raise e