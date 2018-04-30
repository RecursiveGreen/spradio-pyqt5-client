#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Custom widgets for Innkeeper's main window.
'''

from PyQt5.QtCore import pyqtSlot, QCoreApplication, QItemSelection, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QGroupBox,
                             QHBoxLayout, QHeaderView, QLabel, QMessageBox,
                             QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
                             QTableView, QVBoxLayout, QWidget)

from .dialogs.radio import BaseItemDialog
from .models.radio import (AlbumTableModel, ArtistTableModel, GameTableModel,
                           SongTableModel)
from .utils import delete_server_data


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
                 paginate=False,
                 name='',
                 plural='',
                 hstretch=0,
                 vstretch=0):
        super().__init__(parent)

        self.paginate = paginate

        self.name = name
        self.plural = plural
        self.columns = {}

        self.current_selection = None

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

        self.horizontalLayout.addWidget(self.buttonRefresh)
        self.horizontalLayout.addItem(spacerLeft)

        if self.paginate:
            self.initPagination()

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
        self.buttonDelete.setEnabled(False)

        self.horizontalLayout.addWidget(self.buttonAdd)
        self.horizontalLayout.addWidget(self.buttonEdit)
        self.horizontalLayout.addWidget(self.buttonDelete)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonRefresh.clicked.connect(self.updateTable)
        self.buttonAdd.clicked.connect(self.showDialog)
        self.buttonEdit.clicked.connect(self.showDialog)
        self.buttonDelete.clicked.connect(self.deleteItem)

        self.retranslateUi()

    def initPagination(self):
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

        self.horizontalLayout.addWidget(self.buttonFirstPage)
        self.horizontalLayout.addWidget(self.buttonPreviousPage)
        self.horizontalLayout.addWidget(self.spinBoxCurrentPage)
        self.horizontalLayout.addWidget(self.labelTotalPages)
        self.horizontalLayout.addWidget(self.buttonNextPage)
        self.horizontalLayout.addWidget(self.buttonLastPage)
        self.horizontalLayout.addItem(spacerRight)

        self.buttonFirstPage.clicked.connect(self.updatePages)
        self.buttonPreviousPage.clicked.connect(self.updatePages)
        self.spinBoxCurrentPage.valueChanged.connect(self.updatePages)
        self.buttonNextPage.clicked.connect(self.updatePages)
        self.buttonLastPage.clicked.connect(self.updatePages)

    @pyqtSlot(QItemSelection)
    def selectRadioItems(self, item=QItemSelection()):
        if not item.indexes():
            self.buttonEdit.setEnabled(False)
            self.buttonDelete.setEnabled(False)
            self.current_selection = None
        else:
            self.buttonEdit.setEnabled(True)
            self.buttonDelete.setEnabled(True)
            self.current_selection = self.model.rowData(item.indexes()[0])

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

    @pyqtSlot()
    def updateTable(self):
        '''
        Updates the data within the table view from the server. Also refreshes
        the page controls to reflect the current position.
        '''
        if self.paginate:
            self.model.current_page = self.spinBoxCurrentPage.value()
        
        self.model.updateData()
        self.resizeColumns()

        self.tableView.clearSelection()
        self.current_selection = None

        if self.paginate:
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

    def resizeColumns(self):
        '''Automatically resizes table columns to fit new data.'''
        header = self.tableView.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def showDialog(self):
        if self.sender().objectName().startswith('buttonEdit'):
            dialog = BaseItemDialog(self, **self.current_selection)
        else:
            dialog = BaseItemDialog(self)
        dialog.exec_()
        self.updateTable()

    def deleteItem(self):
        should_delete = QMessageBox.question(self,
                                             'Delete ' + self.name,
                                             ('Are you sure you wish to delete'
                                              ' this ' + self.name + '?'),
                                             QMessageBox.Yes |
                                             QMessageBox.No,
                                             QMessageBox.No)
        if should_delete == QMessageBox.Yes:
            endpoint = self.plural + '/' + str(self.current_selection['id'])
            status, results = delete_server_data(endpoint)
            self.updateTable()

    def retranslateUi(self):
        '''Translate labels into the native OS language.'''
        _ = QCoreApplication.translate

        # Group Box header
        self.setTitle(_('Client', self.plural.capitalize()))


class AlbumGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating albums.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='album', plural='albums', vstretch=1)

        self.columns = {'id': {'header': 'ID',
                               'visible': False,
                               'editable': False},
                        'title': {'header': 'Title',
                                  'visible': True,
                                  'editable': True}}

        self.model = AlbumTableModel(self)
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class ArtistGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating artists.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='artist', plural='artists', vstretch=2)

        self.columns = {'id': {'header': 'ID',
                               'visible': False,
                               'editable': False},
                        'first_name': {'header': 'First Name',
                                       'visible': True,
                                       'editable': True},
                        'alias': {'header': 'Alias',
                                  'visible': True,
                                  'editable': True},
                        'last_name': {'header': 'Last Name',
                                      'visible': True,
                                      'editable': True}}

        self.model = ArtistTableModel(self)
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class GameGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating games.'''
    def __init__(self, parent=None):
        super().__init__(parent, name='game', plural='games', vstretch=1)

        self.columns = {'id': {'header': 'ID',
                               'visible': False,
                               'editable': False},
                        'title': {'header': 'Title',
                                  'visible': True,
                                  'editable': True}}

        self.model = GameTableModel(self)
        self.tableView.setModel(self.model)
        selection_model = self.tableView.selectionModel()
        selection_model.selectionChanged.connect(self.selectRadioItems)
        self.updateTable()


class SongGroupBox(BaseItemGroupBox):
    '''A GroupBox for administrating songs.'''
    def __init__(self, parent=None):
        super().__init__(parent,
                         paginate=True,
                         name='song',
                         plural='songs',
                         hstretch=3)

        self.columns = {'id': {'header': 'ID',
                               'visible': False,
                               'editable': False},
                        'album': {'header': 'Album',
                                  'visible': True,
                                  'editable': True},
                        'artists': {'header': 'Artists',
                                    'visible': True,
                                    'editable': True},
                        'game': {'header': 'Game',
                                 'visible': True,
                                 'editable': True},
                        'song_type': {'header': 'Type',
                                      'visible': True,
                                      'editable': False},
                        'title': {'header': 'Title',
                                  'visible': True,
                                  'editable': True},
                        'num_played': {'header': 'Times played',
                                       'visible': False,
                                       'editable': False},
                        'last_played': {'header': 'Last played',
                                        'visible': False,
                                        'editable': False},
                        'length': {'header': 'Length',
                                   'visible': False,
                                   'editable': False},
                        'path': {'header': 'File path',
                                 'visible': False,
                                 'editable': True}}

        self.model = SongTableModel(self)
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
