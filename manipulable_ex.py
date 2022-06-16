from parapy.core import Base, Input, Part, action, child, val
from parapy.geom import Box
from parapy.gui import refresh_top_window


class BoxSizer(Base):
    flag = Input(True)
    width = Input(1, validator=val.Range(1, 5))

    @Part
    def box(self):
        return Box(width=self.width,
                   length=2,
                   height=3,
                   color=(int((child.width - 1) * (255 / 5)),
                          255 - int((child.width - 1) * (255 / 5)),
                          0),
                   tree_style={"color": child.color})

    @action
    def resize(self):
        from time import sleep
        import random
        for _ in range(50):
            self.width = random.randint(1, 5)
            self.flag = not self.flag
            refresh_top_window()
            sleep(0.05)


if __name__ == '__main__':
    from parapy.gui import display

    obj = BoxSizer()
    display(obj)