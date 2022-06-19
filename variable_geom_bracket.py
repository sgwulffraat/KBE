from parapy.core import *
from parapy.geom import *
from parapy.exchange import *


class Variable_geom_bracket(GeomBase):
    @Attribute
    def pts(self):
        return [Point(40, 0, 0), Point(0, 40, 0), Point(0, 160, 0), Point(40, 200, 0),
               Point(200, 200, 0), Point(240, 160, 0), Point(260, 120, 0),
               Point(300, 120, 0), Point(300, 30, 0), Point(240, 0, 0)]

    @Attribute
    def wire_maker(self):
        line_segments = []
        for i in range(len(self.pts)-1):
            line_segments.append(LineSegment(self.pts[i], self.pts[i+1]))
        line_segments.append(LineSegment(self.pts[-1], self.pts[0]))
        return line_segments

    @Part
    def wire(self):
        return Wire(curves_in=self.wire_maker, line_thickness=2)

    @Part
    def extruded_sld(self):
        return ExtrudedSolid(island=self.wire, distance=1, direction=(0, 0, 1))

    @Part
    def face2(self):
        return Face(Polygon([Point(0, 0, 0), Point(-15, 15, 0), Point(-15, 45, 0),
               Point(30, 65, 0), Point(120, 65, 0), Point(140, 30, 0),
               Point(140, 25, 0), Point(50, 25, 0), Point(45, 0, 0)]))

    @Part
    def step(self):
        return STEPWriter(trees=[self])

if __name__ == '__main__':
    from parapy.gui import display
    obj = Variable_geom_bracket()
    display(obj)
