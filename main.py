import logging
import os.path
from tkinter import filedialog, Tk

import PyPDF2
from kivy.clock import mainthread
from kivy4 import *
from kiv import kv
from pylovepdf.ilovepdf import ILovePdf
from pathlib import Path
import shutil
import subprocess

API_KEY = "project_public_520d7abecca835958fd98934e0c49dc8_m5o735ee791f8a3701efe1908d1ae43756ff3"

root = Tk()
root.withdraw()

app_data_path = os.getenv('APPDATA') + '\\' + "PDF Compressor Pro"




def is_valid_pdf(path):
    try:
        PyPDF2.PdfFileReader(open(path, "rb"))
        return True
    except Exception:
        return False


class App(Kivy4):
    file_names = ListProperty([])
    tic = 0
    output_dir = StringProperty("")
    stop_loading = False
    dst = None
    is_compressing = False
    files = []

    def compress_pdf(self, path_list, output_directory):
        if not path_list:
            return False

        if os.path.exists(f"{app_data_path}/output_dir"):
            shutil.rmtree(f"{app_data_path}/output_dir")

        ilovepdf = ILovePdf(API_KEY, verify_ssl=True)
        task = ilovepdf.new_task('compress')

        count = 0
        for path in path_list:
            task.add_file(path)
            count += 1

        task.set_output_folder(f"{app_data_path}/output_dir")
        task.execute()
        task.download()
        task.delete_current_task()

        if count == 1:
            name = os.path.basename(path_list[0]).replace(".pdf", "") + "_compressed.pdf"
        else:
            c = 0
            while os.path.exists(f"{output_directory}/pdf_compressed_{c}.zip"):
                c += 1

            name = f"pdf_compressed_{c}.zip"

        src = f"{app_data_path}/output_dir/" + os.listdir(f"{app_data_path}/output_dir")[0]
        self.dst = f"{output_directory}/{name}"

        shutil.copy(src, self.dst)
        return os.path.getsize(self.dst)

    def on_start(self):
        self.output_dir = self.getFile("output", str(Path.home() / "Downloads"))

    @mainthread
    def make_not_bold(self):
        self.root.ids.title.bold = False

    @thread
    def compress_files(self):
        if self.is_compressing:
            return

        self.stop_loading = False
        self.is_compressing = True

        self.loading_title("Compressing your files")
        try:
            self.make_not_bold()

            files = [x.split("@")[0] for x in self.file_names]
            response = self.compress_pdf(files, self.output_dir)

            old_size = sum(os.path.getsize(file) for file in files)

            self.stop_loading = True

            if response is not False:
                self.set_title(f"Finished successfully!\nold size: {old_size / 1000}kb - new size: {response / 1000}kb\nfiles size reduces by {round((1 - response / old_size) * 100, 1)}%")
                self.root.ids.open.opacity = 1
            else:
                self.set_title("You haven't selected any file")

        except Exception as e:
            logging.error(str(e))
            self.stop_loading = True
            self.set_title("An error occurred")

        finally:
            self.is_compressing = False

    @thread
    def loading_title(self, text):
        while not self.stop_loading:
            for i in range(1, 4):
                if self.stop_loading:
                    return
                self.set_title(text + "." * i)
                time.sleep(0.5)

    @mainthread
    def set_title(self, text):
        self.root.ids.title.text = text

    def on_drop_file(self, kivy_object, path_in_bytes):
        if time.time() - self.tic > 1:
            self.file_names = []

        path = path_in_bytes.decode()

        if is_valid_pdf(path):
            self.file_names.append(path)

        self.tic = time.time()

    def choose_file(self):
        files = filedialog.askopenfiles(filetypes=[('PDF Document', '*.pdf')], defaultextension=".pdf")
        self.file_names = [file.name + f"@{round(os.path.getsize(file.name) / 1000, 2)}kb" for file in files if
                           is_valid_pdf(file.name)]

    def select_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.setFile("output", str(path))
            self.output_dir = path


    def open_folder(self):
        self.dst = self.dst.replace("/", "\\")
        subprocess.Popen(rf'explorer /select,"{self.dst}"')



App(app_name='PDF Compressor Pro', toolbar=True, main_color='Orange', string=kv,
    screen_size=[950, 550], icon='img.png')


