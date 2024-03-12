@echo off
SETLOCAL

REM Check if a file path argument was provided
IF "%~1"=="" (
    echo Usage: %0 [PDF_FILE_PATH]
    goto :EOF
)

SET INPUT_FILE_PATH=%~1

cd /d "C:\Users\giles\prdev\array_pdf\deploy"

docker-compose up

ENDLOCAL
