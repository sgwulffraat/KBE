from problem_solution import Item
from shapely.geometry import Polygon
from circle import Circle
import numpy as np
n = 4
type = "_20A"
tol = 0.3

def connector_input_converter(type, n, tol):
    items = []
    if type[0:3] == "_20":
        if type[-1] == "A":
            d = 23.8 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "B":
            d = 26.2 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "C":
            d = 28.6 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "D":
            d = 31 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "E":
            d = 33.3 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "F":
            d = 36.5 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "G":
            d = 39.7 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "H":
            d = 42.9 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "J":
            d = 46 + 2 * tol
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
    elif type[0:3] == "_24":
        if type[-1] == "A":
            d = 30.2 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "B":
            d = 34.9 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "C":
            d = 38.1 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "D":
            d = 41.3 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "E":
            d = 44.5 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "F":
            d = 49.2 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "G":
            d = 52.4 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "H":
            d = 55.6 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "J":
            d = 58.7 + 2 * tol
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d), 1, 1)
    elif type == "EN2":
        l = 55.6 + 2 * tol
        w = 15.2 + 2 * tol
        area = l*w
        item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 1)
    elif type == "EN4":
        l = 86.1 + 2 * tol
        w = 15.2 + 2 * tol
        area = l*w
        item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 1)
    else:
        item = "Undefined item"
    for i in range(0,n):
        items.append(item)
    total_area = n*area
    return items, total_area

