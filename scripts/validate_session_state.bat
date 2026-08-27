@echo off
setlocal
set PYTHONIOENCODING=utf-8
python "%~dp0validate_session_state.py" %*
exit /b %ERRORLEVEL%
