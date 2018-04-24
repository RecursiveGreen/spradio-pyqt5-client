#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Custom widgets for Innkeeper's main window.
'''

from PyQt5.QtCore import pyqtSlot, QCoreApplication, QItemSelection, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QGroupBox,
                             QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QSpacerItem, QSpinBox, QTableView, QVBoxLayout,
                             QWidget)

from .models.radio import (AlbumTableModel, ArtistTableModel, GameTableModel,
                           SongTableModel)


class DeselectableTableView(QTableView):
    '''
    Custom Table View that allows deselecting items if clicking on the
    whitespace area outside of the table.

    (Thanks to https://stackoverflow.com/questions/2761284/)
    '''
    def mousePressEvent(self, event):
        self.clearSelection()
        QTableView.mousePressEvent(self, event)


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

        self.tableView = DeselectableTableView(self)
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
        icon.addPixmap(QPixmap(':/icons/refresh.svg'), QIcon.Normal, QIcon.On)
        self.buttonRefresh.setIcon(icon)
        self.buttonRefresh.setFlat(True)
        spacerLeft = QSpacerItem(40, 20,
                                 QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonFirstPage = QPushButton(self)
        self.buttonFirstPage.setObjectName('buttonFirstPage' +
                                           self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/arrow-thin-left.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonFirstPage.setIcon(icon)
        self.buttonFirstPage.setFlat(True)
        self.buttonFirstPage.setEnabled(False)
        self.buttonPreviousPage = QPushButton(self)
        self.buttonPreviousPage.setObjectName('buttonPreviousPage' +
                                              self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/cheveron-left.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonPreviousPage.setIcon(icon)
        self.buttonPreviousPage.setFlat(True)
        self.buttonPreviousPage.setEnabled(False)
        self.spinBoxCurrentPage = QSpinBox(self)
        self.spinBoxCurrentPage.setObjectName('spinBoxCurrentPage' +
                                              self.plural.capitalize())
        self.spinBoxCurrentPage.setMaximumSize(QSize(30, 16777215))
        self.spinBoxCurrentPage.setAlignment(Qt.AlignCenter)
        self.spinBoxCurrentPage.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxCurrentPage.setMinimum(1)
        self.spinBoxCurrentPage.setMaximum(9999)

        self.labelTotalPages = QLabel(self)
        self.labelTotalPages.setObjectName('labelTotalPages' +
                                           self.plural.capitalize())
        self.labelTotalPages.setMaximumSize(QSize(40, 16777215))
        self.labelTotalPages.setText('/ ----')

        self.buttonNextPage = QPushButton(self)
        self.buttonNextPage.setObjectName('buttonNextPage' +
                                          self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/cheveron-right.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonNextPage.setIcon(icon)
        self.buttonNextPage.setFlat(True)
        self.buttonLastPage = QPushButton(self)
        self.buttonLastPage.setObjectName('buttonLastPage' +
                                          self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/arrow-thin-right.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonLastPage.setIcon(icon)
        self.buttonLastPage.setFlat(True)
        spacerRight = QSpacerItem(40, 20,
                                  QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setObjectName('buttonAdd' + self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/add-outline.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonAdd.setIcon(icon)
        self.buttonAdd.setFlat(True)
        self.buttonEdit = QPushButton(self)
        self.buttonEdit.setObjectName('buttonEdit' + self.plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/edit-pencil.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonEdit.setIcon(icon)
        self.buttonEdit.setFlat(True)
        self.buttonEdit.setEnabled(False)
        self.buttonDelete = QPushButton(self)
        self.buttonDelete.setObjectName('buttonDelete' + plural.capitalize())
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/minus-outline.svg'),
                       QIcon.Normal,
                       QIcon.On)
        self.buttonDelete.setIcon(icon)
        self.buttonDelete.setFlat(True)

        self.horizontalLayout.addWidget(self.buttonRefresh)
        self.horizontalLayout.addItem(spacerLeft)
        self.horizontalLayout.addWidget(self.buttonFirstPage)
        self.horizontalLayout.addWidget(self.buttonPreviousPage)
        self.horizontalLayout.addWidget(self.spinBoxCurrentPage)
        self.horizontalLayout.addWidget(self.labelTotalPages)
        self.horizontalLayout.addWidget(self.buttonNextPage)
        self.horizontalLayout.addWidget(self.buttonLastPage)
        self.horizontalLayout.addItem(spacerRight)
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonEdit)
        self.horizontalLayout.addWidget(self.buttonDelete)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonFirstPage.clicked.connect(self.updatePages)
        self.buttonPreviousPage.clicked.connect(self.updatePages)
        self.spinBoxCurrentPage.valueChanged.connect(self.updatePages)
        self.buttonNextPage.clicked.connect(self.updatePages)
        self.buttonLastPage.clicked.connect(self.updatePages)

        self.retranslateUi()

    @pyqtSlot(QItemSelection)
    def selectRadioItems(self, item=QItemSelection()):
        if not item.indexes():
            self.buttonEdit.setEnabled(False)
        else:
            self.buttonEdit.setEnabled(True)

    @pyqtSlot()
    def updatePages(self, *args, **kwargs):
        '''Updates the current page spinbox and updates data if necessary.'''
        sender = self.sender().objectName()
        minimum = self.spinBoxCurrentPage.minimum()
        current = self.spinBoxCurrentPage.value()
        maximum = self.spinBoxCurrentPage.maximum()

        if sender.startswith('buttonFirstPage'):
            self.spinBoxCurrentPage.setValue(minimum)
        elif sender.startswith('buttonPreviousPage'):
            if current > minimum:
                self.spinBoxCurrentPage.setValue(current - 1)
        elif sender.startswith('spinBoxCurrentPage'):
            self.updateTable()
        elif sender.startswith('buttonNextPage'):
            if current < maximum:
                self.spinBoxCurrentPage.setValue(current + 1)
        elif sender.startswith('buttonLastPage'):
            self.spinBoxCurrentPage.setValue(maximum)

    def updateTable(self):
        '''
        Updates the data within the table view from the server. Also refreshes
        the page controls to reflect the current position.
        '''
        self.model.current_page = self.spinBoxCurrentPage.value()
        self.model.updateData()

        current = self.model.current_page
        total = self.model.total_pages
        begin = bool(current != 1)
        end = bool(current != total)

        self.buttonFirstPage.setEnabled(begin)
        self.buttonPreviousPage.setEnabled(begin)
        self.spinBoxCurrentPage.setMaximum(total)
        self.labelTotalPages.setText('/ ' + str(total))
        self.buttonNextPage.setEnabled(end)
        self.buttonLastPage.setEnabled(end)

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
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class ArtistGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating artists.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='artist', plural='artists', vstretch=2)

        self.model = ArtistTableModel(parent=self, name='artists')
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class GameGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating games.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='game', plural='games', vstretch=1)

        self.model = GameTableModel(parent=self, name='games')
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class SongGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating songs.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='song', plural='songs', hstretch=2)

        self.model = SongTableModel(parent=self, name='songs')
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


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
