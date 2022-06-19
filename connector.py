from parapy.core import *
from parapy.geom import Box, Cylinder, translate, rotate, GeomBase
from shapely.geometry import Polygon
from connector_input_converter import connector_class_input_converter


class Connector(GeomBase):
    c_type = Input()
    df = Input()
    n = Input(1)
    cog = Input([[0, 0, 0]])
    rotation = Input([0])
    color = Input([83, 120, 128])
    deg = Input(False)
    bracket_height = Input(1)
    bracket = Input()
    lastplaced_item = Input()
    tol = Input()
    poly_container = Input()

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
        return connector_class_input_converter(self.c_type, self.df)

    @Attribute
    def shape(self):
        return self.dimensions[1]

    @Attribute
    def dim(self):
        return self.dimensions[0]

    # @Part
    # def square_connector(self):
    #     return Box(width=self.dim[0] if len(self.dim) == 2 else 0,
    #                length=self.dim[0] if len(self.dim) == 2 else 0,
    #                height=self.height,
    #                centered=True,
    #                hidden=False if self.shape == "square" else True,
    #                label=self.c_type,
    #                quantify=self.n,
    #                position=rotate(
    #                                translate(self.position,
    #                                          'x', self.cog[child.index][0],
    #                                          'y', self.cog[child.index][1],
    #                                          'z', self.bracket_height),
    #                                'z', self.rotation[child.index],
    #                                deg=self.deg),
    #                color=self.color,
    #                transparency=0.5)
    #
    # @Part
    # def circular_connector(self):
    #     return Cylinder(radius=self.dim[0]/2 if len(self.dim) == 1 else 0,
    #                     height=self.height,
    #                     centered=False,
    #                     hidden=False if self.shape == "circle" else True,
    #                     label=self.c_type,
    #                     quantify=self.n,
    #                     position=rotate(
    #                         translate(self.position,
    #                                   'x', self.cog[child.index][0],
    #                                   'y', self.cog[child.index][1],
    #                                   'z', self.bracket_height),
    #                         'z', self.rotation[child.index],
    #                         deg=self.deg),
    #                     color=self.color,
    #                     transparency=0.5)
    #
    # @Part
    # def rectangle_connector(self):
    #     return Box(width=self.dim[0] if len(self.dim) == 2 else 0,
    #                length=self.dim[1] if len(self.dim) == 2 else 0,
    #                height=self.height,
    #                centered=True,
    #                hidden=False if self.shape == "rectangle" else True,
    #                label=self.c_type,
    #                quantify=self.n,
    #                position=rotate(
    #                    translate(self.position,
    #                              'x', self.cog[child.index][0],
    #                              'y', self.cog[child.index][1],
    #                              'z', self.bracket_height),
    #                    'z', self.rotation[child.index],
    #                    deg=self.deg),
    #                color=self.color,
    #                transparency=0.5)

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
                                               'z', self.rotation[child.index],
                                               deg=True),
                               color=self.color,
                               transparency=0.5)

    def initial_item_placement(self, bracket, lastplaced_item, half_width, half_length, step):
        if bracket.__class__ == Cylinder:
            bracket_max_x = 2 * bracket.radius
            bracket_max_y = 2 * bracket.radius
        elif bracket.__class__ == Box:
            bracket_max_x = bracket.width
            bracket_max_y = bracket.length
        else:
            bracket_max_x = 2 * bracket.radius
            bracket_max_y = 2 * bracket.radius
        if lastplaced_item != "None":
            last_items = lastplaced_item.find_children(fn=lambda conn: conn.__class__ == Box
                                                                       or conn.__class__ == Cylinder)
            start_position_x = last_items[-1].cog[0]
            start_position_y = last_items[-1].cog[1]
            if last_items[-1].__class__ == Cylinder:
                previous_half_width = last_items[-1].radius
                previous_half_length = last_items[-1].radius
            else:
                previous_half_width = last_items[-1].width / 2
                previous_half_length = last_items[-1].length / 2
        else:
            start_position_x = half_width + self.tol
            start_position_y = half_length + self.tol
            previous_half_length = 0
            previous_half_width = 0
        for j in range(0, round((bracket_max_y
                                 - (start_position_y + previous_half_length + self.tol)) / half_length) + 1):
            if j == 0:
                if previous_half_length == 0:
                    position = [start_position_x, start_position_y]
                else:
                    if start_position_y < half_length + self.tol:
                        position = [start_position_x + half_width + previous_half_width + self.tol, half_length + self.tol]
                    else:
                        position = [start_position_x + half_width + previous_half_width + self.tol, start_position_y]
            else:
                if previous_half_length == 0:
                    position = [start_position_x, start_position_y + j * half_length]
                else:
                    position = [half_width + self.tol, start_position_y + previous_half_length + self.tol + j * half_length]
            while position[0] < bracket_max_x:
                position[0] = position[0] + step
                pol_connector = Polygon([(position[0] + (half_width + self.tol),
                                          position[1] + (half_length + self.tol)),
                                         (position[0] + (half_width + self.tol),
                                          position[1] - (half_length + self.tol)),
                                         (position[0] - (half_width + self.tol),
                                          position[1] - (half_length + self.tol)),
                                         (position[0] - (half_width + self.tol),
                                          position[1] + (half_length + self.tol))
                                         ])
                if self.poly_container.contains(pol_connector) is True:
                    new_position = translate(self.position, 'x', position[0], 'y', position[1], 'z', self.height)
                    return new_position
        else:
            new_position = translate(self.position, 'x', bracket_max_x/2, 'y', bracket_max_y/2, 'z', self.height)
            return new_position