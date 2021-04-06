# ENSI Sound Finder

Small utility application made to be used at my school, Ecole des Nouvelles Images, to ease the research of sounds in our sound library.

# Install

ENSISoundFinder uses [Python3.7](https://www.python.org/downloads/release/python-370/), [PyQT5](https://pypi.org/project/PyQt5/), [PDFPlumber](https://pypi.org/project/pdfplumber/0.1.2/) and [PyInstaller](https://pypi.org/project/pyinstaller/). 

To install the program, download and use the **install.bat** program, or copy the folder named **ENSISoundFinder** that has been pushed into *W:/Ressources/ENSISoundFinder* into *C:/Program Files*.

# Documentation

When you'll run ENSISoundFinder for the first time, it will initialize its database which you can find in %APPDATA%/ENSISoundFinder/data. Do not modify it or you might corrupt it or delete sounds. If for whatever reason you think the database is not corrupted, just run *Settings/Initialize Database*.

ENSISoundFinder is made for the Ecole des Nouvelles Images sound library only, as it has been coded for its special structure. The role of this application is to find sounds that will match the tags you enter; and then you can play every sound that has been found, and copy the selected ones to your working folder.
