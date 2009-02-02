# Simple application example from:
#   http://doc.trolltech.com/4.0/mainwindows-application.html
#
# Process this file with
#   QMAKESPEC=fedora-win32-cross qmake-qt4 -win32 example.pro
# and then run 'make'.

TEMPLATE        = app
TARGET          = example

CONFIG          += qt warn_on

HEADERS         = mainwindow.h
SOURCES         = mainwindow.cpp main.cpp

RESOURCES       += application.qrc
