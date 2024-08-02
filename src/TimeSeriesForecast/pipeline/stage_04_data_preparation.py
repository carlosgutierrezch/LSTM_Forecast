from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast.components.data_preparation import DataPreparation
from TimeSeriesForecast import logger

STAGE_NAME= 'Data preparation stage'

class DataPreparationTrainingPipeline:
    def __init__(self)->None:
        pass
    def main(self):
        try:
            config= ConfigurationManager()
            data_preparation_config= config.get_data_preparation_config()
            data_preparation= DataPreparation(config=data_preparation_config)
            data_preparation.extract_data_for_preparation()
            data_preparation.scaling_data()
            data_preparation.transform_split_data()
            data_preparation.reshaping_data()
            data_preparation.saving_tensors()
        except Exception as e:
            raise e
        
if __name__=='__main__':
    try:
        logger.info(f'>>>>>>>>>> {STAGE_NAME} started')
        obj= DataPreparationTrainingPipeline()
        obj.main()
        logger.info(f'>>>>>>>>>> {STAGE_NAME} FINISHED')
    except Exception as e:
        raise e