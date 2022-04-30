from shapely.geometry import Polygon, MultiPolygon, Point
from circle import Circle

def container_input_converter(bracketshape, width, length, radius):
    if bracketshape == "rectangle":
        container = Polygon([(0.0, 0), (length, 0.0), (length, width), (0.0, width)])
    if bracketshape ==