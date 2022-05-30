from parapy.core import Base, Input, on_event
from parapy.geom import Compound, Position
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, Gizmo, Manipulation


class ManipulateAnything(Base):
    label = 'right-click me in the viewer to manipulate selected'

    to_manipulate = Input(in_tree=True)

    @on_event(EVT_RIGHT_CLICK_OBJECT)
    def on_click(self, evt):
        if evt.multiple:
            self.start_manipulation_many(evt.selected, evt.source)
        else:
            self.start_manipulation_one(evt.selected[0], evt.source)

    def start_manipulation_one(self, obj, viewer):
        def on_submit(evt: EndEvent):
            self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, viewer)

    def are_orientations_aligned(self, orientations):
        ori, *oris = orientations
        for _ori in oris:
            if not _ori.is_almost_equal(ori):
                return False
        return True

    def start_manipulation_many(self, objs, viewer):
        if self.are_orientations_aligned((o.orientation for o in objs)):
            basis_pos = objs[0].position
        else:
            basis_pos = Position()

        obj = Compound(
            objs,
            position=basis_pos.replace(
                location=objs[0].position.midpoint(
                    objs[-1].position)))

        def on_submit(evt: EndEvent):
            for obj in objs:
                self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, viewer)

    def _start_manipulation(self, obj, on_submit, viewer):
        gizmo = Gizmo(size=.4, position=obj.position)
        obj = Manipulation(obj=obj, viewer=viewer, on_submit=on_submit,
                           ghost=obj, gizmo=gizmo)
        obj.start()

    def _on_submit(self, evt: EndEvent, obj):
        obj.position = evt.transformation.apply(obj.position)


if __name__ == '__main__':
    from parapy.geom import Cube
    from parapy.gui import display

    boxes = [
        Cube(1, centered=True, color="red"),
        Cube(1, centered=True, color="green",
             position=Position().translate(x=2)),
        Cube(1, centered=True, color="blue",
             position=Position().translate(x=4))]

    obj = ManipulateAnything(to_manipulate=boxes)

    display(obj)
