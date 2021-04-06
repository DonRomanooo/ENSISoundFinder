import re


def cleanup_str(string):
    # replace non alphanumerical characters with spaces
    return re.sub("[^a-z^A-Z^0-9]|(xa0)|(\\n)|(.037e)|(\W[n])", " ", string)

