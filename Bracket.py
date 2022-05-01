from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.geom import *
from connector_input_converter import connector_input_converter
from parapy.exchange import *
from shapely.geometry import Polygon
from circle import Circle
import numpy as np
import warnings



class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle" , "file"]

    #Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectortypes = ["_20A", "_20B", "_20C", "_20D", "_20E", "_20F", "_20G",
                      "_20H", "_20J", "_24A", "_24B", "_24C", "_24D", "_24E",
                      "_24F", "_24G", "_24H", "_24J", "EN2", "EN4"]

    #Input block bracket generator
    bracketshape = Input("rectangle",
                         widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular",
                                                               "Create from file"]))
    filename = Input(__file__, widget=FilePicker)
    #Widget section connector type selection
    type1 = Input("_20A", label="Type Connector",
                  widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B",
                                                         "MIL/20-C", "MIL/20-D", "MIL/20-E",
                                                         "MIL/20-F", "MIL/20-G", "MIL/20-H",
                                                         "MIL/20-J", "MIL/24-A", "MIL/24-B",
                                                         "MIL/24-C", "MIL/24-D", "MIL/24-E",
                                                         "MIL/24-F", "MIL/24-G", "MIL/24-H",
                                                         "MIL/24-J", "EN/2", "EN/4"]))
    n1 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type2 = Input("_20B", label="Type Connector",
                  widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B",
                                                         "MIL/20-C", "MIL/20-D", "MIL/20-E",
                                                         "MIL/20-F", "MIL/20-G", "MIL/20-H",
                                                         "MIL/20-J", "MIL/24-A", "MIL/24-B",
                                                         "MIL/24-C", "MIL/24-D", "MIL/24-E",
                                                         "MIL/24-F", "MIL/24-G", "MIL/24-H",
                                                         "MIL/24-J", "EN/2", "EN/4"]))
    n2 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type3 = Input("_20C", label="Type Connector",
                  widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B",
                                                         "MIL/20-C", "MIL/20-D", "MIL/20-E",
                                                         "MIL/20-F", "MIL/20-G", "MIL/20-H",
                                                         "MIL/20-J", "MIL/24-A", "MIL/24-B",
                                                         "MIL/24-C", "MIL/24-D", "MIL/24-E",
                                                         "MIL/24-F", "MIL/24-G", "MIL/24-H",
                                                         "MIL/24-J", "EN/2", "EN/4"]))
    n3 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type4 = Input("_20D", label="Type Connector",
                  widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B",
                                                         "MIL/20-C", "MIL/20-D", "MIL/20-E",
                                                         "MIL/20-F", "MIL/20-G", "MIL/20-H",
                                                         "MIL/20-J", "MIL/24-A", "MIL/24-B",
                                                         "MIL/24-C", "MIL/24-D", "MIL/24-E",
                                                         "MIL/24-F", "MIL/24-G", "MIL/24-H",
                                                         "MIL/24-J", "EN/2", "EN/4"]))
    n4 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))

    #Specify tolerance between connectors
    tol = Input(0.3, label="Tolerance", validator=Positive(incl_zero=True))

    #height or thickness of the to be designed bracket
    height = Input(1, validator=Positive(incl_zero=True))
    popup_gui = Input(True)

    @Input
    def radius(self):
        if self.bracketshape == "circle":
            radius = 100
        else:
            radius = None
        return radius

    @Input
    def width(self):
        if self.bracketshape == "rectangle":
            width = 100
        else:
            width = None
        return width

    @Input
    def length(self):
        if self.bracketshape == "rectangle":
            length = 100
        else:
            length = None
        return length

    @Attribute
    def bracket_area(self):
        if self.bracketshape == "rectangle":
            bracket_area = self.width * self.length
        if self.bracketshape == "circle":
            bracket_area = np.pi * self.radius**2
        if self.bracketshape == "file":
            bracket_area = self.bracket_from_file.children[0].children[0].children[0].area
        return bracket_area

    @Attribute
    def optimize_items(self):
        input = []
        # container =
        items1, area1 = connector_input_converter(self.type1, self.n1, self.tol)
        items2, area2 = connector_input_converter(self.type2, self.n2, self.tol)
        items3, area3 = connector_input_converter(self.type3, self.n3, self.tol)
        items4, area4 = connector_input_converter(self.type4, self.n4, self.tol)
        if area1 + area2 + area3 + area4 > self.bracket_area:
            msg = "Combined connector area larger than bracket area, impossible " \
                  "to fit all connectors. Try using less or smaller connectors"
            warnings.warn(msg)
            if self.popup_gui:
                generate_warning("Warning: Value changed", msg)
        input = items1 + items2 + items3 + items4
        return input

    @Attribute
    def optimize_container(self):
        if self.bracketshape == "rectangle":
            container = Polygon([(0.0, 0), (self.length, 0.0), (self.length, self.width), (0.0, self.width)])
        if self.bracketshape == "circle":
            container = Circle((0, 0), self.radius)
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[0].edges)):
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            print(points)
            container = Polygon(points)
        return container

    @Part
    def bracket_box(self):
        return Box(width=self.width, length=self.length, height=self.height, centered = False ,
                   hidden = False if self.bracketshape == "rectangle" else True, label = "Bracket")

    @Part
    def bracket_cylinder(self):
        return Cylinder(radius=self.radius, height=self.height, centered = False,
                        hidden = False if self.bracketshape == "circle" else True,
                        label = "Bracket")

    @Part
    def bracket_from_file(self):
        return STEPReader(filename=self.filename,
                          hidden = False if self.bracketshape == "file" else True, label = "Bracket")

    @Part
    def step(self):
        return STEPWriter(trees=self.bracket_test)

def generate_warning(warning_header, msg):
    """
    This function generates the warning dialog box
    :param warning_header: The text to be shown on the dialog box header
    :param msg: the message to be shown in dialog box
    :return: None as it is GUI operation
    """
    from tkinter import Tk, messagebox

    # initialization
    window = Tk()
    window.withdraw()

    # generates message box
    messagebox.showwarning(warning_header, msg)

    # kills the gui
    window.deiconify()
    window.destroy()
    window.quit()

if __name__ == '__main__':
    from parapy.gui import display

    obj = Bracket()
    display([obj])