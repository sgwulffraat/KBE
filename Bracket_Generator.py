from shapely.geometry import polygon
from parapy.geom import *
from parapy.core import *
from parapy.exchange import *
from ref_frame import Frame

class Bracket(GeomBase):
    filename = "rotated_translated_circle.stp"
    shape = "from file"
    height = 5
    width = 250
    length = 500
    radius = 400

    if shape == "square":
        @Part
        def bracket(self):
            return Box(width=self.width,length=self.width,height=self.height)

        @Part
        def reference_frame(self):
            return Frame(pos=Position(location=getattr(self.bracket,'cog'),
                                      orientation=getattr(self.bracket,'orientation')))
    elif shape == "rectangle":
        @Part
        def bracket(self):
            return Box(width=self.width,length=self.length,height=self.height)

        @Part
        def reference_frame(self):
            return Frame(pos=Position(location=getattr(self.bracket,'cog'),
                                      orientation=getattr(self.bracket,'orientation')))
    elif shape == "circle":
        @Part
        def bracket(self):
            return Cylinder(radius = self.radius,height = self.height,position=translate(rotate(self.position,'x',45),'x',250,'y',100,'z',-300,))

        @Part
        def reference_frame(self):
            return Frame(pos=Position(location=getattr(self.bracket,'cog'),
                                      orientation=getattr(self.bracket,'orientation')))
    elif shape == "from file":
        @Part
        def bracket(self):
            return STEPReader(filename=self.filename)

        @Part
        def reference_frame(self):
            return Frame(pos=Position(location=getattr(self.bracket.children[0].children[0].children[0], 'cog'),
                                      orientation=getattr(self.bracket.children[0].children[0].children[0],'orientation')))
    else:
        print("WARNING: Geometry was not defined!")

    @Part
    def step(self):
        return STEPWriter(trees = self.bracket)





if __name__ == '__main__':
    from parapy.gui import display

    obj = Bracket()
    display([obj])
