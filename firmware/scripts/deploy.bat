REM Meant to launch new code on connected RPi 2040
REM Expected arguments: Folder containing python code. 
REM @echo off

ren D:\code.py D:\old_code.py
ren D:\boot.py D:\old_boot.py

copy %1\code.py D:\
copy %1\boot.py D:\