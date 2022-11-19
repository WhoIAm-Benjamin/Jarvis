@ECHO OFF
pyinstaller -F -w --distpath="." main.spec
set/p=">"