import sys,os
from typing import List
from collections import namedtuple
from exception import FinanceException
from entity.config_entity import DataIngestionConfig
from entity.artifact_entity import DataIngestionArtifact
from entity.metadata_entity import DataIngestionMetadata
import pandas as pd
from logger import logger
from datetime import datetime
from config.spark_manager import spark_session
import requests
import uuid
import time
import re
import json 



DownloadUrl = namedtuple("DownloadUrl", ["url", "file_name",'n_retry'])

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig, n_retry=5):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.failed_download_urls:List[DownloadUrl] = []
            self.n_retry= n_retry
        except Exception as e:
          raise FinanceException(e,sys)
        


    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            if self.data_ingestion_config.from_date != self.data_ingestion_config.to_date:
                self.download_files()

            if os.path.exists(self.data_ingestion_config.download_dir):
                logger.info(f"Converting and combining downloaded json into parquet format...")
                file_path = self.convert_json_files_to_parquet()
                self.write_metadata(file_path=file_path)

            feature_store_file_path= os.path.join(self.data_ingestion_config.feature_store_dir, self.data_ingestion_config.file_name)

            artifact= DataIngestionArtifact(feature_store_file_path=feature_store_file_path, download_dir=self.data_ingestion_config.download_dir, metadata_file_path=self.data_ingestion_config.metadata_file_path)
            logger.info(f"Data ingestion artifact: {artifact}")
            return artifact

        except Exception as e:
            raise FinanceException(e,sys)
        

    def write_metadata(self, file_path:str):
        try:
            logger.info(f"Writing metadata file...")
            metadata_info= DataIngestionMetadata(metadata_file_path=self.data_ingestion_config.metadata_file_path)
            metadata_info.write_metadata_info(from_date=self.data_ingestion_config.from_date, to_date=self.data_ingestion_config.to_date, data_file_path=file_path)
            logger.info(f"Metadata file is written successfully...")

        except Exception as e:
            raise FinanceException(e,sys)
        

        
    def convert_json_files_to_parquet(self):
        try:
            json_data_dir= self.data_ingestion_config.download_dir
            data_dir= self.data_ingestion_config.feature_store_dir
            output_file_name= self.data_ingestion_config.file_name
            os.makedirs(data_dir, exist_ok=True)
            file_path= os.path.join(data_dir, output_file_name)
            logger.info(f"Parquet file to be created at {file_path}...")
            if not os.path.exists(json_data_dir):
                return file_path
            
            for file_name in os.listdir(json_data_dir):
                json_file_path= os.path.join(json_data_dir, file_name)
                logger.debug(f"Converting {json_file_path} into parquet format...")

                df= spark_session.read.json(json_file_path)

                if df.count() > 0:
                    df.write.mode("append").parquet(file_path)

            return file_path
        
        except Exception as e:
            raise FinanceException(e,sys)


    def download_files(self, n_day_interval:int=None):
        try:
           required_interval= self.get_required_interval()
           logger.info(f"Required interval is {required_interval}, Now starting download files...")
           for index in range(1, len(required_interval)):
               from_date, to_date= required_interval[index-1], required_interval[index]
               logger.debug(f"Downloading files for the interval {from_date} to {to_date}")
               datasource_url:str= self.data_ingestion_config.data_source_url
               url= datasource_url.replace("<todate>", to_date).replace("<fromdate>", from_date)
               logger.debug(f"Downloading files from {url}")

               file_name= f"{self.data_ingestion_config.file_name}_{from_date}_{to_date}.json"
               file_path= os.path.join(self.data_ingestion_config.download_dir, file_name)
               download_url= DownloadUrl(url=url, file_path=file_path, n_retry=self.n_retry)
               self.download_data(download_url=download_url)
               logger.info(f"All files are downloaded successfully @ {index}")

        except Exception as e:
            raise FinanceException(e,sys)
        


        
    def download_data(self, download_url:DownloadUrl):
        try:
            logger.info(f"Downloading data from {download_url.url}...")
            download_dir= os.path.dirname(download_url.file_path)
            
            os.makedirs(download_dir, exist_ok=True)
            data= requests.get(download_url.url, params={"User-agent": f"your bot {uuid.uuid4()}"})

            try:
                logger.info(f"Downloading data from {download_url.file_path}...")
                with open(download_url.file_path, "wb") as file:
                    finance_complaint_data= list(map(lambda x:x['_source'], filter(lambda x:"_source" in x.keys(), json.loads(data.content))))
                    json.dump(finance_complaint_data, file)

                logger.info(f"Data is downloaded successfully... {download_url.file_path}")
            except Exception as e:
                logger.error(f"Failed to download data from {download_url.url}...")
                if os.path.exists(download_url.file_path):
                    os.remove(download_url.file_path)
                self.retry_download_data(data, download_url=download_url)

        except Exception as e:
            raise FinanceException(e,sys)
        


    def retry_download_data(self, data, download_url:DownloadUrl):
        try:
            if download_url.n_retry ==0:
                self.failed_download_urls.append(download_url)
                logger.info(f"Failed to download data from {download_url.url}...")
                return
            
            content= data.content.decode("utf-8")
            wait_second= re.findall(r'\d+', content)

            if len(wait_second) > 0:
                time.sleep(int(wait_second[0])+2)

            failed_file_path= os.path.join(self.data_ingestion_config.failed_dir, os.path.basename(download_url.file_path))
            os.makedirs(self.data_ingestion_config.failed_dir, exist_ok=True)
            with open(failed_file_path, "wb") as file:
                file.write(data.content)

            download_url = DownloadUrl(url=download_url.url, file_path=failed_file_path, n_retry=download_url.n_retry-1)
            self.download_data(download_url=download_url)

        except Exception as e:
            raise FinanceException(e,sys)
                

        
                    

        
    def get_required_interval(self):
        try:
            start_date= datetime.strptime(self.data_ingestion_config.from_date, "%Y-%m-%d")
            end_date= datetime.strptime(self.data_ingestion_config.to_date, "%Y-%m-%d")
            n_diff_days= (end_date- start_date).days
            if n_diff_days > 30:
                freq="M"
            elif n_diff_days > 365:
                freq="Y"
            elif n_diff_days > 7:
                freq="W"

            logger.debug(f"Required interval is {freq}")
            if freq is None:
                interval= pd.date_range(start= self.data_ingestion_config.from_date, end= self.data_ingestion_config.to_date, periods=2).astype('str').tolist()
            else:
                interval= pd.date_range(start= self.data_ingestion_config.from_date, end= self.data_ingestion_config.to_date, freq=freq).astype('str').tolist()

            logger.debug(f"Required interval is {interval}")
            if self.data_ingestion_config.to_date not in interval:
                interval.append(self.data_ingestion_config.to_date)
            return interval
        
        except Exception as e:
            raise FinanceException(e,sys)
