# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Draw an SVG of earthquake locations from the committed USGS snapshot."""

import json
from pathlib import Path


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "earthquakes_4_5_month.geojson"
OUTPUT_FILE = ROOT / "out" / "earthquakes_4_5_month.svg"


def marker_area(magnitude: float) -> float:
    """Convert earthquake magnitude to a readable SVG circle radius."""
    return 2.2 + (magnitude - 4.5) * 1.35


def depth_colour(depth_km: float, maximum_depth: float) -> str:
    """Map depth from deep purple to pale yellow."""
    fraction = min(max(depth_km / maximum_depth, 0), 1)
    stops = [(28, 18, 68), (124, 43, 128), (230, 95, 48), (252, 226, 112)]
    scaled = fraction * (len(stops) - 1)
    lower = int(scaled)
    upper = min(lower + 1, len(stops) - 1)
    blend = scaled - lower
    rgb = [round(stops[lower][i] * (1 - blend) + stops[upper][i] * blend) for i in range(3)]
    return "#" + "".join(f"{channel:02x}" for channel in rgb)


def make_plot() -> None:
    """Read the cached earthquake events and save a longitude-latitude plot."""
    with DATA_FILE.open(encoding="utf-8") as data_file:
        feed = json.load(data_file)

    longitudes = []
    latitudes = []
    magnitudes = []
    depths_km = []

    for event in feed["features"]:
        longitude, latitude, depth_km = event["geometry"]["coordinates"]
        magnitude = event["properties"]["mag"]
        if magnitude is None or depth_km is None:
            continue
        longitudes.append(longitude)
        latitudes.append(latitude)
        magnitudes.append(magnitude)
        depths_km.append(depth_km)

    width, height = 1200, 700
    left, top, plot_width, plot_height = 92, 120, 990, 440
    maximum_depth = max(depths_km, default=1)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#101820"/>',
        '<text x="92" y="55" fill="#f4f1de" font-family="Arial,sans-serif" font-size="27" font-weight="700">EARTHQUAKES, ONE MONTH / MAGNITUDE 4.5+</text>',
        '<text x="92" y="82" fill="#c5c8c6" font-family="Arial,sans-serif" font-size="14">A global view of reported epicentres, depth and relative magnitude</text>',
    ]

    for longitude in range(-180, 181, 60):
        x = left + (longitude + 180) / 360 * plot_width
        svg.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_height}" stroke="#65727c" stroke-opacity=".42"/>')
        svg.append(f'<text x="{x:.1f}" y="{top + plot_height + 23}" text-anchor="middle" fill="#e8e6df" font-family="Arial,sans-serif" font-size="12">{longitude}°</text>')
    for latitude in range(-60, 61, 30):
        y = top + (90 - latitude) / 180 * plot_height
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#65727c" stroke-opacity=".42"/>')
        svg.append(f'<text x="{left - 13}" y="{y + 4:.1f}" text-anchor="end" fill="#e8e6df" font-family="Arial,sans-serif" font-size="12">{latitude}°</text>')

    for longitude, latitude, magnitude, depth_km in zip(longitudes, latitudes, magnitudes, depths_km):
        x = left + (longitude + 180) / 360 * plot_width
        y = top + (90 - latitude) / 180 * plot_height
        radius = marker_area(magnitude)
        colour = depth_colour(depth_km, maximum_depth)
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{colour}" fill-opacity=".82" stroke="#f4f1de" stroke-width=".55"><title>Magnitude {magnitude}; depth {depth_km} km</title></circle>')

    svg.extend([
        f'<text x="{left + plot_width / 2}" y="{top + plot_height + 51}" text-anchor="middle" fill="#e8e6df" font-family="Arial,sans-serif" font-size="14">Longitude (degrees)</text>',
        f'<text x="25" y="{top + plot_height / 2}" text-anchor="middle" fill="#e8e6df" font-family="Arial,sans-serif" font-size="14" transform="rotate(-90 25 {top + plot_height / 2})">Latitude (degrees)</text>',
        '<text x="1110" y="143" fill="#e8e6df" font-family="Arial,sans-serif" font-size="12">DEPTH</text>',
    ])
    for step in range(61):
        fraction = step / 60
        y = 160 + fraction * 290
        svg.append(f'<line x1="1110" y1="{y:.1f}" x2="1132" y2="{y:.1f}" stroke="{depth_colour(fraction * maximum_depth, maximum_depth)}" stroke-width="5"/>')
    svg.extend([
        '<text x="1140" y="166" fill="#e8e6df" font-family="Arial,sans-serif" font-size="11">0 km</text>',
        f'<text x="1140" y="455" fill="#e8e6df" font-family="Arial,sans-serif" font-size="11">{maximum_depth:.0f} km</text>',
        '<circle cx="1100" cy="505" r="3" fill="#e8e6df"/><text x="1115" y="509" fill="#e8e6df" font-family="Arial,sans-serif" font-size="11">M4.5</text>',
        '<circle cx="1100" cy="535" r="7" fill="#e8e6df"/><text x="1115" y="539" fill="#e8e6df" font-family="Arial,sans-serif" font-size="11">M7.0</text>',
        '<text x="92" y="645" fill="#c5c8c6" font-family="Arial,sans-serif" font-size="12">Each point is one reported event · larger circles = higher magnitude · snapshot downloaded 2026-10-03 UTC</text>',
        '</svg>',
    ])
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")
    print(f"Plotted {len(longitudes)} events to {OUTPUT_FILE}")


if __name__ == "__main__":
    make_plot()
