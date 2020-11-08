from kivy.app import App
# from kivy.garden.magnet import Magnet
from magnet import Magnet
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import os

IMAGEDIR = 'C:\\Programming\\32'

IMAGES = filter(
    lambda x: x.endswith('.png'),
    os.listdir(IMAGEDIR))


class Root(FloatLayout):
    pass


class DraggableImage(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)

    def on_img(self, *args):
        self.clear_widgets()

        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.remove_widget(self.img)
            self.app.root.add_widget(self.img)
            self.center = touch.pos
            self.img.center = touch.pos
            return True

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        grid_layout = self.app.root.ids.grid_layout
        float_layout = self.app.root.ids.float_layout

        if touch.grab_current == self:
            self.img.center = touch.pos
            if grid_layout.collide_point(*touch.pos):
                grid_layout.remove_widget(self)
                float_layout.remove_widget(self)

                for i, c in enumerate(grid_layout.children):
                    if c.collision_point(*touch.pos):  # if c.collide_point(*touch.pos):
                        grid_layout.add_widget(self, i + 1)  # grid_layout.add_widget(self, i - 1)
                        break
                else:
                    grid_layout.add_widget(self)
            else:
                if self.parent == grid_layout:
                    grid_layout.remove_widget(self)
                    float_layout.add_widget(self)

                self.center = touch.pos

        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if touch.grab_current == self:
            self.app.root.remove_widget(self.img)
            self.add_widget(self.img)
            touch.ungrab(self)
            return True

        return super(DraggableImage, self).on_touch_up(touch, *args)

    def collision_point(self, x, y):
        x_left = self.center_x - (self.width / 1.5)

        x_right = self.center_x + (self.width / 1.5)
        y_bottom = self.center_y - (self.height / 1.5)
        y_top = self.center_y + (self.height / 1.5)
        return x_left <= x <= x_right and y_bottom <= y <= y_top


class WordBuilder(App):
    def build(self):
        # self.root = Builder.load_string(kv)
        for i in IMAGES:
            image = Image(source=os.path.join(IMAGEDIR, i), size=(32, 32),
                          size_hint=(None, None))

            draggable = DraggableImage(img=image, app=self,
                                       size_hint=(None, None),
                                       size=(32, 32))
            self.root.ids.grid_layout.add_widget(draggable)

        return self.root


if __name__ == '__main__':
    WordBuilder().run()
