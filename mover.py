from shapely.geometry import LineString, MultiLineString, GeometryCollection,Polygon
from GPS_to_XY import gps_to_xy, xy_to_gps
from calSwath_SP import calculate_pass_spacing


# def polygon_centroid(points):
#     x_list = [p[0] for p in points]
#     y_list = [p[1] for p in points]
#     return sum(x_list)/len(points), sum(y_list)/len(points)


def generate_refined_coverage(boundary_gps, altitude_m):
    # Reference for local frame
    ref_lat, ref_lon = boundary_gps[0]

    # Convert boundary to XY
    boundary_xy = [gps_to_xy(lat, lon, ref_lat, ref_lon)
                   for lat, lon in boundary_gps]

    polygon = Polygon(boundary_xy)

    # Step 2 parameters
    _, pass_spacing = calculate_pass_spacing(
        altitude_m=altitude_m,
        fov_deg=57,
        overlap=0.25
    )

    # Centroid-based scanning
    cx, cy = polygon.centroid.coords[0]

    min_y, max_y = polygon.bounds[1], polygon.bounds[3]

    waypoints = []
    direction = True

    offsets = []
    i = 0
    while True:
        y1 = cy + i * pass_spacing
        y2 = cy - i * pass_spacing
        if y1 > max_y and y2 < min_y:
            break
        if y1 <= max_y:
            offsets.append(y1)
        if y2 >= min_y and i != 0:
            offsets.append(y2)
        i += 1
    offsets.sort(key=lambda y: abs(y - cy))
    for y in offsets:
        sweep = LineString([
            (polygon.bounds[0] - 50, y),
            (polygon.bounds[2] + 50, y)
        ])

        clipped = sweep.intersection(polygon)

        if clipped.is_empty:
            continue

        if isinstance(clipped, LineString):
            segments = [clipped]

        elif isinstance(clipped, MultiLineString):
            segments = list(clipped.geoms)

        elif isinstance(clipped, GeometryCollection):
            segments = [g for g in clipped.geoms if isinstance(g, LineString)]

        else:
            continue

        MIN_SWEEP_LENGTH = 12 

        for seg in segments:
            if seg.length < MIN_SWEEP_LENGTH:
                continue
            x1, y1 = seg.coords[0]
            x2, y2 = seg.coords[-1]

            if not direction:
                x1, y1, x2, y2 = x2, y2, x1, y1

            lat1, lon1 = xy_to_gps(x1, y1, ref_lat, ref_lon)
            lat2, lon2 = xy_to_gps(x2, y2, ref_lat, ref_lon)

            waypoints.append((lat1, lon1, altitude_m))
            waypoints.append((lat2, lon2, altitude_m))

            direction = not direction

    return waypoints

# def generate_lawnmower_waypoints_irregular(boundary_gps, altitude_m):
#     # Reference point
#     ref_lat, ref_lon = boundary_gps[0]

#     # Convert boundary to XY
#     xy_points = [gps_to_xy(lat, lon, ref_lat, ref_lon) for lat, lon in boundary_gps]

#     xs = [p[0] for p in xy_points]
#     ys = [p[1] for p in xy_points]

#     min_x, max_x = min(xs), max(xs)
#     min_y, max_y = min(ys), max(ys)

#     # Step 2 parameters
#     swath, pass_spacing = calculate_pass_spacing(
#         altitude_m=altitude_m,
#         fov_deg=57,
#         overlap=0.25
#     )

#     waypoints = []
#     y = min_y
#     direction = True

#     while y <= max_y:
#         if direction:
#             start = (min_x, y)
#             end = (max_x, y)
#         else:
#             start = (max_x, y)
#             end = (min_x, y)

#         lat1, lon1 = xy_to_gps(start[0], start[1], ref_lat, ref_lon)
#         lat2, lon2 = xy_to_gps(end[0], end[1], ref_lat, ref_lon)

#         waypoints.append((lat1, lon1, altitude_m))
#         waypoints.append((lat2, lon2, altitude_m))

#         direction = not direction
#         y += pass_spacing

#     return waypoints
