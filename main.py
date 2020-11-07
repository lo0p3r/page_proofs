from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from pdf2image import convert_from_path
import tempfile
import os
import sys
from pathlib import Path
import ghostscript
import locale


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        # here comes loading
        pdf_file = os.path.join(path, filename[0])
        self.text_input.text = pdf_file
        #with open(os.path.join(path, filename[0])) as stream:
        #    self.text_input.text = stream.read()
        pdf_dir = os.path.dirname(pdf_file)
        temp_dir_name = os.path.join(
            pdf_dir,
            os.path.basename(pdf_file)[:-4])
        #temp_dir = tempfile.TemporaryDirectory('', '', pdf_dir)
        if not os.path.exists(temp_dir_name):
            os.makedirs(temp_dir_name)
        poppler_path = r"C:\Python\poppler-20.11.0\bin"
        #pages = convert_from_path(
        #    pdf_file,
        #    poppler_path=poppler_path,
        #    output_folder=temp_dir.name,
        #    fmt='jpg',
        #    dpi=300,
        #    output_file='')

        #count = 0
        #for page in pages:
        #    page.save(os.path.join(temp_dir, 'out' + str(count) + '.jpg'), 'JPEG')

        self.extract_jpg(pdf_file, temp_dir_name)
        #self.pdf2jpeg(pdf_file, temp_dir_name)

        self.dismiss_popup()

    def save(self, path, filename):
        # here comes saving

        # with open(os.path.join(path, filename), 'w') as stream:
        #    stream.write(self.text_input.text)

        self.dismiss_popup()

    def extract_jpg(self, input_path, output_path):
        with open(input_path, "rb") as file:
            pdf = file.read()

            startmark = b"\xff\xd8"
            startfix = 0
            endmark = b"\xff\xd9"
            endfix = 2
            i = 0

            njpg = 1
            while True:
                istream = pdf.find(b"stream", i)
                if istream < 0:
                    break
                istart = pdf.find(startmark, istream, istream + 20)
                if istart < 0:
                    i = istream + 20
                    continue
                iend = pdf.find(b"endstream", istart)
                if iend < 0:
                    raise Exception("Didn't find end of stream!")
                iend = pdf.find(endmark, iend - 20)
                if iend < 0:
                    raise Exception("Didn't find end of JPG!")

                istart += startfix
                iend += endfix
                jpg = pdf[istart:iend]
                file_name = os.path.basename(input_path)
                newfile = "{}.jpg".format(file_name[:-4] + "_" + str(njpg).zfill(3))
                output_file = os.path.join(output_path, newfile)
                with open(output_file, "wb") as jpgfile:
                    jpgfile.write(jpg)

                njpg += 1
                i = iend

                #return newfile

    def pdf2jpeg(self, pdf_input_path, jpeg_output_path):
        args = ["gs",  # actual value doesn't matter
                "--permit-file-read=" + os.path.dirname(pdf_input_path),
                "--permit-file-write=" + jpeg_output_path,
                "-dNOPAUSE",
                #"-dBATCH",
                "-sDEVICE=jpeg",
                "-dTextAlphaBits=4",
                "-r300",
                #"-sOutputFile=" + jpeg_output_path,
                "-o a%03d.jpg",
                pdf_input_path]

        encoding = locale.getpreferredencoding()
        args = [a.encode(encoding) for a in args]

        with ghostscript.Ghostscript(*args) as g:
            ghostscript.cleanup()

class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    Editor().run()