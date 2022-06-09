import numpy as np
import random

from shapely.geometry import Polygon, Point


#poly = Polygon([(23.789642, 90.354714), (23.789603, 90.403000), (23.767688, 90.403597),(23.766510, 90.355448)])

def random_points_within(poly,poly2, num_points):
    poly=Polygon(poly)
    min_x, min_y, max_x, max_y = poly.bounds
    poly2=Polygon(poly2)
    points = []

    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if random_point.within(poly2):
            if random_point.within(poly):
                points.append(random_point)

    return points

def check_within(Point1,poly):
    poly=Polygon(poly)
    return Point1.within(poly)
