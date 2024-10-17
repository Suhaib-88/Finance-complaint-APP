from src.component.training.data_ingestion import DataIngestion
from exception import FinanceException
from config.config_pipeline.training import FinanceConfig
from logger import logger
import sys

class TrainingPipeline:
    def __init__(self, finance_config: FinanceConfig):
        self.finance_config:FinanceConfig= finance_config

    def start_data_ingestion(self)-> None:
        try:
            data_ingestion_config= self.finance_config.get_data_ingestion_config()
            data_ingestion= DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise FinanceException(e,sys) from e
        

            

