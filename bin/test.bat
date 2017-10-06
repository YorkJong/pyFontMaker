@echo off
set fontmaker=..\fontmaker\fontmaker.py


set outfile=filename.lst
echo =^> Generate a filename list file (%outfile%).
%fontmaker% name -o%outfile% char.lst

set name=%outfile%
set chars=char.lst
set font=arial.ttf

set dir=fore
echo =^> Generate font picture of only foreground.
%fontmaker% fore -n%name% -d%dir% -cGreen -f%font% -s40 -H %chars%

set dir=edge
echo =^> Generate font pictures with 1-pixel edge.
%fontmaker% edge -n%name% -d%dir% -cRed -eGreen -f%font% -s40 %chars%

set dir=shadow11
echo =^> Generate font pictures with 1x1 shadow.
%fontmaker% shadow11 -n%name% -d%dir% -cRed -eGreen -f%font% -s40 %chars%

set dir=shadow21
echo =^> Generate font pictures with 2x1 shadow.
%fontmaker% shadow21 -n%name% -d%dir% -cRed -eGreen -f%font% -s40 %chars%

pause
