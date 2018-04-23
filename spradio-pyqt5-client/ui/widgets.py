#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Custom widgets for Innkeeper's main window.
'''

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QGroupBox, QHBoxLayout,
                             QPushButton, QSizePolicy, QSpacerItem, QTableView,
                             QVBoxLayout, QWidget)

from .models.radio import (AlbumTableModel, ArtistTableModel, GameTableModel,
                           SongTableModel)


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
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout' +
                                            plural.capitalize())

        self.buttonRefresh = QPushButton(self)
        self.buttonRefresh.setObjectName('buttonRefresh' +
                                         self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/refresh.svg"), QIcon.Normal, QIcon.On)
        self.buttonRefresh.setIcon(icon)
        self.buttonRefresh.setFlat(True)
        spacer = QSpacerItem(40, 20,
                             QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setObjectName('buttonAdd' + self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/add-outline.svg"),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonAdd.setIcon(icon)
        self.buttonAdd.setFlat(True)
        self.buttonEdit = QPushButton(self)
        self.buttonEdit.setObjectName('buttonEdit' + self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/edit-pencil.svg"),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonEdit.setIcon(icon)
        self.buttonEdit.setFlat(True)
        self.buttonDelete = QPushButton(self)
        self.buttonDelete.setObjectName('buttonDelete' + plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/minus-outline.svg"),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonDelete.setIcon(icon)
        self.buttonDelete.setFlat(True)

        self.horizontalLayout.addWidget(self.buttonRefresh)
        self.horizontalLayout.addItem(spacer)
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonEdit)
        self.horizontalLayout.addWidget(self.buttonDelete)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        '''Translate labels into the native OS language.'''
        _ = QCoreApplication.translate

        # Group Box header
        self.setTitle(_('Client', self.plural.capitalize()))


class AlbumGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating albums.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='album', plural='albums', vstretch=1)

        self.model = AlbumTableModel(parent=self, name='albums')
        self.tableView.setModel(self.model)


class ArtistGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating artists.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='artist', plural='artists', vstretch=2)

        self.model = ArtistTableModel(parent=self, name='artists')
        self.tableView.setModel(self.model)


class GameGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating games.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='game', plural='games', vstretch=1)

        self.model = GameTableModel(parent=self, name='games')
        self.tableView.setModel(self.model)


class SongGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating songs.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='song', plural='songs', hstretch=2)

        self.model = SongTableModel(parent=self, name='songs')
        self.tableView.setModel(self.model)


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
        self.groupBoxArtists = ArtistGroupBox(self)
        self.groupBoxAlbums = AlbumGroupBox(self)
        self.groupBoxGames = GameGroupBox(self)
        self.groupBoxSongs = SongGroupBox(self)

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
