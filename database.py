# Database #


import os, json

import convert


def init_database(sound_lib_path, database_path):
    # initialize the database

    sound_library = os.listdir(sound_lib_path)

    for folder in sound_library:
        current_folder_path = os.path.join(sound_library, folder)

        if os.path.isfile(current_folder_path): continue

        else if "Sound Ideas def" in folder:
        # initialize sound_ideas_def libraries
            sound_ideas_path = os.path.join(sound_lib_path, folder)
            sound_ideas_folder = os.listdir(sound_ideas_path)

            for si_folder in sound_ideas_folder:
                if os.path.isfile(si_folder): continue

                current_si_folder_path = os.path.join(sound_ideas_folder, si_folder)

                for file in os.listdir(current_si_folder_path):
                    current_file_path = os.path.join(current_si_folder_path, file)

                    filename, extension = os.path.splitext(file) 

                    if extension == "pdf":

                        new_file = filename + ".json"
                        new_file_path = os.path.join(database_path, new_file)
                        convert.convert_pdf_to_json(current_file_path, new_file_path)

        else:
        # initialize any other folder found in the root dir of the sound_lib_path
            convert.convert_folder_to_database(current_folder_path, database_path)





