import sys, os, time
from datetime import datetime


def __init():
    pass


class Logger():
    # Utility class to log informations to the user
    
    @staticmethod
    def message(input):
        # Outputs an information
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        sys.stdout.write(f"{current_time} [INFO] : {input}\n")

    @staticmethod
    def warning(input):
        # Outputs a warning
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        sys.stdout.write(f"{current_time} [WARNING] : {input}\n")

    @staticmethod
    def error(input):
        # Outputs an error
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        sys.stderr.write(f"{current_time} [ERROR] : {input}\n")

    @staticmethod
    def console_progress_bar(prefix, suffix, progress, length):
        # Prints a progress bar to the console
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        iter = int(progress * length / 100.0)

        bar = f"\r{current_time} [INFO] : {prefix}[{(('#' * iter) + (' ' * (length - iter)))}]{suffix}"
        if iter == length : bar += "\n"

        sys.stdout.write(bar)

    @staticmethod
    def waiting_wheel():
        # Prints a waiting wheel to the console \-/

        def spinning_cursor():
            while True:
                for cursor in "\\|/-":
                    yield cursor

        spinner = spinning_cursor()

        for i in range(0, 4):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write("\b")

    @staticmethod
    def waiting_message(input):
        # Prints message with a spinning wheel
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        def spinning_cursor():
            while True:
                for cursor in "\\|/-":
                    yield cursor

        spinner = spinning_cursor()

        for i in range(0, 4):
            sys.stdout.write("%s [INFO] : " % current_time + input + " " + next(spinner))
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write("\r")
