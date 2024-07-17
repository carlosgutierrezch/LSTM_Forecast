from TimeSeriesForecast import logger
from TimeSeriesForecast.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
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