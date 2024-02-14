@REM Script to Activate/Deactivate Python venv

@echo off
set virtual_env_name="test"

if NOT "%VIRTUAL_ENV%" == "" (
    call %virtual_env_name%\Scripts\deactivate.bat
    exit /b
)
if exist %virtual_env_name%\ (
    call %virtual_env_name%\Scripts\activate.bat
) else (
    call py -m venv %virtual_env_name%
    call %virtual_env_name%\Scripts\activate.bat
)
