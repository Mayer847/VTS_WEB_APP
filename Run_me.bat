@echo off

:: vts.py location
cd

::open local host on default browser
::open http://127.0.0.1:5000/
start "" "http://127.0.0.1:5000/"

:: run vts.py
python -m flask --app vts.py run

