from parapy.core import *
from parapy.geom import Box, Cylinder, translate, rotate, GeomBase
from connector_input_converter import connector_class_input_converter


class Connector(GeomBase):
    c_type = Input()                # Type connector
    df = Input()                    # Connector information data frame
    n = Input(1)                    # Number of connectors
    cog = Input([[0, 0, 0]])        # Centre of gravity
    color = Input([83, 120, 128])
    deg = Input(False)
    bracket_height = Input(1)

    @Input
    def rotation(self):
        rotation = [0]*self.n
        return rotation

    @Input
    def height(self):
        height = 10
        if height < 2*self.bracket_height:
            height = 2*self.bracket_height
        else:
            height = height
        return height

    @Attribute
    def dimensions(self):
        "Function to retrieve both shape and dimensions"
        return connector_class_input_converter(self.c_type, self.df)

    @Attribute
    def shape(self):
        """shape of connector"""
        return self.dimensions[1]

    @Attribute
    def dim(self):
        """Dimensions in [width,length] or [radius,radius]"""
        return self.dimensions[0]

    @Part
    def circular_connector(self):
        return MutableSequence(type=Cylinder, radius=self.dim[0]/2,
                               height=self.height,
                               centered=False,
                               hidden=False if self.shape == "circle" else True,
                               label=self.c_type,
                               quantify=self.n,
                               position=translate(self.position,
                                                   'x', self.cog[child.index][0],
                                                   'y', self.cog[child.index][1],
                                                   'z', 0),
                               color=self.color,
                               transparency=0.5)

    @Part
    def rectangle_connector(self):
        return MutableSequence(type=Box, width=self.dim[0],
                               length=self.dim[1],
                               height=self.height,
                               centered=True,
                               hidden=False if self.shape == "rectangle" or self.shape == "square" else True,
                               label=self.c_type,
                               quantify=self.n,
                               position=rotate(translate(self.position,
                                                         'x', self.cog[child.index][0],
                                                         'y', self.cog[child.index][1],
                                                         'z', self.height/2),
                                                'z',self.rotation[child.index],
                                                deg=True),
                               color=self.color,
                               transparency=0.5)

