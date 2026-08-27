@echo off
setlocal
set PYTHONIOENCODING=utf-8
python "%~dp0render_session_markdown.py" %*
exit /b %ERRORLEVEL%
