from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast.components.data_cleaning import DataCleaning
from TimeSeriesForecast import logger

STAGE_NAME= 'Data Cleaning Stage'

class DataCleaningTrainingPipeline:
    def __init__(self)->None:
        pass
    def main(self):
        try:
            config= ConfigurationManager()
            data_cleaning_config= config.get_data_cleaning_config()
            data_cleaning_config= DataCleaning(config=data_cleaning_config)
            data_cleaning_config.read_and_prepare_data()
            data_cleaning_config.clean_data()
            data_cleaning_config.filter_data()
            data_cleaning_config.transform_data()
        except Exception as e:
            raise e
        
if __name__== '__main__':
    try:
        logger.info(f">>>>>>>>> {STAGE_NAME} started")
        obj= DataCleaningTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>> {STAGE_NAME} completed")
    except Exception as e:
        raise e