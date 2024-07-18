from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast.components.data_validation import DataValidation
from TimeSeriesForecast import logger

STAGE_NAME= 'Data validation stage'

class DataValidationTrainingPipeline:
    def __init__(self) -> None:
        pass
    def main(self):
        try:
            config= ConfigurationManager()
            data_validation_config= config.get_data_validation_config()
            data_validation= DataValidation(config=data_validation_config)
            data_validation.validate_all_columns()
        except Exception as e:
            raise e

if __name__== '__main__':
    try:
        logger.info(f'>>>>>>> stage {STAGE_NAME} STARTED')
        obj= DataValidationTrainingPipeline()
        obj.main()
        logger.info(f'>>>>>>>> stage {STAGE_NAME} COMPLETED')
    except Exception as e:
        raise e