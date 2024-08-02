from TimeSeriesForecast import logger
from TimeSeriesForecast.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from TimeSeriesForecast.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from TimeSeriesForecast.pipeline.stage_03_data_cleaning import DataCleaningTrainingPipeline
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


STAGE_NAME= 'Data ingestion stage'
try:
    logger.info(f'>>>>>> stage {STAGE_NAME} started <<<<<')
    obj= DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>>>>> stage {STAGE_NAME} completed! <<<<<<')
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME= 'Data validation stage'
try:
    logger.info(f'>>>>>>> stage {STAGE_NAME} STARTED')
    obj= DataValidationTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>>>> stage {STAGE_NAME} COMPLETED')
except Exception as e:
    raise e

STAGE_NAME= 'Data Cleaning stage'
try:
    logger.info(f'>>>>>>> {STAGE_NAME} STARTED')
    obj= DataCleaningTrainingPipeline()
    obj.main()
    logger.info('>>>>>>>> stage {STAGE_NAME} COMPLETED')
except Exception as e:
    raise e