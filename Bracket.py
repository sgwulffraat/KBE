from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.gui import display
from parapy.geom import *

class Bracket(GeomBase):
    #Shape input: rectangle, circle or file
    options = ["rectangle", "circle" , "file"]
    shape = Input("rectangle", widget=Dropdown(options, labels=["Rectangular", "Circular", "Create from file"]))
    file = Input(__file__, widget=FilePicker)

    @Part
    def bracket_shape(self):
        if self.shape == "rectangle":
            geom = RectangularSurface(width=2.0, length=1.0)
        if self.shape == "circle":
            geom =  CircularFace(radius=1.0)
        if self.shape == "file":
            geom =  self.file
        return geom

    #Connector input

test = Bracket()
display(test)