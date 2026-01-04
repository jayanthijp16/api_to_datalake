import logging
import sys
import argparse

from src.api_client import load_api_config
from src.pipeline import WeatherPipeline
from src.geocode import geocode_location

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

def parse_args():
    parser = argparse.ArgumentParser(description="Weather API → Data Lake Loader")

    parser.add_argument("--city", type=str, help="City name (e.g., 'Hartford, CT')")
    parser.add_argument("--lat", type=float, help="Latitude")
    parser.add_argument("--lon", type=float, help="Longitude")

    return parser.parse_args()

def normalize_location_for_filename(location: str) -> str:
    # Remove commas, spaces, and special characters
    cleaned = (
        location.replace(",", " ")
                .replace("  ", " ")
                .strip()
                .replace(" ", "_")
    )
    return cleaned


if __name__ == "__main__":
    setup_logging()
    args = parse_args()

    # Determine coordinates
    if args.city:
        lat, lon = geocode_location(args.city)
        logging.info(f"Resolved '{args.city}' → lat={lat}, lon={lon}")
    elif args.lat and args.lon:
        lat, lon = args.lat, args.lon
    else:
        raise ValueError("You must provide either --city or --lat and --lon")

    config_path = "config/weather_config.json"
    logging.info("Loading weather config from %s", config_path)

    config = load_api_config(config_path)
    location_key = normalize_location_for_filename(args.city)
    pipeline = WeatherPipeline(config, lat, lon, location_key)
    pipeline.run()
