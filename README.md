# Weather API → Data Lake → GCS Loader

A production‑style data ingestion pipeline that fetches weather data for any U.S. city, writes raw and curated datasets locally, and uploads them to Google Cloud Storage (GCS).  
This project demonstrates real-world data engineering patterns including API ingestion, state-aware geocoding, data lake zone design, and cloud integration.

---
## Why This Project Matters

This project demonstrates real data engineering skills that companies look for:

- It mirrors real-world API ingestion patterns used in enterprise ETL/ELT systems.
- It shows cloud-native engineering by integrating with Google Cloud Storage.
- It handles real data quality challenges with state-aware geocoding.
- It uses a clean, modular architecture that is easy to extend and maintain.
- It proves end-to-end ownership: ingestion, transformation, storage, cloud upload, and documentation.

---
##  Features

- **Dynamic city input** (`--city "Hartford,CT"`)
- **State-aware geocoding** (Manchester, CT ≠ Manchester, UK)
- **Weather API ingestion** using Open‑Meteo
- **Raw zone** (JSON)
- **Curated zone** (Parquet)
- **Automatic filename generation** based on city/state
- **Upload to Google Cloud Storage**
- **Modular, production-style architecture**

---

##  Project Structure

api_to_datalake/
│── main.py
│── requirements.txt
│── README.md
│
├── config/
│   ├── weather_config.json
│   └── gcs_config.json
│
├── data_lake/
│   ├── raw/
│   └── curated/
│
└── src/
├── api_client.py
├── geocode.py
├── data_lake_writer.py
├── gcs_uploader.py
└── pipeline.py

---

##  Architecture Overview

### 1. **Input**
User provides a city:
python main.py  --city "Manchester,CT"

### 2. **Geocoding**
- Converts `"Manchester,CT"` → `(lat, lon)`
- State-aware matching ensures correct U.S. city

### 3. **Weather API Call**
- Fetches hourly weather metrics (temperature, humidity, windspeed)

### 4. **Data Lake Writes**
- Raw JSON → `data_lake/raw/weather_Manchester_CT_raw.json`
- Curated Parquet → `data_lake/curated/weather_Manchester_CT_curated.parquet`

### 5. **GCS Upload**
- Uploads both files to your GCS bucket

---

##  Setup Instructions

### 1. Clone the repo
git clone <your-repo-url>
cd api_to_datalake

### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Install Google Cloud CLI  
Download from: https://cloud.google.com/sdk/docs/install

Then authenticate:
gcloud auth application-default login
gcloud config set project <your-project-id>
gcloud auth application-default set-quota-project <your-project-id>

### 5. Configure GCS
Edit `config/gcs_config.json`:
```json
{
  "bucket_name": "your-bucket-name",
  "raw_prefix": "weather/raw/",
  "curated_prefix": "weather/curated/"
}
```

### 6. Running the Pipeline
Fetch weather for a city:

python main.py --city "Hartford,CT"

Output files:
data_lake/raw/weather_Hartford_CT_raw.json
data_lake/curated/weather_Hartford_CT_curated.parquet

GCS upload:
gs://your-bucket/weather/raw/weather_Hartford_CT_raw.json
gs://your-bucket/weather/curated/weather_Hartford_CT_curated.parquet


## Extensibility
This project is designed to grow.
You can easily extend it to:

Multi‑city batch ingestion
Daily scheduled runs (cron / Cloud Scheduler)
BigQuery ingestion
S3 / Azure Data Lake support
Docker + Cloud Run deployment

## License
This project is open for personal and educational use.

## Author
Jayanthi Vaiyapuri  
Senior Data Engineer | Cloud & AI Enthusiast

