from problem_solution import Item
from shapely.geometry import Polygon
from circle import Circle
n = 4
type = "_20A"
tol = 0.3

def connector_input_converter(type, n, tol):
    items = []
    if type[0:3] == "_20":
        if type[-1] == "A":
            d = 23.8 + 2*tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "B":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "C":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "D":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "E":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "F":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "G":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "H":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
        if type[-1] == "J":
            d = 23.8 + 2 * tol
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 1)
    elif type[0:3] == "_24":
        if type[-1] == "A":
            d = 30.2 + 2*tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "B":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "C":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "D":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "E":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "F":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "G":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "H":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
        if type[-1] == "J":
            d = 30.2 + 2 * tol
            item = Item(Circle((0, 0), d), 1, 1)
    elif type == "EN2":
        l = 55.6 + 2 * tol
        w = 15.2 + 2 * tol
        item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 1)
    elif type == "EN4":
        l = 86.1 + 2 * tol
        w = 15.2 + 2 * tol
        item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 1)
    else:
        item = "Undefined item"
    for i in range(0,n):
        items.append(item)
    return items

input = connector_input_converter(type, n, tol)
print(input)