@echo off

start cmd /k "cd ./frontend && yarn start"

start cmd /k "cd ./backend && cd ./SNU_venv/Scripts && activate && cd ../../ && python main.py"