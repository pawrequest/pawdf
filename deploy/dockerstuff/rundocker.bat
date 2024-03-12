@echo off
docker run -v "R:/Parcelforce Labels:/data" array_pdf print_array "/data/shiplabel.pdf"
pause

