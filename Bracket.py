from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.geom import *
del parapy.geom.occ.curve.Circle
from connector_input_converter import connector_input_converter, read_connector_excel
from parapy.exchange import *
from shapely.geometry import Polygon, Point
from circle import Circle
from parapy.geom import TextLabel, Leader

#add no input warning
#annotation
#site


class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle" , "file"]

    #Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectorlabels, df, df2 = read_connector_excel('Connector details.xlsx', 'Connector details', 'Cavity specific area')

    #Input block bracket generator
    bracketshape = Input("rectangle",
                         widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular",
                                                               "Create from file"]))
    filename = Input(__file__, widget=FilePicker)

    #Widget section connector type selection
    type1 = Input("MIL/20-A", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n1 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type2 = Input("MIL/24-A", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n2 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type3 = Input("EN-2", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n3 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))
    type4 = Input("EN-4", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n4 = Input(0, label="Number of this type", validator=Positive(incl_zero=True))

    #Specify tolerance between connectors
    tol = Input(0.3, label="Tolerance", validator=Positive(incl_zero=True))

    #height or thickness of the to be designed bracket
    height = Input(1, validator=Positive(incl_zero=True), label="Thickness of bracket")

    #Allow pop up
    popup_gui = Input(True, label= "Allow pop-up")

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
        items1, area1 = connector_input_converter(self.type1, self.n1, self.tol, self.df, self.df2)
        items2, area2 = connector_input_converter(self.type2, self.n2, self.tol, self.df, self.df2)
        items3, area3 = connector_input_converter(self.type3, self.n3, self.tol, self.df, self.df2)
        items4, area4 = connector_input_converter(self.type4, self.n4, self.tol, self.df, self.df2)
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

    @Part
    def labels(self):
        return TextLabel(text="Bracket",
                         position=self.bracket_box.cog,
                         overlay=True)


def generate_warning(warning_header, msg):

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