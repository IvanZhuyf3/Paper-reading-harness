@echo off
setlocal
set PYTHONIOENCODING=utf-8
python "%~dp0validate_paper_model.py" %*
exit /b %ERRORLEVEL%
