#!/usr/bin/env python3
"""Add distance and elevation metadata to GPX files.

Uses <extensions> for structured data:
  <route:distance>59.9</route:distance>
  <route:elevation>245</route:elevation>
  <route:stops>
    <route:stop name="Cafe Name" url="https://..."/>
  </route:stops>

Preserves existing stops when updating distance/elevation.
"""

import gpxpy
from pathlib import Path
from xml.etree import ElementTree as ET

ROUTE_NS = "http://gpx-routes.example.com/1.0"


def get_existing_stops(gpx: gpxpy.gpx.GPX) -> list[ET.Element]:
    """Extract existing stops from metadata extensions."""
    stops = []
    for ext in gpx.metadata_extensions:
        if ext.tag == f"{{{ROUTE_NS}}}stops":
            for stop in ext:
                if stop.tag == f"{{{ROUTE_NS}}}stop":
                    stops.append(stop)
    return stops


def process_gpx(filepath: Path) -> None:
    with open(filepath, encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    total_distance = 0.0
    total_uphill = 0.0

    for track in gpx.tracks:
        total_distance += track.length_3d() or 0
        uphill, _ = track.get_uphill_downhill()
        total_uphill += uphill or 0

    if total_distance == 0:
        print(f"  Skipping {filepath.name}: no track data")
        return

    distance_km = total_distance / 1000

    # Preserve existing stops
    existing_stops = get_existing_stops(gpx)

    # Clear old metadata
    gpx.keywords = None
    gpx.metadata_extensions.clear()

    # Add namespace
    gpx.nsmap["route"] = ROUTE_NS

    # Create new extensions
    dist_el = ET.Element(f"{{{ROUTE_NS}}}distance")
    dist_el.text = f"{distance_km:.1f}"

    elev_el = ET.Element(f"{{{ROUTE_NS}}}elevation")
    elev_el.text = f"{total_uphill:.0f}"

    gpx.metadata_extensions.append(dist_el)
    gpx.metadata_extensions.append(elev_el)

    # Restore stops if any
    if existing_stops:
        stops_el = ET.Element(f"{{{ROUTE_NS}}}stops")
        for stop in existing_stops:
            stops_el.append(stop)
        gpx.metadata_extensions.append(stops_el)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())

    stops_count = len(existing_stops)
    stops_info = f", {stops_count} stops" if stops_count else ""
    print(f"  {filepath.name}: {distance_km:.1f} km, +{total_uphill:.0f}m{stops_info}")


def main() -> None:
    gpx_dir = Path("gpx")
    gpx_files = list(gpx_dir.rglob("*.gpx"))

    print(f"Found {len(gpx_files)} GPX files\n")

    for filepath in sorted(gpx_files):
        process_gpx(filepath)

    print(f"\nDone! Updated {len(gpx_files)} files.")


if __name__ == "__main__":
    main()
