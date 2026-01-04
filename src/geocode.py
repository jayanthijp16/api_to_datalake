import requests
from typing import Optional, Tuple, List, Dict


US_STATE_MAP = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}


def geocode_location(location: str) -> Tuple[float, float]:
    """
    Convert a location like 'Manchester,CT' or 'Hartford, CT' into lat/lon.
    Fully state-aware and US-aware.
    """

    city, state_code = _parse_city_state(location)
    state_full = US_STATE_MAP.get(state_code.upper()) if state_code else None

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 20}

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        raise ValueError(f"No geocoding results for: {location}")

    # 1. Exact match: US + state code match
    for r in results:
        if r.get("country_code") == "US" and r.get("admin1_code") == state_code:
            return r["latitude"], r["longitude"]

    # 2. Match: US + full state name match
    for r in results:
        if r.get("country_code") == "US" and r.get("admin1") == state_full:
            return r["latitude"], r["longitude"]

    # 3. Any US match
    for r in results:
        if r.get("country_code") == "US":
            return r["latitude"], r["longitude"]

    # 4. Fallback: first result
    r = results[0]
    return r["latitude"], r["longitude"]


def _parse_city_state(location: str) -> Tuple[str, Optional[str]]:
    """
    Parse 'Manchester,CT' → ('Manchester', 'CT')
    Parse 'Hartford, CT' → ('Hartford', 'CT')
    Parse 'Hartford' → ('Hartford', None)
    """
    parts = [p.strip() for p in location.split(",") if p.strip()]

    if len(parts) == 1:
        return parts[0], None

    city = parts[0]
    state = parts[1].upper()

    # Normalize state code (CT, MA, NH, etc.)
    if state in US_STATE_MAP:
        return city, state

    # If user typed "Connecticut" instead of "CT"
    for code, full in US_STATE_MAP.items():
        if state.lower() == full.lower():
            return city, code

    return city, None
