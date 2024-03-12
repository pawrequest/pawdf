@echo off
SETLOCAL

REM Check if a file path argument was provided
IF "%~1"=="" (
    echo Usage: %0 [PDF_FILE_PATH]
    goto :EOF
)

REM Navigate to the deploy directory
cd /d "C:\Users\giles\prdev\array_pdf\deploy"

REM Create a temporary env file in the deploy directory
echo INPUT_FILE_PATH=%~1 > temp.env

REM Pass the env file to docker-compose, referencing it in the current directory
docker-compose --env-file temp.env up

REM Cleanup the temp env file in the deploy directory
del temp.env

ENDLOCAL
