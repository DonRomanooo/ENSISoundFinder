# Convert #

# This file contains methods to convert the serie of pdf from SoundIdeasDef to json files

import pdfplumber, json, sys, os, re, time, random
from threading import Thread

from logger import Logger
import utils


def convert_pdf_to_json(src_file, dest_file, **kwargs):
    # convert a pdf file to a database usable for SoundFinder
    
    pdf = pdfplumber.open(r"%s" % src_file)

    progress_function = kwargs.get("progress", None)
    message_function = kwargs.get("message", None)

    if message_function: message_function(f"Processing {src_file}")

    items = []

    progress_jump = 100.0 / len(pdf.pages)
    progress = 0

    index = 0

    for p in pdf.pages:

        text = p.extract_words(use_text_flow=True, keep_blank_chars=True)

        list_index = 0

        i = 0

        for i in range(0, (len(text) - 9), 9):

            filename_base = text[i + 2]["text"]

            filename = filename_base

            m = re.search(r"\d(.*)\d", filename_base)
            
            if m:
                filename = m.group(0).split("_")
                if len(filename) > 1: filename = f"sss{filename[0]}{filename[1]}.wav"
                else: filename = f"sss{filename[0]}.wav"
            
            sound = {
                "Title" : utils.cleanup_str(text[i]["text"]),
                "Description" : utils.cleanup_str(text[i + 1]["text"]),
                "FileName" : os.path.join(os.path.dirname(src_file), filename).replace("/", "\\"),
                "Keywords" : utils.cleanup_str(text[i + 3]["text"]).lower().split(" "),
                "Time" : utils.cleanup_str(text[i + 5]["text"])
            }

            sound["Keywords"] += sound["Title"].lower().split(" ")
            sound["Keywords"] += sound["Description"].lower().split(" ")

            for key in sound["Keywords"]:
                if key == "":
                    sound["Keywords"].remove(key)

            if len(items) > 0:
                if sound["FileName"] != items[index - 1]["FileName"]:
                    items.append(sound)
                    index += 1

            else:
                items.append(sound)
                index += 1
                
        progress += progress_jump
        progress_out = round(progress)

        if progress_function: progress_function(progress_out)

        if progress_out % 5 == 0 or progress_out == 1:
            Logger.console_progress_bar(f"Processing {src_file} : ", f" {progress_out}%", progress_out, 20)

    sys.stdout.write("\n")

    with open(r"%s" % dest_file, "w") as output:
        json.dump(items, output, indent=2)
    


def convert_folder_to_database(folder_path, database_path, **kwargs):
    # convert a folder to a database usable for ENSISoundFinder
    items = []
    progress = 0

    progress_function = kwargs.get("progress", None)
    message_function = kwargs.get("message", None)

    if message_function: message_function(f"Processing {folder_path}")
    
    total_files = 0

    for root, dirs, files in os.walk(folder_path, topdown=True):
        for f in files: total_files += 1


    for root, dirs, files in os.walk(folder_path, topdown=True):
            for f in files:
                progress_jump = 100.0 / total_files

                name, extension = os.path.splitext(f)
                tags = []

                if extension == ".wav":
                    filepath = os.path.join(root, f)
                    subdirs = filepath.replace(folder_path, "")
                    subdirs_re = re.sub("[^a-z^A-Z^0-9]", " ", subdirs)
                    name_re = re.sub("[^a-z^A-Z^0-9]", " ", name)
                    tags += subdirs_re.lower().split(" ")
                    tags += name_re.lower().split(" ")

                    item = {
                        "Title" : name,
                        "Description" : "",
                        "FileName" : filepath.replace("/", "\\"),
                        "Keywords" : tags,
                        "Time" : ""
                    }

                    items.append(item)

                progress += progress_jump
                progress_out = round(progress)

                if progress_function: progress_function(progress_out)

                if progress_out % 5 == 0 or progress_out == 1:
                    Logger.console_progress_bar(f"Processing {folder_path} : ", f" {progress_out}%", progress_out, 20)

    sys.stdout.write("\n")

    output_filename = os.path.basename(folder_path) + ".json"
    output_file = os.path.join(database_path, output_filename.lower())

    with open(output_file, "w") as f:
        json.dump(items, f, indent=2)