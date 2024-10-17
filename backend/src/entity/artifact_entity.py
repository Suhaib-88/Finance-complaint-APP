from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["feature_store_file_path", "meta_data_file_path", "download_dir"])