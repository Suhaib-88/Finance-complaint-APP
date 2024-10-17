from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["pipeline_name", "artifact_dir"])

DataIngestionConfig= namedtuple("DataIngestionConfig", ["from_date", "to_date", "data_ingestion_dir", "download_dir","failed_dir", "file_name", "feature_store_dir", "meta_data_file_path", 
                                                        "data_source_url"])

