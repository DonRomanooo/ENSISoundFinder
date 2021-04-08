@echo off

rem build the executable with pyinstaller

set pyinstaller=""

rem find pyinstaller
for /F "tokens=* USEBACKQ" %%F in (`where pyinstaller.exe`) do (
    set pyinstaller=%%F
)

set /p buildver="Enter build version : "

"%pyinstaller%" app.py --onefile --name ENSISoundFinder_%buildver%