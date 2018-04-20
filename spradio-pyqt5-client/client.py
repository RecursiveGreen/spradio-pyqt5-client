#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Innkeeper
Copyright (C) 2018 Josh Washburne

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import traceback

from PyQt5.QtCore import QCoreApplication, qFatal, QT_VERSION
from PyQt5.QtWidgets import QApplication

from ui.mainwindow import Client


ORGANIZATION_NAME = 'Save Point Radio'
ORGANIZATION_DOMAIN = 'savepointradio.net'
APPLICATION_NAME = 'Innkeeper'

# Globals are not fun, but this is to prevent random crashes when exiting.
# http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
app = None

# PyQt5 doesn't always get the entire traceback out to the terminal before
# crashing. This gets around that.
# https://stackoverflow.com/questions/44447674/
if QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        qFatal('')
sys.excepthook = excepthook


def main():
    ''' Main loop for the Innkeeper application.'''
    global app

    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
