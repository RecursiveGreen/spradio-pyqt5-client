#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Data models used within the application for the radio playlist.
'''

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from ..utils import full_name, get_server_data


class BaseRadioModel(QAbstractTableModel):
    '''Base data model to represent radio items.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name = parent.plural
        self.columns = {k: v['header'] for (k, v) in parent.columns.items()
                        if v['visible']}
        self.paginate = parent.paginate

        self._data = []
        self.current_page = 1
        self.total_pages = 1

    def updateData(self):
        if self.paginate:
            status, results = get_server_data(self.name, self.current_page)
            self._data = results['results']
            self.total_pages = results['total_pages']
        else:
            all_items = []
            status, results = get_server_data(self.name, 1)
            all_items += results['results']
            for x in range(2, results['total_pages'] + 1):
                status, results = get_server_data(self.name, x)
                all_items += results['results']
            self._data = all_items
        self.updateLayout()

    def updateLayout(self):
        '''
        Force the view to refresh itself after the data has been changed.
        '''
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

    def rowData(self, index):
        if index.isValid():
            return self._data[index.row()]
        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return list(self.columns.values())[col]
        return None


class ArtistTableModel(BaseRadioModel):
    '''Data model to represent artists on the radio.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.columns = {'full_name': 'Full Name'}

    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                return full_name(self._data[index.row()])
        return None


class AlbumTableModel(BaseRadioModel):
    '''Data model to represent albums on the radio.'''
    pass


class GameTableModel(BaseRadioModel):
    '''Data model to represent games on the radio.'''
    pass


class SongTableModel(BaseRadioModel):
    '''Data model to represent songs on the radio.'''
    def data(self, index, role):
        if index.isValid():
            if (role == Qt.DisplayRole) or (role == Qt.EditRole):
                attr_name = list(self.columns.keys())[index.column()]
                row = self._data[index.row()]
                if row[attr_name] is not None:
                    if attr_name == 'game' or attr_name == 'album':
                        return row[attr_name]['title']
                    elif attr_name == 'artists':
                        artists = ', '.join([full_name(a)
                                             for a in row['artists']])
                        return artists
                    return row[attr_name]
        return None
