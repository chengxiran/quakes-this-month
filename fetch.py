# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Download one USGS monthly earthquake snapshot into data/."""

from pathlib import Path

import requests


URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson"
DESTINATION = Path(__file__).parent / "data" / "earthquakes_4_5_month.geojson"


def save_usgs_snapshot() -> None:
    """Save the server response body without parsing or rewriting it."""
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(response.content)
    print(f"Saved {len(response.content):,} bytes to {DESTINATION}")


if __name__ == "__main__":
    save_usgs_snapshot()
