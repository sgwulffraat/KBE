from parapy.core import *
from parapy.geom import *
from connector_input_converter import connector_class_input_converter

class Connector(GeomBase):
    c_type = Input()
    tol = Input()
    df = Input ()
    shape_size = connector_class_input_converter(c_type, tol, df)

    @Attribute
    def shape(self):
        return self._shape

    @Attribute
    def size(self):
        return self._size

    @Part
    def square_connector(self):
        return Box(width=self.size[0] if len(self.size) == 2 else 0,
                   length=self.size[0] if len(self.size) == 2 else 0,
                   height=self.height,
                   centered=False,
                   hidden=False if self.shape == "square" else True,
                   label=self.c_type)

    @Part
    def circular_connector(self):
        return Cylinder(radius=self.size[0] if len(self.size) == 1 else 0,
                        height=self.height,
                        centered=False,
                        hidden=False if self.shape == "circle" else True,
                        label=self.c_type)

    @Part
    def rectangle_connector(self):
        return Box(width=self.size[1] if len(self.size) == 2 else 0,
                   length=self.size[0] if len(self.size) == 2 else 0,
                   height=self.height,
                   centered=False,
                   hidden=False if self.shape == "rectangle" else True,
                   label=self.c_type)
