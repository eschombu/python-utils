import numpy as np


def haversine(lat1, lng1, lat2, lng2):
    R_earth = 6371009  # meters, avg
    h = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lng2 - lng1) / 2) ** 2
    return 2 * R_earth * np.arcsin(np.sqrt(h))