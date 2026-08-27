@echo off
setlocal
set PYTHONIOENCODING=utf-8
python -m unittest scripts\test_session_state.py > verification\2026-08-27_session_tests.txt 2>&1
exit /b %ERRORLEVEL%
