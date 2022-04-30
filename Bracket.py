from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.geom import *
from connector_input_converter import connector_input_converter
from parapy.exchange import *
#from ref_frame import Frame


class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle" , "file"]

    #Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectortypes = ["_20A", "_20B", "_20C", "_20D", "_20E", "_20F", "_20G", "_20H", "_20J", "_24A", "_24B", "_24C", "_24D", "_24E", "_24F", "_24G", "_24H", "_24J", "EN2", "EN4"]

    #Input block bracket generator
    bracketshape = Input("rectangle", widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular", "Create from file"]))
    file = Input(__file__, widget=FilePicker, validator=Optional)

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
            radius = 1
        else:
            radius = None
        return radius

    @Input
    def width(self):
        if self.bracketshape == "rectangle":
            width = 1
        else:
            width = None
        return width

    @Input
    def length(self):
        if self.bracketshape == "rectangle":
            length = 1
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
        container =
        items1 = connector_input_converter(self.type1, self.n1, self.tol)
        items2 = connector_input_converter(self.type2, self.n2, self.tol)
        items3 = connector_input_converter(self.type3, self.n3, self.tol)
        items4 = connector_input_converter(self.type4, self.n4, self.tol)
        input.append(items1[0:-1])
        input.append(items2[0:-1])
        input.append(items3[0:-1])
        input.append(items4[0:-1])
        return input

    # @Part
    # def bracket_shape(self):
    #     if self.shape == "rectangle":
    #         return RectangularSurface(width=2.0, length=1.0)



    # if bracketshape == "square":
    #     @Part
    #     def bracket(self):
    #         return Box(width=self.width, length=self.width, height=self.height)
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif shape == "rectangle":
    #     @Part
    #     def bracket(self):
    #         return Box(width=self.width, length=self.length, height=self.height)
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif shape == "circle":
    #     @Part
    #     def bracket(self):
    #         return Cylinder(radius=self.radius, height=self.height,
    #                         position=translate(rotate(self.position, 'x', 45), 'x', 250, 'y', 100, 'z', -300, ))
    #
    #     @Part
    #     def reference_frame(self):
    #         return Frame(pos=Position(location=getattr(self.bracket, 'cog'),
    #                                   orientation=getattr(self.bracket, 'orientation')))
    # elif shape == "file":
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

    # @Part
    # def step(self):
    #     return STEPWriter(trees=self.bracket)

if __name__ == '__main__':
    from parapy.gui import display

    obj = Bracket()
    display([obj])

