# Database #


import os, json, threading

import convert


def init_database(sound_lib_path, database_path):
    # initialize the database

    sound_library = os.listdir(sound_lib_path)

    for folder in sound_library:
        current_folder_path = os.path.join(sound_lib_path, folder)

        if os.path.isfile(current_folder_path): continue

        if folder == ".DS_Store": continue

        elif "_Sound Ideas def" in folder:
        # initialize sound_ideas_def libraries
            sound_ideas_path = os.path.join(sound_lib_path, folder)
            sound_ideas_folder = os.listdir(sound_ideas_path)

            for si_folder in sound_ideas_folder:
                if os.path.isfile(si_folder): continue
                if "DS" in si_folder or "ds" in si_folder or "Store" in si_folder: continue

                current_si_folder_path = os.path.join(sound_ideas_path, si_folder)

                for file in os.listdir(current_si_folder_path):
                    current_file_path = os.path.join(current_si_folder_path, file)

                    filename, extension = os.path.splitext(file) 

                    if extension == ".pdf" and not filename.startswith("._"):

                        new_file = filename + ".json"
                        new_file_path = os.path.join(database_path, new_file)
                        convert.convert_pdf_to_json(current_file_path, new_file_path)

        else:
        # initialize any other folder found in the root dir of the sound_lib_path
            convert.convert_folder_to_database(current_folder_path, database_path)


def load_database(database_path, **kwargs):
    # load the database in memory for a faster access

    progress_function = kwargs.get("progress", None)

    db_files = os.listdir(database_path)

    progress_jump = 100.0 / len(db_files)

    progress = 0

    database = []

    for file in files:
        name, ext = os.path.splitext(file)

        if ext != ".json":
            continue

        else:
            file_path = os.path.join(database_path, file)

            with open(file_path, "r") as f:
                file_data = json.load(f)

            for element in file_data:
                database.append(element)

        progress += progress_jump
        progress_function(progress)

    
    return database





