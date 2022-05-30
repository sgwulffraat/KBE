from parapy.core import *
from parapy.geom import *
from parapy.exchange import *


class Variable_geom_bracket(GeomBase):
    @Attribute
    def pts(self):
        return [Point(0, 0, 0), Point(1, 2, 0), Point(6, 2, 0),
               Point(6, 4, 0), Point(8, 5, 0), Point(9, 1, 0),
               Point(7, 0, 0)]
    @Part
    def face1(self):
        return Face(island = Polygon(points = self.pts))

    @Part
    def face2(self):
        return Face(Polygon([Point(0, 0, 0), Point(-15, 15, 0), Point(-15, 45, 0),
               Point(30, 65, 0), Point(120, 65, 0), Point(140, 30, 0),
               Point(140, 25, 0), Point(50, 25, 0), Point(45, 0, 0)]))



    # @Part
    # def bracket(self):
    #     return Face()

    @Part
    def step(self):
        return STEPWriter(trees = self.face2)

if __name__ == '__main__':
    from parapy.gui import display
    obj = Variable_geom_bracket()
    display(obj)
