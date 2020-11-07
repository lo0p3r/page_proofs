from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.drag_n_drop import (
    DraggableController, DraggableLayoutBehavior, DraggableObjectBehavior,
    SpacerWidget)
from kivy.properties import ObjectProperty

drag_controller = DraggableController()

class RootLayout(BoxLayout):
    pages: ObjectProperty(None)


class DraggableBoxLayout(DraggableLayoutBehavior, BoxLayout):

    def compare_pos_to_widget(self, widget, pos):
        if self.orientation == 'vertical':
            return 'before' if pos[1] >= widget.center_y else 'after'
        return 'before' if pos[0] < widget.center_x else 'after'

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)

class DragLabel(DraggableObjectBehavior, Label):

    def __init__(self, **kwargs):
        super(DragLabel, self).__init__(
            **kwargs, drag_controller=drag_controller)

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)

class DragAndDrop(App):

    drag_controller = drag_controller

if __name__ == "__main__":
    DragAndDrop().run()