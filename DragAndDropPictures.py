from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy_garden.drag_n_drop import (
    DraggableController, DraggableLayoutBehavior, DraggableObjectBehavior,
    SpacerWidget)
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

import os

drag_controller = DraggableController()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class RootLayout(BoxLayout):
    output_folder = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    pages: DictProperty(None)  # key - page number, value - dict (key - page property, like id, class, etc)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        if (os.path.isdir(os.path.join(path, filename[0]))):
            self.output_folder.text = os.path.join(path, filename[0])
        else:
            self.output_folder.text = 'C:\\'

        self.dismiss_popup()



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