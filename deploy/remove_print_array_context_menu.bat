@echo off
set VENV="R:\paul_r\.internal\.anovenv"
call %VENV%\Scripts\activate
remove-menu
call deactivate
pause
