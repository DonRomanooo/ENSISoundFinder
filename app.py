# Application #

import sys, os, json, time, shutil, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import database, find
from logger import Logger


class InitThread(QThread):
    update = pyqtSignal(int)

    def __init__(self, sound_lib_dir, sound_lib_database, **kwargs):
        QThread.__init__(self)

        self.sound_lib_dir = sound_lib_dir
        self.sound_lib_database = sound_lib_database

        self.message_func = kwargs.get("message", None)
        self.close_prog_func = kwargs.get("close_prog", None)
        self.close_log_func = kwargs.get("close_log", None)
        self.init = kwargs.get("init", True)

    def run(self):
        if self.init: database.init_database(self.sound_lib_dir, self.sound_lib_database, progress=self.update.emit, message=self.message_func)

        if self.message_func: self.message_func("Loading Database...")

        self.database = database.load_database(self.sound_lib_database, progress=self.update.emit)

        time.sleep(1)

        if self.close_prog_func: self.close_prog_func()
        if self.close_log_func: self.close_log_func()


class Popup(QWidget):
    def __init__(self, name, has_message=False, message="" ,has_progress_bar=False, has_output_list=False):
        QWidget.__init__(self)

        self.setWindowTitle(name)

        self.has_message = has_message
        self.message = message
        self.has_progress_bar = has_progress_bar
        self.has_output_list = has_output_list

        main_layout = QVBoxLayout()

        if self.has_message:
            self.message_label = QLabel(self.message)
            main_layout.addWidget(self.message_label)

        if self.has_progress_bar:
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(0, 0, 300, 25)
            self.progress_bar.setMaximum(100)
            main_layout.addWidget(self.progress_bar)

        if self.has_output_list:
            self.output_list = QListWidget()
            main_layout.addWidget(self.output_list)

        self.setLayout(main_layout)

        self.show()


    def set_progress_status(self, progress):
        if self.has_progress_bar: self.progress_bar.setValue(progress)


    def add_message(self, msg):
        if self.has_output_list: self.output_list.addItem(msg)


class App(QMainWindow):
    # main application

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("ENSI Sound Finder")

        self.setMinimumWidth(600)
        self.setMinimumHeight(900)

        main_layout = QVBoxLayout()
        main_widget = QWidget(self)

        # menubar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        help_menu = menubar.addMenu("Help")

        # working dir
        working_dir_layout = QHBoxLayout()

        self.current_working_directory = "D:/"
        self.working_dir_label = QLabel(self.current_working_directory)
        working_dir_layout.addWidget(self.working_dir_label)

        self.set_working_dir_button = QPushButton("Select")
        self.set_working_dir_button.setMaximumWidth(70)
        self.set_working_dir_button.clicked.connect(self.set_working_dir)
        working_dir_layout.addWidget(self.set_working_dir_button)

        # searchbar 
        searchbar_layout = QHBoxLayout()

        self.input_tags = QLineEdit("Tags")
        searchbar_layout.addWidget(self.input_tags)

        self.search_button = QPushButton("Search")
        self.search_button.setMaximumWidth(70)
        self.search_button.clicked.connect(self.search)
        searchbar_layout.addWidget(self.search_button)

        # list
        self.search_list = QListWidget()

        # tools buttons
        tools_layout = QHBoxLayout()

        self.play_button = QPushButton("Open")
        self.play_button.clicked.connect(self.open)
        tools_layout.addWidget(self.play_button)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy)
        tools_layout.addWidget(self.copy_button)

        # layout
        main_layout.addLayout(working_dir_layout)
        main_layout.addLayout(searchbar_layout)
        main_layout.addWidget(self.search_list)
        main_layout.addLayout(tools_layout)

        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)

        self.popup_window = None

        self.initialize()


    def set_working_dir(self):
        self.current_working_directory = QFileDialog.getExistingDirectory(self, "Select the working directory", "C:/")
        self.working_dir_label.setText(self.current_working_directory)


    def copy(self):
        self.selected_items = self.search_list.selectedItems()

        new_name, ok = QInputDialog.getText(self, "Copy File", "Set he new filename :")

        if len(self.selected_items) > 0 and ok:
            for s_item in self.selected_items:
                for found_item in self.found_sounds:
                    if s_item.text() == f"{found_item['Title']} {found_item['Description']}":
                        
                        filename = found_item["FileName"]
                        dirname = self.current_working_directory

                        if not new_name.endswith(".wav") : new_name += ".wav"

                        copy_filename = os.path.join(dirname, new_name)

                        shutil.copy(filename, copy_filename)


    def open(self):
        self.selected_items = self.search_list.selectedItems()

        if len(self.selected_items) > 0:
            for s_item in self.selected_items:
                for found_item in self.found_sounds:
                    if s_item.text() == f"{found_item['Title']} {found_item['Description']}":
                        
                        filename = found_item["FileName"]
                        
                        if(os.path.exists(filename)):
                            subprocess.Popen([filename], shell=True)

    
    def settings_ui(self):
        pass


    def search(self):
        tags = self.input_tags.text().split(" ")
        self.found_sounds = find.search(self.database, tags)
        self.update_list()


    def update_list(self):
        self.search_list.clear()

        for item in self.found_sounds:
            self.search_list.addItem(f"{item['Title']} {item['Description']}")


    def initialize(self):
        # initialize the application when you run it
        # if you run it for the first time, it will initialize the database
        self.pref_file = os.environ["APPDATA"] + "/ENSISoundFinder/preferences.pref"
        self.sound_lib_database = os.environ["APPDATA"] + "/ENSISoundFinder/data"

        self.init_popup = Popup("ENSISoundFinder", has_output_list=True)
        self.init_popup.setMinimumHeight(600)
        self.init_popup.setMinimumWidth(250)

        self.init_popup.add_message("Initializing ENSISoundFinder...")

        if not os.path.exists(self.pref_file):
            os.umask(770)
            os.makedirs(os.path.dirname(self.pref_file))
            os.makedirs(self.sound_lib_database)

            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.Directory)

            self.sound_lib_dir = dlg.getExistingDirectory(self, "Select the sound library directory")

            with open(self.pref_file, "w") as f:
                pref_data = {
                    "SOUND_LIB_PATH" : self.sound_lib_dir,
                    "DATABASE_PATH" : self.sound_lib_database
                }

                json.dump(pref_data, f, indent=2)

            self.init_popup.add_message("Initializing database...")

            self.progress_popup = Popup("Progress", has_message=True, message = "Progress", has_progress_bar=True)

            self.init_thread = InitThread(self.sound_lib_dir, self.sound_lib_database, message=self.init_popup.add_message, close_prog=self.progress_popup.close, close_log=self.init_popup.close)
            self.init_thread.update.connect(self.progress_popup.set_progress_status)
            self.init_thread.finished.connect(self.move_database)
            self.init_thread.start()

        else:
            
            with open(self.pref_file, "r") as f:
                data = json.load(f)

            self.sound_lib_dir = data["SOUND_LIB_PATH"]

            self.progress_popup = Popup("Progress", has_message=True, message = "Progress", has_progress_bar=True)
            self.progress_popup.show()

            self.init_thread = InitThread(self.sound_lib_dir, self.sound_lib_database, message=self.init_popup.add_message, close_prog=self.progress_popup.close, close_log=self.init_popup.close, init=False)
            self.init_thread.update.connect(self.progress_popup.set_progress_status)
            self.init_thread.finished.connect(self.move_database)
            self.init_thread.start()
        

    def move_database(self):
        self.database = self.init_thread.database
        Logger.message("Database loaded successfully")



app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
application = App()
application.show()

app.exec_()