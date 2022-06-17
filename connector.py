from parapy.core import *
from parapy.geom import *
from connector_input_converter import connector_class_input_converter


class Connector(GeomBase):
    c_type = Input()
    df = Input()
    n = Input(1)
    height = Input(1)
    cog = Input([[0, 0, 0]])
    rotation = Input([0])
    color = Input([83, 120, 128])
    deg = Input(False)
    bracket_height = Input()

    @Attribute
    def dimensions(self):
        return connector_class_input_converter(self.c_type, self.df)

    @Attribute
    def shape(self):
        return self.dimensions[1]

    @Attribute
    def dim(self):
        return self.dimensions[0]

    @Part
    def square_connector(self):
        return Box(width=self.dim[0] if len(self.dim) == 2 else 0,
                   length=self.dim[0] if len(self.dim) == 2 else 0,
                   height=self.height,
                   centered=True,
                   hidden=False if self.shape == "square" else True,
                   label=self.c_type,
                   quantify=self.n,
                   position=rotate(
                                   translate(self.position,
                                             'x', self.cog[child.index][0],
                                             'y', self.cog[child.index][1],
                                             'z', self.bracket_height),
                                   'z', self.rotation[child.index],
                                   deg=self.deg),
                   color=self.color,
                   transparency=0.5)

    @Part
    def circular_connector(self):
        return Cylinder(radius=self.dim[0]/2 if len(self.dim) == 1 else 0,
                        height=self.height,
                        centered=False,
                        hidden=False if self.shape == "circle" else True,
                        label=self.c_type,
                        quantify=self.n,
                        position=rotate(
                            translate(self.position,
                                      'x', self.cog[child.index][0],
                                      'y', self.cog[child.index][1],
                                      'z', self.bracket_height),
                            'z', self.rotation[child.index],
                            deg=self.deg),
                        color=self.color,
                        transparency=0.5)

    @Part
    def rectangle_connector(self):
        return Box(width=self.dim[0] if len(self.dim) == 2 else 0,
                   length=self.dim[1] if len(self.dim) == 2 else 0,
                   height=self.height,
                   centered=True,
                   hidden=False if self.shape == "rectangle" else True,
                   label=self.c_type,
                   quantify=self.n,
                   position=rotate(
                       translate(self.position,
                                 'x', self.cog[child.index][0],
                                 'y', self.cog[child.index][1],
                                 'z', self.bracket_height),
                       'z', self.rotation[child.index],
                       deg=self.deg),
                   color=self.color,
                   transparency=0.5)
