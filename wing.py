from parapy.core import *

class Wing(Base):
    chord_root = Input(3.0)
    chord_tip = Input(1.0)
    span = Input(10.0)
    @Attribute
    def area(self):
        return (self.chord_root + self.chord_tip) * self.span * 0.5

    @Attribute
    def taper_ratio(self):
        return self.chord_tip/self.chord_root

    @Attribute
    def aspect_ratio(self):
        return self.span**2/self.area


if __name__ == '__main__':
    from parapy.gui import display
    obj = Wing()
    display(obj)
