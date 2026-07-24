@echo off
chcp 65001 >nul
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo Cleaning old builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

echo Building BibleAliasEditor.exe...
pyinstaller --onefile --name "BibleAliasEditor" --icon "icon.ico" ^
  --add-data "data;data" --add-data "app.py;." ^
  --hidden-import streamlit --hidden-import tkinter --collect-all streamlit --collect-all tkinter launcher.py

echo Done! Output: dist\BibleAliasEditor.exe
pause
