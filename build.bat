@echo off

rem build the executable with pyinstaller

set pyinstaller=""

rem find pyinstaller
for /F "tokens=* USEBACKQ" %%F in (`where pyinstaller.exe`) do (
    set pyinstaller=%%F
)

"%pyinstaller%" app.py --onefile --name ENSISoundFinder