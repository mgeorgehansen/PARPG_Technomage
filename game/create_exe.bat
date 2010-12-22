@echo off
python setup_exe.py py2exe
Rem remove directories created by p2exe for temporary storing
rmdir build /S /q
pause
echo on