#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Custom widgets for Innkeeper's main window.
'''

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QPushButton, QSizePolicy,
                             QSpacerItem, QTableView, QVBoxLayout, QWidget)


class BaseItemGroupBox(QGroupBox):
    '''A GroupBox for administrating an item.'''
    def __init__(self,
                 parent=None,
                 name='',
                 plural='',
                 hstretch=0,
                 vstretch=0):
        super().__init__(parent)
        self.name = name
        self.plural = plural

        self.setObjectName('groupBox' + self.plural.capitalize())

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout' +
                                          self.plural.capitalize())
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)

        self.tableView = QTableView(self)
        self.tableView.setObjectName('tableView' + self.plural.capitalize())
        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout' +
                                            plural.capitalize())

        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setObjectName('buttonAdd' + self.plural.capitalize())
        spacerLeft = QSpacerItem(40,
                                 20,
                                 QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self.buttonEdit = QPushButton(self)
        self.buttonEdit.setObjectName('buttonEdit' + self.plural.capitalize())
        spacerRight = QSpacerItem(40,
                                  20,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.buttonDelete = QPushButton(self)
        self.buttonDelete.setObjectName('buttonDelete' + plural.capitalize())

        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addItem(spacerLeft)
        self.horizontalLayout.addWidget(self.buttonEdit)
        self.horizontalLayout.addItem(spacerRight)
        self.horizontalLayout.addWidget(self.buttonDelete)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        '''Translate labels into the native OS language.'''
        _ = QCoreApplication.translate

        # Group Box header
        self.setTitle(_('Client', self.plural.capitalize()))

        # Button labels
        self.buttonAdd.setText(_('Client', 'Add ' + self.name.capitalize()))
        self.buttonEdit.setText(_('Client', 'Edit ' + self.name.capitalize()))
        self.buttonDelete.setText(_('Client',
                                    'Delete ' + self.name.capitalize()))


class PlaylistTab(QWidget):
    '''A widget for administrating the all models of the playlist data.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('tabPlaylist')
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayoutPlaylist")
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setSpacing(6)

        # Artists/Albums/Games Layout Widget
        self.verticalWidget = QWidget(self)
        self.verticalWidget.setObjectName('verticalWidgetPlaylist')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget
                                     .sizePolicy()
                                     .hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName('verticalLayoutPlaylist')
        self.verticalLayout.setContentsMargins(0, 0, 1, 0)
        self.verticalLayout.setSpacing(1)
        self.horizontalLayout.addWidget(self.verticalWidget)

        # Create the group box widgets for the playlist items
        self.groupBoxArtists = BaseItemGroupBox(self.verticalWidget,
                                                name='artist',
                                                plural='artists',
                                                vstretch=2)
        self.groupBoxAlbums = BaseItemGroupBox(self.verticalWidget,
                                               name='album',
                                               plural='albums',
                                               vstretch=1)
        self.groupBoxGames = BaseItemGroupBox(self.verticalWidget,
                                              name='game',
                                              plural='games',
                                              vstretch=1)
        self.groupBoxSongs = BaseItemGroupBox(self.verticalWidget,
                                              name='song',
                                              plural='songs',
                                              hstretch=2)

        # Add group boxes to layouts
        self.verticalLayout.addWidget(self.groupBoxArtists)
        self.verticalLayout.addWidget(self.groupBoxAlbums)
        self.verticalLayout.addWidget(self.groupBoxGames)

        self.horizontalLayout.addWidget(self.groupBoxSongs)


class ControlsTab(QWidget):
    '''A widget for controlling playback on the radio station.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('tabControls')
