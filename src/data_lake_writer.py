import json
import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)

class DataLakeWriter:
    def __init__(self, raw_path: str, curated_path: str):
        self.raw_path = Path(raw_path)
        self.curated_path = Path(curated_path)

    def write_raw(self, data: Dict[str, Any]) -> None:
        self.raw_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Writing raw weather JSON to %s", self.raw_path)

        with self.raw_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def write_curated(self, data: Dict[str, Any]) -> None:
        if "hourly" not in data:
            logger.warning("No hourly weather data found.")
            return

        df = pd.DataFrame(data["hourly"])
        self.curated_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Writing curated weather data (%d rows) to %s", len(df), self.curated_path)
        df.to_parquet(self.curated_path, index=False)
