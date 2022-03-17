from parapy.core import *
from wing import Wing

class Aircraft(Base):
    fuselage_radius = Input(4.)
    fuselage_length = Input(30.)
    engine_radius = Input(1.3)
    engine_length = Input(5.)
    density = Input(1.225)
    speed = Input(120.)
    n_engines = Input(4)

    @Part
    def my_wing(self):
        return Wing(span=5.)