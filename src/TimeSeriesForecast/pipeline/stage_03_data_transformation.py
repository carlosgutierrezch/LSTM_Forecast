from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast.components.data_transformation import DataTransformation
from TimeSeriesForecast import logger

STAGE_NAME= 'Data Transformation Stage'

class DataTransformationTrainingPipeline:
    def __init__(self)->None:
        pass
    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            df= data_transformation.read_and_prepare_data()
            df= data_transformation.rename_clean_data(df)
            df= data_transformation.loc_data(df)
            data_transformation.lag_transform_data(df,n_steps=7)
        except Exception as e:
            raise e
        
if __name__== '__main__':
    try:
        logger.info(f">>>>>>>>> {STAGE_NAME} staryted")
        obj= DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>> {STAGE_NAME} completed")
    except Exception as e:
        raise e