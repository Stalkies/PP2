@echo off
REM Активируем виртуальное окружение
call venv\Scripts\activate.bat

REM Запускаем скрипт main.py
python main.py

REM Деактивируем виртуальное окружение (необязательно)
deactivate

pause