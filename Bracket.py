from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.geom import *
from connector_input_converter import connector_input_converter
from parapy.exchange import *
from ref_frame import Frame
from shapely.geometry import Polygon, Point
from circle import Circle



class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle" , "file"]

    #Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectortypes = ["_20A", "_20B", "_20C", "_20D", "_20E", "_20F", "_20G", "_20H", "_20J", "_24A", "_24B", "_24C", "_24D", "_24E", "_24F", "_24G", "_24H", "_24J", "EN2", "EN4"]

    #Input block bracket generator
    bracketshape = Input("rectangle", widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular", "Create from file"]))
    filename = Input(__file__, widget=FilePicker)
    height = Input(1)
    #Widget section connector type selection
    #ADD VALIDATORS
    type1 = Input("_20A", label="Type Connector", widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B", "MIL/20-C", "MIL/20-D", "MIL/20-E", "MIL/20-F", "MIL/20-G", "MIL/20-H", "MIL/20-J", "MIL/24-A", "MIL/24-B", "MIL/24-C", "MIL/24-D", "MIL/24-E", "MIL/24-F", "MIL/24-G", "MIL/24-H", "MIL/24-J", "EN/2", "EN/4"]))
    n1 = Input(0, label="Number of this type")
    type2 = Input("_20A", label="Type Connector", widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B", "MIL/20-C", "MIL/20-D", "MIL/20-E", "MIL/20-F", "MIL/20-G", "MIL/20-H", "MIL/20-J", "MIL/24-A", "MIL/24-B", "MIL/24-C", "MIL/24-D", "MIL/24-E", "MIL/24-F", "MIL/24-G", "MIL/24-H", "MIL/24-J", "EN/2", "EN/4"]))
    n2 = Input(0, label="Number of this type")
    type3 = Input("_20A", label="Type Connector", widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B", "MIL/20-C", "MIL/20-D", "MIL/20-E", "MIL/20-F", "MIL/20-G", "MIL/20-H", "MIL/20-J", "MIL/24-A", "MIL/24-B", "MIL/24-C", "MIL/24-D", "MIL/24-E", "MIL/24-F", "MIL/24-G", "MIL/24-H", "MIL/24-J", "EN/2", "EN/4"]))
    n3 = Input(0, label="Number of this type")
    type4 = Input("_20A", label="Type Connector", widget=Dropdown(connectortypes,labels=["MIL/20-A", "MIL/20-B", "MIL/20-C", "MIL/20-D", "MIL/20-E", "MIL/20-F", "MIL/20-G", "MIL/20-H", "MIL/20-J", "MIL/24-A", "MIL/24-B", "MIL/24-C", "MIL/24-D", "MIL/24-E", "MIL/24-F", "MIL/24-G", "MIL/24-H", "MIL/24-J", "EN/2", "EN/4"]))
    n4 = Input(0, label="Number of this type")
    tol = Input(0.3, label="Tolerance")

    @Input
    def radius(self):
        if self.bracketshape == "circle":
            radius = 5
        else:
            radius = None
        return radius

    @Input
    def width(self):
        if self.bracketshape == "rectangle":
            width = 10
        else:
            width = None
        return width

    @Input
    def length(self):
        if self.bracketshape == "rectangle":
            length = 10
        else:
            length = None
        return length

    # @file.getter
    # def file(self):
    #     if self.bracketshape == "file":
    #         file = __file__
    #     else:
    #         file = None
    #     return file


    @Attribute
    def optimize_items(self):
        input = []
        # container =
        items1 = connector_input_converter(self.type1, self.n1, self.tol)
        items2 = connector_input_converter(self.type2, self.n2, self.tol)
        items3 = connector_input_converter(self.type3, self.n3, self.tol)
        items4 = connector_input_converter(self.type4, self.n4, self.tol)
        input.append(items1[0:-1])
        input.append(items2[0:-1])
        input.append(items3[0:-1])
        input.append(items4[0:-1])
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
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x, self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            print(points)
            container = Polygon(points)
        return container

    @Part
    def bracket_box(self):
        return Box(width=self.width, length=self.length, height=self.height, centered = True , hidden = False if self.bracketshape == "rectangle" else True, label = "Bracket")

    @Part
    def bracket_cylinder(self):
        return Cylinder(radius=self.radius, height=self.height, centered = True, hidden = False if self.bracketshape == "circle" else True, label = "Bracket")

    @Part
    def bracket_from_file(self):
        return STEPReader(filename=self.filename, hidden = False if self.bracketshape == "file" else True, label = "Bracket")

    # if bracketshape == "square":
    #     @Part
    #     def bracket(self):
    #         return Box(width=self.width, length=self.width, height=self.height)
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif bracketshape == "rectangle":
    #     @Part
    #     def bracket(self):
    #         return Box(width=self.width, length=self.length, height=self.height)
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif bracketshape == "circle":
    #     @Part
    #     def bracket(self):
    #         return Cylinder(radius=self.radius, height=self.height,
    #                         position=translate(rotate(self.position, 'x', 45), 'x', 250, 'y', 100, 'z', -300, ))
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif bracketshape == "file":
    #     @Part
    #     def bracket(self):
    #         return STEPReader(filename=self.filename)
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket.children[0].children[0].children[0], 'cog'),
    #                                   orientation=getattr(self.bracket.children[0].children[0].children[0],
    #                                                       'orientation')))
    # else:
    #     print("WARNING: Geometry was not defined!")

    @Part
    def step(self):
        return STEPWriter(trees=self.bracket_test)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Bracket()
    display([obj])

