from parapy.core import *
from parapy.geom import *
from parapy.core.widgets import Dropdown
from connector_input_converter import connector_class_input_converter
del parapy.geom.occ.curve.Circle

class Connector(GeomBase):
    connectorlabels = Input()
    type = Input("MIL/20-A", label="Type Connector", widget=Dropdown(connectorlabels))

    @Attribute
    def connector_labels(self):
        return self.connectorlabels

    @Attribute
    def dimensions(self):
        shape,size = connector_class_input_converter(self.type, self.tol, self.df)
        return shape, size

    @Part
    def square_connector(self):
        return Box(width=self.size[0] if len(size) == 2 else 0, length=self.size[0] if len(self.size) == 2 else 0,
                   height=self.height, centered=False, hidden=False if self.shape == "square" else True,
                   label=self.type)

    @Part
    def circular_connector(self):
        return Cylinder(radius=self.size[0] if len(self.size) == 1 else 0, height=self.height, centered=False,
                        hidden=False if self.shape == "circle" else True, label=self.type)

    @Part
    def rectangle_connector(self):
        return Box(width=self.size[1] if len(self.size) == 2 else 0, length=self.size[0] if len(self.size) == 2 else 0,
                   height=self.height, centered=False, hidden=False if self.shape == "rectangle" else True,
                   label=self.type)
