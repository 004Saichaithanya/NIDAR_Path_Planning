from lxml import etree
from mover import generate_lawnmower_waypoints_irregular

def extract_boundary_from_kml(kml_file):
    tree = etree.parse(kml_file)
    root = tree.getroot()

    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    coords = root.xpath(
        ".//kml:Polygon/kml:outerBoundaryIs/kml:LinearRing/kml:coordinates",
        namespaces=ns
    )

    if not coords:
        raise ValueError("No polygon found in KML")

    coord_text = coords[0].text.strip()

    boundary = []
    for line in coord_text.split():
        lon, lat, *_ = map(float, line.split(","))
        boundary.append((lat, lon))

    return boundary



ALTITUDE_FEET = 50
ALTITUDE_METERS = ALTITUDE_FEET * 0.3048


boundary = extract_boundary_from_kml("mission_area_aoi.kml")

waypoints = generate_lawnmower_waypoints_irregular(boundary, ALTITUDE_METERS)

print(boundary)

for i, wp in enumerate(waypoints):
    print(f"WP{i+1}: {wp}")
