from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.gui import display
from parapy.geom import *

class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    options = ["rectangle", "circle" , "file"]
    shape = Input("rectangle", widget=Dropdown(options, labels=["Rectangular", "Circular", "Create from file"]))
    file = Input(derived, widget=FilePicker, validator=Optional)
    if shape == "rectangle":
        width2 = Input(1)

    @Input
    def radius(self):
        if self.shape == "circle":
            radius = 1
        else:
            radius = None
        return radius

    @Input
    def width(self):
        if self.shape == "rectangle":
            width = 1
        else:
            width = None
        return width

    @Input
    def length(self):
        if self.shape == "rectangle":
            length = 1
        else:
            length = None
        return length

    @file.getter
    def file(self):
        if self.shape == "file":
            file = __file__
        else:
            file = None
        return file


    #@Attribute
    #coords = optimize()

    # @Part
    # def bracket_shape(self):
    #     if self.shape == "rectangle":
    #         return RectangularSurface(width=2.0, length=1.0)

    #Connector input

test = Bracket()
display(test)