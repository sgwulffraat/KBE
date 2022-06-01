from parapy.core import Base, Input, on_event, Attribute
from parapy.geom import Compound, Position, Box, Vector
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, Gizmo, Manipulation, MotionEvent, PlanarTranslation, Translation


class ManipulateAnything(Base):
    label = 'right-click the object that is to be moved in the viewer to manipulate selected'

    to_manipulate = Input(in_tree=True)

    @Attribute(in_tree=True)
    def boundary(self):
        edges = Box(400, 400, 200, centered=True, color='blue', transparency=.5).edges
        for e in edges:
            e.color = 'red'
        return edges

    @on_event(EVT_RIGHT_CLICK_OBJECT)
    def on_click(self, evt):
        if evt.selected[0] == self.to_manipulate.bracket_box \
                or evt.selected[0] == self.to_manipulate.bracket_cylinder \
                or evt.selected[0] == self.to_manipulate.bracket_from_file:
            return print("Bracket is not manipulable")
        elif evt.multiple:
            self.start_manipulation_many(evt.selected, evt.source)
        else:
            self.start_manipulation_one(evt.selected[0], evt.source)

    def start_manipulation_one(self, obj, viewer):
        def on_motion(evt: MotionEvent):
            current_position = evt.current_position
            if -200 > current_position.y or current_position.y > 200:
                evt.Veto()
            if -200 > current_position.x or current_position.x > 200:
                evt.Veto()
            if -100 > current_position.z or current_position.z > 100:
                evt.Veto()

        def on_submit(evt: EndEvent):
            self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, on_motion, viewer)

    def _on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        if -2 > current_position.y or current_position.y > 2:
            evt.Veto()
        if -2 > current_position.x or current_position.x > 2:
            evt.Veto()
        if -1 > current_position.z or current_position.z > 1:
            evt.Veto()

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

        def on_motion(evt: MotionEvent):
            current_position = evt.current_position
            if -200 > current_position.y or current_position.y > 200:
                evt.Veto()
            if -200 > current_position.x or current_position.x > 200:
                evt.Veto()
            if -100 > current_position.z or current_position.z > 100:
                evt.Veto()

        def on_submit(evt: EndEvent):
            for obj in objs:
                self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, on_motion, viewer)

    def _start_manipulation(self, obj, on_submit, on_motion, viewer):
        gizmo = Gizmo(size=20, position=obj.position, modes=[Translation(axis=Vector(1,0,0))])
        obj = Manipulation(obj=obj,
                           viewer=viewer,
                           on_submit=on_submit,
                           on_motion=on_motion,
                           ghost=obj,
                           gizmo=gizmo, )
        obj.start()

    def _on_submit(self, evt: EndEvent, obj):
        obj.position = evt.transformation.apply(obj.position)
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.geom import Cube
    from parapy.gui import display

    object2 = Bracket()
    # obj3 = ManipulateAnything(to_manipulate=Connector(c_type="Mil"))

    display(obj3)
