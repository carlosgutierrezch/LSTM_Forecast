"""
Script with a class where relies the parameters of the yaml files and the data ingestion address
"""

from TimeSeriesForecast.constants import *
from TimeSeriesForecast.utils.common import read_yaml,create_directories
from TimeSeriesForecast.entity.config_entity import DataIngestionConfig
from TimeSeriesForecast.entity.config_entity import DataValidationConfig
from TimeSeriesForecast.entity.config_entity import DataCleaningConfig
from TimeSeriesForecast.entity.config_entity import DataPreparationConfig
from TimeSeriesForecast.entity.config_entity import ModelTrainerConfig
from TimeSeriesForecast.entity.config_entity import ModelEvaluationConfig
class ConfigurationManager:
    """
    Data class that receives paths and the DataIngestionConfig function to 
    configure the parameters for data ingestion
    """
    def __init__(self,
                config_filepath = CONFIG_FILE_PATH,
                params_filepath = PARAMS_FILE_PATH,
                schema_filepath = SCHEMA_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self)->DataIngestionConfig:
        config= self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config= DataIngestionConfig(
                                                    root_dir=config.root_dir,
                                                    source_URL= config.source_URL,
                                                    local_data_file= config.local_data_file,
                                                    unzip_dir= config.unzip_dir
                                                    )
        return data_ingestion_config
    
    def get_data_validation_config(self)-> DataValidationConfig:
        config= self.config.data_validation
        schema= self.schema.COLUMNS
        
        create_directories([config.root_dir])
        
        data_validation_config= DataValidationConfig(
                                                    root_dir=  config.root_dir,
                                                    STATUS_FILE= config.STATUS_FILE,
                                                    unzip_data_dir= config.unzip_data_dir,
                                                    all_schema= schema
                                                    )
        
        return data_validation_config
    
    def get_data_cleaning_config(self)-> DataCleaningConfig:
        config= self.config.data_cleaning
        
        create_directories([config.root_dir])

        data_cleaning_config= DataCleaningConfig(
                                                root_dir= config.root_dir,
                                                data_path= config.data_path
                                                )
        return data_cleaning_config
    
    def get_data_preparation_config(self)->DataPreparationConfig:
        config= self.config.data_preparation

        create_directories([config.root_dir])

        data_preparation_config= DataPreparationConfig(
                                                        root_dir= config.root_dir,
                                                        data_path= config.data_path,
                                                        save_path= config.save_path
                                                        )
        return data_preparation_config
    
    def model_trainer_config(self)->ModelTrainerConfig:
        config= self.config.model_trainer
        params= self.params.TorchModel
                
        create_directories([config.root_dir])
                
        model_trainer_config= ModelTrainerConfig(
                                                root_dir= config.root_dir,
                                                data_path= config.data_path,
                                                save_path= config.save_path,
                                                model_name= config.model_name,
                                                n_steps= params.n_steps,
                                                split_ratio= params.split_ratio,
                                                seed= params.seed,
                                                drop_out_rate= params.drop_out_rate,
                                                input_size= params.input_size,
                                                hidden_size= params.hidden_size,
                                                num_stacked_layers= params.num_stacked_layers,
                                                learning_rate= params.learning_rate,
                                                num_epochs= params.num_epochs,
                                                batch_size= params.batch_size
                                                )
        return model_trainer_config
    
    def get_eval_config(self)-> ModelEvaluationConfig:
        config= self.config.model_evaluation
        params= self.params.TorchModel

        return_eval= ModelEvaluationConfig(
                                            root_dir=config.root_dir,
                                            test_data_path= config.test_data_path,
                                            model_path= config.model_path,
                                            metric_file_name= config.metric_file_name,
                                            mlflow_url= config.mlflow_url,
                                            batch_size= params.batch_size,
                                            num_epochs= params.num_epochs,
                                            all_params= params
                                            )
        return return_eval