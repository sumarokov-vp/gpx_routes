#!/usr/bin/env python3
"""Add distance and elevation metadata to all GPX files."""

import gpxpy
from pathlib import Path


def process_gpx(filepath: Path) -> None:
    with open(filepath, encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    total_distance = 0.0
    total_uphill = 0.0
    total_downhill = 0.0

    for track in gpx.tracks:
        total_distance += track.length_3d() or 0
        uphill, downhill = track.get_uphill_downhill()
        total_uphill += uphill or 0
        total_downhill += downhill or 0

    if total_distance == 0:
        print(f"  Skipping {filepath.name}: no track data")
        return

    distance_km = total_distance / 1000
    desc = f"Distance: {distance_km:.1f} km | Elevation: +{total_uphill:.0f}m / -{total_downhill:.0f}m"

    gpx.description = desc

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())

    print(f"  {filepath.name}: {distance_km:.1f} km, +{total_uphill:.0f}m/-{total_downhill:.0f}m")


def main() -> None:
    gpx_dir = Path("gpx")
    gpx_files = list(gpx_dir.rglob("*.gpx"))

    print(f"Found {len(gpx_files)} GPX files\n")

    for filepath in sorted(gpx_files):
        process_gpx(filepath)

    print(f"\nDone! Updated {len(gpx_files)} files.")


if __name__ == "__main__":
    main()
