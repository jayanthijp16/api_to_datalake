import logging
from typing import Dict, Any

from src.api_client import APIClient
from src.data_lake_writer import DataLakeWriter

logger = logging.getLogger(__name__)

from src.gcs_uploader import GCSUploader
import json

class WeatherPipeline:
    def __init__(self, config, lat, lon, location_key):
        self.config = config
        self.location_key = location_key

        params = config.get("params", {})
        params["latitude"] = lat
        params["longitude"] = lon

        self.api_client = APIClient(
            base_url=config["base_url"],
            endpoint=config["endpoint"],
            params=params,
            pagination_config=config.get("pagination", {})
        )

        # Build dynamic local paths
        raw_path = f"data_lake/raw/weather_{location_key}_raw.json"
        curated_path = f"data_lake/curated/weather_{location_key}_curated.parquet"

        self.writer = DataLakeWriter(raw_path, curated_path)

        # Load GCS config
        with open("config/gcs_config.json") as f:
            gcs_cfg = json.load(f)

        self.gcs_uploader = GCSUploader(gcs_cfg["bucket_name"])
        self.raw_prefix = gcs_cfg["raw_prefix"]
        self.curated_prefix = gcs_cfg["curated_prefix"]

    def run(self):
        logger.info("Starting Weather API → Data Lake → GCS pipeline.")

        data = self.api_client.fetch()

        # Local writes
        self.writer.write_raw(data)
        self.writer.write_curated(data)

        # GCS uploads
        raw_gcs_path = f"{self.raw_prefix}weather_{self.location_key}_raw.json"
        curated_gcs_path = f"{self.curated_prefix}weather_{self.location_key}_curated.parquet"

        self.gcs_uploader.upload_file(self.writer.raw_path, raw_gcs_path)
        self.gcs_uploader.upload_file(self.writer.curated_path, curated_gcs_path)

        logger.info("Pipeline completed successfully.")
