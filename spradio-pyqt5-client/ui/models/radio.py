#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Data models used within the application for the radio playlist.
'''

import keyring

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QSettings, Qt
from PyQt5.QtWidgets import qApp

import requests

from ..utils import full_name


class BaseRadioModel(QAbstractTableModel):
    '''Base data model to represent radio items.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = ''
        self.columns = {}

        self._data = []
        self.current_page = 1
        self.total_pages = 1

    def updateData(self):
        settings = QSettings()
        base_url = settings.value('server/api_base_url', type=str)
        url = base_url + self.name + '/?page=' + str(self.current_page)
        password = 'Token ' + keyring.get_password(qApp.applicationName(),
                                                   'Token')
        headers = {'content-type': 'application/json',
                   'authorization': password}
        req = requests.get(url, headers=headers)
        self._data = req.json()['results']
        self.total_pages = req.json()['total_pages']

        # Force the view to refresh itself after the data has been changed.
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(0),
                                               self.columnCount(0)))
        self.layoutChanged.emit()

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                attr_name = list(self.columns.keys())[index.column()]
                row = self._data[index.row()]
                return row[attr_name]
        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return list(self.columns.values())[col]
        return None


class ArtistTableModel(BaseRadioModel):
    '''Data model to represent artists on the radio.'''
    def __init__(self, parent=None, name='artists'):
        super().__init__(parent)

        self.name = name
        self.columns = {'full_name': 'Full Name'}

    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                return full_name(self._data[index.row()])
        return None


class AlbumTableModel(BaseRadioModel):
    '''Data model to represent albums on the radio.'''
    def __init__(self, parent=None, name='albums'):
        super().__init__(parent)

        self.name = name
        self.columns = {'title': 'Title'}


class GameTableModel(BaseRadioModel):
    '''Data model to represent games on the radio.'''
    def __init__(self, parent=None, name='games'):
        super().__init__(parent)

        self.name = name
        self.columns = {'title': 'Title'}


class SongTableModel(BaseRadioModel):
    '''Data model to represent songs on the radio.'''
    def __init__(self, parent=None, name='songs'):
        super().__init__(parent)

        self.name = name
        self.columns = {'game': 'Game',
                        'album': 'Album',
                        'artists': 'Artists',
                        'title': 'Title'}

    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                attr_name = list(self.columns.keys())[index.column()]
                row = self._data[index.row()]
                if attr_name == 'game' or attr_name == 'album':
                    return row[attr_name]['title']
                elif attr_name == 'artists':
                    artists = ', '.join([full_name(a) for a in row['artists']])
                    return artists
                return row[attr_name]
        return None
