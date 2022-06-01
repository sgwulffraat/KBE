import typing

from parapy.core import HiddenPart, Input, Attribute, on_event
from parapy.core.abstract import DrawableParaPyObject
from parapy.geom import Cube, VZ, VX, VY
from parapy.geom.occ.drawable import DrawableShape
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, ManipulationMode, Manipulation
from parapy.gui.manipulation.gizmo import GizmoBase
from parapy.gui.manipulation.modes import Translation


class FaceGizmoHandleWrapper(DrawableShape):
    face = Input()
    mode: ManipulationMode = Input()
    boundary_color = Input('black')
    selection_sensitivity = Input(1)
    line_thickness = 1

    @property
    def _Handle_AIS_InteractiveObject(self):
        return self.face._Handle_AIS_InteractiveObject


class CubeGizmo(GizmoBase):
    cube: Cube = Input()

    # all in_tree slots will be automatically picked up by the base class'
    # `GizmoBase.shapes` slot. But in our case we want to take some faces
    # and set their colors, so we can just override the method.
    @Attribute
    def shapes(self) -> typing.Sequence[DrawableShape]:
        cube = self.cube
        faces = []
        for face in [cube.top_face, cube.bottom_face]:
            faces.append(FaceGizmoHandleWrapper(face=face, color='red',
                                                mode=Translation(VZ)))
        for face in [cube.left_face, cube.right_face]:
            faces.append(FaceGizmoHandleWrapper(face=face, color='green',
                                                mode=Translation(VX)))
        for face in [cube.front_face, cube.rear_face]:
            faces.append(FaceGizmoHandleWrapper(face=face, color='blue',
                                                mode=Translation(VY)))
        return faces

    # we need to override this method to tell to the gizmo which mode should
    # be activated depending on which face is being selected.
    def interactive_shape_to_manipulation_mode(
            self, detected_object: DrawableParaPyObject) -> \
            typing.Optional[ManipulationMode]:

        if isinstance(detected_object, FaceGizmoHandleWrapper):
            return detected_object.mode


class CustomManipulable(Cube):
    label = 'right-click me in the viewer to start manipulating'

    @HiddenPart
    def gizmo(self):
        return CubeGizmo(position=self.position,
                         cube=self)

    def create_manipulation(self, viewer):
        """
        :param parapy.gui.viewer.Viewer viewer: viewer in which the
            manipulation takes place.
        :rtype: Manipulation
        """
        return Manipulation(obj=self,
                            viewer=viewer,
                            gizmo=self.gizmo,
                            # uncomment this to make the object itself act as
                            # its ghost, meaning that the original shape will
                            # move along with the gizmo and at all effects,
                            # in this case, disappear until on_end.
                            # ghost=self,
                            reference_position=self.position,
                            on_submit=self.on_submit)

    def start(self, viewer):
        """Start to make_manipulation this Manipulable object inside
        ``viewer``."""
        viewer = viewer

        manipulation = self.create_manipulation(viewer)
        manipulation.start()

    @on_event(EVT_RIGHT_CLICK_OBJECT)
    def _on_left_click(self, evt):
        self.start(evt.source)

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    display(CustomManipulable(1))