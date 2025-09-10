@echo off
cd %~dp0
python organize_files.py
python strategist_agent.py
pause