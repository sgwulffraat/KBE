from parapy.core import *
from parapy.geom import *
del parapy.geom.occ.curve.Circle
from parapy.gui.manipulation import (
    EndEvent, ManipulableBase)
from parapy.gui.manipulation.modes import ALL_TRANSFORMATIONS

class Connector(GeomBase):
    type = Input()
    n = Input()

    @Attribute
    size


    @Part
    def rectangle_connector(self):
        return Box(width=self.width, length=self.length, height=self.height, centered=False,
                   hidden=False if self.shape == "rectangle" else True, label="Bracket")

    @Part
    def rectangle_connector(self):
        return Cylinder(radius=self.radius, height=self.height, centered=False,
                        hidden=False if self.shape == "circle" else True,
                        label=type)
