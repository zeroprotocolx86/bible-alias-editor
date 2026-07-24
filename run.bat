@echo off
chcp 65001 >nul
title Bible Alias Database Editor
echo Запуск редактора Біблійний Аліас...
echo Відкрийте браузер: http://localhost:8501
streamlit run app.py
pause
