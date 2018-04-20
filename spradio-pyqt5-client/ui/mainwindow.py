#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Main Mindow UI for Innkeeper.
'''

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QAction, qApp, QGridLayout, QMainWindow,
                             QMessageBox, QTabWidget, QWidget)

from .dialogs.settings import SettingsDialog
from .widgets import ControlsTab, PlaylistTab


class Client(QMainWindow):
    '''The client Main Window.'''
    def __init__(self):
        super().__init__()
        self.initActions()
        self.initUi()

    def initActions(self):
        self.actionSettings = QAction('&Settings', self)
        self.actionSettings.setStatusTip('Change application settings')
        self.actionSettings.triggered.connect(self.showSettings)

        self.actionExit = QAction('&Exit', self)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setStatusTip('Exit application')
        self.actionExit.triggered.connect(self.close)

        self.actionAbout = QAction('About', self)
        self.actionAbout.setStatusTip('About application')
        self.actionAbout.triggered.connect(self.about)

        self.actionAboutQt = QAction('About Qt', self)
        self.actionAboutQt.setStatusTip('About Qt')
        self.actionAboutQt.triggered.connect(self.aboutQt)

    def initMenu(self):
        self.menu = self.menuBar()
        self.menuFile = self.menu.addMenu('&File')
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp = self.menu.addMenu('&Help')
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutQt)

    def initUi(self):
        '''Build all the UI components.'''

        # Main window
        self.setObjectName('windowMain')
        self.resize(1280, 800)

        # Main widget for the main window
        self.widgetMain = QWidget(parent=self)
        self.widgetMain.setObjectName('widgetMain')
        self.gridLayoutMain = QGridLayout(self.widgetMain)
        self.gridLayoutMain.setObjectName('gridLayoutMain')
        self.gridLayoutMain.setContentsMargins(0, 0, 0, 0)

        # Main tabbed widget for main widget
        self.tabWidgetMain = QTabWidget(parent=self.widgetMain)
        self.tabWidgetMain.setObjectName('tabWidgetMain')
        self.gridLayoutMain.addWidget(self.tabWidgetMain, 0, 0, 1, 1)
        self.setCentralWidget(self.widgetMain)

        # Add tabs to the main tab widget
        self.tabPlaylist = PlaylistTab()
        self.tabControls = ControlsTab()
        self.tabWidgetMain.addTab(self.tabPlaylist, '')
        self.tabWidgetMain.addTab(self.tabControls, '')

        self.statusBar()
        self.initMenu()

        self.retranslateUi()

        self.tabWidgetMain.setCurrentIndex(0)
        self.show()

    def showSettings(self):
        dialogSettings = SettingsDialog()
        dialogSettings.exec_()

    def about(self):
        QMessageBox.about(self,
                          'About ' + qApp.applicationName(),
                          ('A native desktop application for importing new '
                           'music into the Save Point Radio database.'))

    def aboutQt(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def closeEvent(self, event):
        should_exit = QMessageBox.question(self,
                                           'Exit Application',
                                           'Do you want to exit the client?',
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
        if should_exit == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def retranslateUi(self):
        '''Translate labels into native language and assign them to widgets.'''
        _ = QCoreApplication.translate
        # Main Window Title
        self.setWindowTitle(_('Client', qApp.applicationName()))

        # Tab titles
        self.tabWidgetMain \
            .setTabText(self.tabWidgetMain.indexOf(self.tabPlaylist),
                        _('Client', 'Main Playlist'))
        self.tabWidgetMain \
            .setTabText(self.tabWidgetMain.indexOf(self.tabControls),
                        _('Client', 'Radio Controls'))
