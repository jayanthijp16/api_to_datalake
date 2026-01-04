import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                 pagination_config: Optional[Dict[str, Any]] = None):
        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint
        self.params = params or {}
        self.pagination_config = pagination_config or {}

    def _build_url(self) -> str:
        return f"{self.base_url}{self.endpoint}"

    def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch data from API, with optional pagination.
        """
        if self.pagination_config.get("enabled"):
            return self._fetch_with_pagination()
        else:
            return self._fetch_single_page()

    def _fetch_single_page(self) -> List[Dict[str, Any]]:
        url = self._build_url()
        logger.info("Calling API: %s", url)
        response = requests.get(url, params=self.params, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info("Received %d records from API (single page)", len(data))
        return data

    def _fetch_with_pagination(self) -> List[Dict[str, Any]]:
        url = self._build_url()
        all_records: List[Dict[str, Any]] = []

        page_param = self.pagination_config.get("page_param", "page")
        start_page = self.pagination_config.get("start_page", 1)
        max_pages = self.pagination_config.get("max_pages", 1)

        for page in range(start_page, start_page + max_pages):
            params = {**self.params, page_param: page}
            logger.info("Calling API: %s | page=%s", url, page)
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            page_data = response.json()
            if not page_data:
                logger.info("No more data at page %s, stopping pagination.", page)
                break
            logger.info("Received %d records from page %s", len(page_data), page)
            all_records.extend(page_data)

        logger.info("Total records fetched with pagination: %d", len(all_records))
        return all_records


def load_api_config(config_path: str) -> Dict[str, Any]:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
