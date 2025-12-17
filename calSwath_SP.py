import math
def calculate_pass_spacing(altitude_m, fov_deg, overlap=0.25):
    swath = 2 * altitude_m * math.tan(math.radians(fov_deg / 2))
    spacing = swath * (1 - overlap)
    return swath, spacing
