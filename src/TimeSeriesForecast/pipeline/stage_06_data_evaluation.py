
from TimeSeriesForecast.components.model_evaluation import ModelEvaluation
from TimeSeriesForecast.config.configuration import ConfigurationManager
from TimeSeriesForecast import logger

STAGE_NAME= 'Data validation stage'

class ModelEvaluationPipeline:
    def __init__(self)->None:
        pass
    def main(self):
        try:

            configu= ConfigurationManager()
            model_eval= configu.get_eval_config()
            model_evaluation= ModelEvaluation(config=model_eval)
            model_evaluation.tensor_loader()
            model_evaluation.model_loader()
        except Exception as e:
            raise e
    
if __name__=='__main__':
    try:
        logger.info(f'>>>>>>>>> {STAGE_NAME} started')
        obj= ModelEvaluationPipeline()
        obj.main()
        logger.info(f'>>>>>>>>> {STAGE_NAME} finished')
    except Exception as e:
        raise e

    