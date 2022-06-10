from source.problem_solution import Item
from shapely.geometry import Polygon
from source.circle import Circle
import numpy as np
import pandas as pd

def read_connector_excel(filename, sheetname, sheetname2):
    xls = pd.ExcelFile(filename)
    df = pd.read_excel(xls, sheetname)
    df2 = pd.read_excel(xls, sheetname2)
    options = []
    for i in range(0,len(df["Document ID"])):
        if df["Document ID"].iloc[i][0:3] == "MIL":
            options.append(df["Document ID"].iloc[i][0:3] + df["Document ID"].iloc[i][-3:-1] +
                  df["Document ID"].iloc[i][-1] + "-" + df["Shell size"].iloc[i])
        elif df["Document ID"].iloc[i][0:2] == "EN":
            options.append(df["Document ID"].iloc[i][0:2]  + "-" + df["Shell size"].iloc[i][0])
    return options, df, df2


def connector_input_converter(type, n, tol, df, df2):
    items = []
    if type[0:3] == "MIL":
        if type[4:6] == '20':
            d = df["Dimension"][df.index[df["Shell size"] == type[-1]][0]] + 2 * tol
            size = [d]
            area = d**2
            item = Item(Polygon([(0.0, 0.0), (d, 0.0), (d, d), (0, d)]), 1, 100/df2["Area / contact"][df.index[df["Shell size"] == type[-1]][0]])
        if type[4:6] == '24':
            d = df["Dimension"][df.index[df["Shell size"] == type[-1]][1]] + 2 * tol
            size = [d, d]
            area = np.pi * (d / 2) ** 2
            item = Item(Circle((0, 0), d/2), 1, 100/df2["Area / contact"][df.index[df["Shell size"] == type[-1]][1]])
    elif type[0:2] == "EN":
        if type[-1] == '2':
            l = 55.6 + 2 * tol
            w = 15.2 + 2 * tol
            size = [l, w]
            area = l * w
            item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 100/df2["Area / contact"][df.index[df["Shell size"] == str(type[-1]+" module")][0]])
        if type[-1] == '4':
            l = 86.1 + 2 * tol
            w = 15.2 + 2 * tol
            size = [l, w]
            area = l * w
            item = Item(Polygon([(0.0, 0.0), (l, 0.0), (l, w), (0, w)]), 1, 100/df2["Area / contact"][df.index[df["Shell size"] == str(type[-1]+" module")][0]])
    else:
        item = "Undefined item"
        size = []
    for i in range(0,n):
        items.append(item)
    total_area = n*area
    return items, total_area

def connector_class_input_converter(type, df):
    if type[0:3] == "MIL":
        if type[4:6] == '20':
            d = df["Dimension"][df.index[df["Shell size"] == type[-1]][0]]
            size = [d, d]
            shape = 'square'
        if type[4:6] == '24':
            d = df["Dimension"][df.index[df["Shell size"] == type[-1]][1]]
            size = [d]
            shape = 'circle'
    elif type[0:2] == "EN":
        shape = 'rectangle'
        if type[-1] == '2':
            l = 55.6
            w = 15.2
            size = [l, w]
        if type[-1] == '4':
            l = 86.1
            w = 15.2
            size = [l, w]
    else:
        size = []
        shape = 'Undefined item'
    return size, shape