from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast.components.model_trainer import ModelTrainer
from TimeSeriesForecast import logger

STAGE_NAME= 'Model Training stage'

class ModelTrainingPipeline:
    def __init__(self)->None:
        pass
    def main(self):
        try:
            config= ConfigurationManager()
            model_trainer= config.model_trainer_config()
            model_t= ModelTrainer(config=model_trainer)
            model_t.tensor_loader()
            model_t.time_series_dataset()
            model_t.training_torch()
        except Exception as e:
            raise e

if __name__=='__main__':
    try:
        logger.info(f'>>>>>>>>> {STAGE_NAME} started')
        obj= ModelTrainingPipeline()
        obj.main()
        logger.info(f'>>>>>>>>> {STAGE_NAME} FINISHED')
    except Exception as e:
        raise e