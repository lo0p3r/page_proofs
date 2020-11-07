from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy_garden.drag_n_drop import (
    DraggableController, DraggableLayoutBehavior, DraggableObjectBehavior,
    SpacerWidget)

drag_controller = DraggableController()

class MyBoxLayout(BoxLayout):
    def mycallback(self, instance):
        print('The button <%s> is being pressed' % instance.text)

class DraggableBoxLayout(DraggableLayoutBehavior, BoxLayout):

    def compare_pos_to_widget(self, widget, pos):
        if self.orientation == 'vertical':
            return 'before' if pos[1] >= widget.center_y else 'after'
        return 'before' if pos[0] < widget.center_x else 'after'

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)

kv= '''
MyBoxLayout:
    id: mybox
    Button:
        id: mybutton
        text: 'List widgets'
        on_press: root.mycallback(self)
        font_size: 14
        size: (300, 200)
        color: (1, 1, 1, 1)
    DraggableBoxLayout:
        id: drag1
        drag_classes: ['label']
        orientation: 'vertical'
        Label:
            id: l1
            text: 'A'
        Label:
            id: l2
            text: 'A'
        Label:
            id: l3
            text: 'A'
    DraggableBoxLayout:
        id: drag2
        drag_classes: ['label']
        orientation: 'vertical'
        DragLabel:
            id: l4
            text: 'A*'
            drag_cls: 'label'
        DragLabel:
            id: l5
            text: 'A*'
            drag_cls: 'label'
'''

class DragLabel(DraggableObjectBehavior, Label):

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)

class MyApp(App):

    drag_controller = drag_controller

    def build(self):
        return Builder.load_string(kv)

if __name__ == "__main__":
    MyApp().run()