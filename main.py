from TimeSeriesForecast import logger
from TimeSeriesForecast.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from TimeSeriesForecast.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from TimeSeriesForecast.pipeline.stage_03_data_cleaning import DataCleaningTrainingPipeline
from TimeSeriesForecast.pipeline.stage_04_data_preparation import DataPreparationTrainingPipeline
from TimeSeriesForecast.pipeline.stage_05_data_pipeline import ModelTrainingPipeline
from TimeSeriesForecast.pipeline.stage_06_data_evaluation import ModelEvaluationPipeline
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

STAGE_NAME= 'Data preparation stage'
try:
    logger.info(f'>>>>>>>>>> {STAGE_NAME} STARTED')
    obj= DataPreparationTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>>>>>> {STAGE_NAME} FINISHED')
except Exception as e:
    raise e

STAGE_NAME= 'Model training stage'
try:
    logger.info(f'>>>>>>>>>> {STAGE_NAME} STARTED')
    obj= ModelTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>>>>>> {STAGE_NAME} FINISHED')
except Exception as e:
    raise e

STAGE_NAME= 'Data evaluation stage'
try:
    logger.info(f'>>>>>>>>>> {STAGE_NAME} STARTED')
    obj= ModelEvaluationPipeline()
    obj.main()
    logger.info(f'>>>>>>>>>> {STAGE_NAME} FINISHED')
except Exception as e:
    raise e 