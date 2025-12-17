import math

R = 6378137  # Earth radius (meters)

def gps_to_xy(lat, lon, ref_lat, ref_lon):
    x = math.radians(lon - ref_lon) * R * math.cos(math.radians(ref_lat))
    y = math.radians(lat - ref_lat) * R
    return x, y

def xy_to_gps(x, y, ref_lat, ref_lon):
    lat = ref_lat + math.degrees(y / R)
    lon = ref_lon + math.degrees(x / (R * math.cos(math.radians(ref_lat))))
    return lat, lon
