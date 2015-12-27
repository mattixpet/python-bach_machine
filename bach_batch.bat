:: run multiple parallel instances of bach.bat for maximum chordage
@echo off

set N=4
for /L %%i in (1,1,%N%) do (
  start bach.bat
)