from parapy.core import Part, action, child
from parapy.core.sequence import MutableSequence
from parapy.geom import Box, GeomBase, translate
from parapy.gui import get_top_window
from parapy.gui.actions import ViewerSelection


class MutableBoxesExample(GeomBase):

    @Part
    def boxes(self):
        return MutableSequence(type=Box, quantify=2,
                               width=1, length=1, height=child.index + 1,
                               position=translate(self.position, 'x',
                                                  child.index),
                               label=(f"Box {id(child.__this__)} at "
                                      f"index: {child.index}"))

    @action
    def append_red_box(self):
        self.boxes.append(Box(1, 1, 1, color='red'))

    @action
    def append_green_box(self):
        self.boxes.append(Box(1, 1, 1, color='green'))

    @action
    def append_box(self):
        self.boxes.append(Box())  # parameters are obtained from parent

    @action
    def pop_last(self):
        self.boxes.pop()

    @action
    def remove_boxes(self):
        # Enter selection mode for the user to select boxes in the viewer
        main_window = get_top_window()
        context = ViewerSelection(main_window, multiple=True)
        if context.start():
            for obj in context.selected:
                self.boxes.remove(obj)


if __name__ == '__main__':
    from parapy.gui import display

    obj = MutableBoxesExample()
    display(obj, autodraw=True)