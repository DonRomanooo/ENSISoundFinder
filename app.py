# Application #

import sys, os, json
from playsound import playsound
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import database


class Popup(QWidget):
    def __init__(self, name, has_message=False, message="" ,has_progress_bar=False, has_output_list=False):
        QWidget.__init__(self)

        self.setWindowTitle(name)

        main_layout = QVBoxLayout()

        self.has_message = has_message
        self.has_progress_bar = has_progress_bar
        self.has_output_list = has_output_list

        if has_message:
            self.message = QLabel(message)
            main_layout.addWidget(self.message)

        if has_progress_bar:
            self.progress_bar = QProgressBar(self)
            main_layout.addWidget(self.progress_bar)

        if has_output_list:
            self.output_list = QListView()
            main_layout.addWidget(self.output_list)

        self.setLayout(main_layout)


    def set_progress_status(progress):
        if self.has_progress_bar: self.progress_bar.setValue(progress)


    def add_message(msg):
        if self.has_output_list: self.output_list.append(msg)


class App(QMainWindow):
    # main application

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("ENSI Sound Finder")

        main_layout = QVBoxLayout()
        main_widget = QWidget(self)

        # menubar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        help_menu = menubar.addMenu("Help")

        # working dir
        working_dir_layout = QHBoxLayout()

        self.current_working_directory = "D:/Mon_film/postprod/sons/boot"
        self.working_dir_label = QLabel(self.current_working_directory)
        working_dir_layout.addWidget(self.working_dir_label)

        self.set_working_dir_button = QPushButton("Select")
        self.set_working_dir_button.setMaximumWidth(70)
        working_dir_layout.addWidget(self.set_working_dir_button)

        # searchbar 
        searchbar_layout = QHBoxLayout()

        self.input_tags = QLineEdit("Tags")
        searchbar_layout.addWidget(self.input_tags)

        self.search_button = QPushButton("Search")
        self.search_button.setMaximumWidth(70)
        searchbar_layout.addWidget(self.search_button)

        # list
        self.search_list = QListWidget()

        # tools buttons
        tools_layout = QHBoxLayout()

        self.play_button = QPushButton("Play")
        tools_layout.addWidget(self.play_button)

        self.add_button = QPushButton("Add")
        tools_layout.addWidget(self.add_button)

        # layout
        main_layout.addLayout(working_dir_layout)
        main_layout.addLayout(searchbar_layout)
        main_layout.addWidget(self.search_list)
        main_layout.addLayout(tools_layout)

        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)

        self.popup_window = None

    
    def settings_ui(self):
        pass


    def update_list(self):
        pass


    def initialize(self):
        # initialize the application when you run it
        # if you run it for the first time, it will initialize the database
        self.pref_file = os.environ["APPDATA"] + "/ENSISoundFinder/preferences.pref"
        self.sound_lib_database = os.environ["APPDATA"] + "/ENSISoundFinder/data"

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

            database.init_database(self.sound_lib_dir, self.sound_lib_database)

            
        self.data = database.load_database(self.sound_lib_database)


        




app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
application = App()
application.show()

app.exec_()