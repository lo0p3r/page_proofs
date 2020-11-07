from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

import os

class UploadWindow(Screen):
    paths = StringProperty()
    text_input = StringProperty()

    def show_load_list(self):
        content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load the sound files", content=content, size_hint=(.5, .5))
        self._popup.open()

    def load_list(self, path, filename):
        with open(os.path.join(path, filename[0]), encoding="utf8", errors='ignore') as stream:
            filename_actual = os.path.basename(filename.pop())
            global importedfiles
            importedfiles.append((filename_actual, path))
            print(importedfiles)

        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Loader(App):
    pass

if __name__ == '__main__':
    Loader().run()