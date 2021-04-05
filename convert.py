# Convert #

# This file contains methods to convert the serie of pdf from SoundIdeasDef to json files

import pdfplumber, json, sys, os, re
from threading import Thread

from logger import Logger


def convert_pdf_to_json(src_file, dest_file):
    # convert a pdf file to a database usable for SoundFinder
    
    pdf = pdfplumber.open(r"%s" % src_file)

    items = []

    progress_jump = 100.0 / len(pdf.pages)
    progress = 0
    
    for p in pdf.pages:

        text = p.extract_words(use_text_flow=True, keep_blank_chars=True)

        index = 0
        list_index = 0

        i = 0

        for i in range(0, (len(text) - 9), 9):

            filename_base = str(text[i + 2]["text"]).replace(u"\xa0", u" ")

            filename = filename_base

            m = re.search(r"\d(.*)\d", filename_base)
            
            if m:
                filename = m.group(0).replace("_", "")
                filename = F"sss{filename}.wav"

            sound = {
                "Title" : str(text[i]["text"]).replace(u"\xa0", u" "),
                "Description" : str(text[i + 1]["text"]).replace(u"\xa0", u" "),
                "FileName" : filename,
                "Keywords" : str(text[i + 3]["text"]).replace(u"\xa0", u" "),
                "Time" : str(text[i + 5]["text"]).replace(u"\xa0", u" ")
            }

            items.append(sound)
        
        progress += progress_jump
        progress_out = round(progress)

        if progress_out % 5 == 0 or progress_out == 1:
            Logger.console_progress_bar(f"Processing {src_file} : ", f" {progress_out}%", progress_out, 20)


    with open(r"%s" % dest_file, "w") as output:
        json.dump(items, output, indent=2)
    


def convert_folder_to_database(folder_path, database_path):
    # convert a folder to a database usable for ENSISoundFinder
    items = []
    progress = 0
    
    total_files = 0

    for root, dirs, files in os.walk(folder_path, topdown=True):
        for f in files: total_files += 1


    for root, dirs, files in os.walk(folder_path, topdown=True):
            for f in files:
                progress_jump = 100.0 / total_files

                name, extension = os.path.splitext(f)
                tags = ""

                if extension == ".wav":
                    filepath = os.path.join(root, f)
                    subdirs = filepath.replace(root, "")
                    subdirs_re = re.sub("[^a-z^A-Z^0-9]", " ", subdirs)
                    name_re = re.sub("[^a-z^A-Z^0-9]", " ", name)
                    tags += subdirs_re
                    tags += name_re

                    item = {
                        "Title" : name,
                        "Description" : "",
                        "FileName" : filepath,
                        "Keywords" : tags,
                        "Time" : ""
                    }

                    items.append(item)

                progress += progress_jump
                progress_out = round(progress)

                if progress_out % 5 == 0 or progress_out == 1:
                    Logger.console_progress_bar(f"Processing {folder_path} : ", f" {progress_out}%", progress_out, 20)

    output_filename = os.path.basename(folder_path) + ".json"
    output_file = os.path.join(database_path, output_filename.lower())

    with open(output_file, "w") as f:
        json.dump(items, f, indent=2)