::mkdir build
::cxfreeze main.py -c -O --target-dir build
set PATH=%PATH%;C:\Working\pyinstaller-1.5.1\
::Build.py build.spec 1> analysis.txt 2> analysis.err.txt
Build.py build.spec