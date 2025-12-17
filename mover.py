from GPS_to_XY import gps_to_xy,xy_to_gps
from calSwath_SP import calculate_pass_spacing

def generate_lawnmower_waypoints_irregular(boundary_gps, altitude_m):
    # Reference point
    ref_lat, ref_lon = boundary_gps[0]

    # Convert boundary to XY
    xy_points = [gps_to_xy(lat, lon, ref_lat, ref_lon) for lat, lon in boundary_gps]

    xs = [p[0] for p in xy_points]
    ys = [p[1] for p in xy_points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Step 2 parameters
    swath, pass_spacing = calculate_pass_spacing(
        altitude_m=altitude_m,
        fov_deg=57,
        overlap=0.25
    )

    waypoints = []
    y = min_y
    direction = True

    while y <= max_y:
        if direction:
            start = (min_x, y)
            end = (max_x, y)
        else:
            start = (max_x, y)
            end = (min_x, y)

        lat1, lon1 = xy_to_gps(start[0], start[1], ref_lat, ref_lon)
        lat2, lon2 = xy_to_gps(end[0], end[1], ref_lat, ref_lon)

        waypoints.append((lat1, lon1, altitude_m))
        waypoints.append((lat2, lon2, altitude_m))

        direction = not direction
        y += pass_spacing

    return waypoints
