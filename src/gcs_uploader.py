import logging
from google.cloud import storage
from pathlib import Path

logger = logging.getLogger(__name__)

class GCSUploader:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_path: str, gcs_path: str):
        local_file = Path(local_path)

        if not local_file.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")

        blob = self.bucket.blob(gcs_path)
        logger.info("Uploading %s → gs://%s/%s", local_path, self.bucket.name, gcs_path)

        blob.upload_from_filename(local_path)

        logger.info("Upload complete.")
