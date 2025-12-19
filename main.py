from lxml import etree
from mover import generate_curved_center_coverage

# -------------------------------
# KML Boundary Extraction
# -------------------------------
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


# -------------------------------
# KML Waypoint Export
# -------------------------------

def export_waypoints_to_kml(waypoints, output_file):
    NS = "http://www.opengis.net/kml/2.2"
    KML = "{%s}" % NS

    kml = etree.Element(KML + "kml", nsmap={None: NS})
    doc = etree.SubElement(kml, KML + "Document")

    etree.SubElement(doc, KML + "name").text = "Curved Center Coverage Path"

    placemark = etree.SubElement(doc, KML + "Placemark")
    etree.SubElement(placemark, KML + "name").text = "Flight Path"

    linestring = etree.SubElement(placemark, KML + "LineString")
    etree.SubElement(linestring, KML + "tessellate").text = "1"
    etree.SubElement(linestring, KML + "altitudeMode").text = "absolute"

    coords = etree.SubElement(linestring, KML + "coordinates")

    coord_lines = []
    for wp in waypoints:
        lat = wp[0]
        lon = wp[1]
        alt = wp[2] if len(wp) > 2 else 15.24
        coord_lines.append(f"{lon},{lat},{alt}")

    coords.text = "\n".join(coord_lines)

    etree.ElementTree(kml).write(
        output_file,
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True
    )

    print(f"[✓] VALID KML exported → {output_file}")





# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    ALTITUDE_FEET = 50
    ALTITUDE_METERS = ALTITUDE_FEET * 0.3048

    boundary = extract_boundary_from_kml("mission_area_aoi_2.kml")

    waypoints = generate_curved_center_coverage(
        boundary,
        ALTITUDE_METERS
    )

    print(f"[INFO] Generated {len(waypoints)} waypoints")

    export_waypoints_to_kml(
        waypoints,
        "step3_curved_center_path.kml"
    )
