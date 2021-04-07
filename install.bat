@echo off

rem find pip and git

setlocal enabledelayedexpansion 
setlocal enableextensions

set pip=""
set git=""
set pyinstaller=""


rem find git
for /F "tokens=* USEBACKQ" %%F in (`where git.exe`) do (
    set git=%%F
) 

rem find pip
for /F "tokens=* USEBACKQ" %%F in (`where pip.exe`) do (
    echo.%%F | findstr /C:"37">nul && (set pip=%%F)
)


rem verify if pip has been found
(echo "%pip%" & echo.) | findstr /O . | more +1 | (set /P RESULT= & call exit /B %%RESULT%%)
set /A lengthpip=%ERRORLEVEL%-5

rem verify if git has been found
(echo "%git%" & echo.) | findstr /O . | more +1 | (set /P RESULT= & call exit /B %%RESULT%%)
set /A lengthgit=%ERRORLEVEL%-5

rem if pip and git found, install packages and install software

if %lengthpip% gtr 2 if %lengthgit% gtr 2 (
    %pip% install pyqt5
    %pip% install pdfplumber
    %pip% install pyinstaller

    cd %PROGRAMFILES%
    mkdir ENSISoundFinder
    cd ENSISoundFinder
    "%git%" clone "https://github.com/DonRomanooo/ENSISoundFinder.git" "git-clone"

    cd git-clone

    build

) else (
    echo [ERROR] : Python37 has not been found, please check your PATH or your Python installation
)

endlocal
