#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Classes for the Settings Dialog.
'''

from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QLabel,
                             QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout)

from ..utils import post_server_data, put_server_data


class BaseItemDialog(QDialog):
    '''
    Abstract Dialog for all radio items.
    '''
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.modified = False
        self.structure = {}

        self.initStructure(kwargs)
        self.initUi()

    def initStructure(self, kwargs):
        for attr, item in self.parent().columns.items():
            original = kwargs.get(attr, '')
            self.structure[attr] = {}
            self.structure[attr]['original'] = original
            self.structure[attr]['widgets'] = {}
            self.structure[attr]['widgets']['label'] = QLabel(self)
            self.structure[attr]['widgets']['label'].setText(item['header'])
            if item['editable']:
                widgets = self.structure[attr]['widgets']
                widgets['field'] = QLineEdit(self)
                widgets['field'].textEdited.connect(self.textModified)
            else:
                self.structure[attr]['widgets']['field'] = QLabel(self)
            self.structure[attr]['widgets']['field'].setText(str(original))

    def initUi(self):
        name = self.parent().name.capitalize()
        self.setObjectName('dialog' + name)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayout' + name)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName('formLayout' + name)

        # Labels / Line Edits for item model.
        for attr, item in self.structure.items():
            print(attr)
            print(item)
            self.formLayout.addRow(item['widgets']['label'],
                                   item['widgets']['field'])
            spacer = QSpacerItem(20, 40,
                                 QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.formLayout.addItem(spacer)

        # Button Box
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName('buttonBox' + name)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Reset)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        apply = self.buttonBox.button(QDialogButtonBox.Apply)
        apply.clicked.connect(self.saveItem)
        apply.setEnabled(False)
        reset = self.buttonBox.button(QDialogButtonBox.Reset)
        reset.clicked.connect(self.resetValues)

        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

    def textModified(self, *args, **kwargs):
        self.modified = True
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(True)

    def resetValues(self):
        for attr, item in self.structure.items():
            if attr == 'id' and item['original'] == '':
                font = QFont()
                font.setBold(True)
                font.setWeight(75)
                font.setItalic(True)
                item['widgets']['field'].setFont(font)
                item['widgets']['field'].setText('[NEW ITEM]')
            else:
                item['widgets']['field'].setText(str(item['original']))

        self.modified = False
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

    def saveItem(self):
        endpoint = self.parent().plural
        current_data = {}
        for attr, item in self.structure.items():
            if attr is not 'id':
                current_data[attr] = item['widgets']['field'].text()

        if self.structure['id']['original'] == '':
            status, results = post_server_data(endpoint, current_data)
            current_data['id'] = results['id']
        else:
            current_data['id'] = self.structure['id']['original']
            status, results = put_server_data(endpoint + '/' +
                                              str(current_data['id']),
                                              current_data)

        if status in [200, 201]:
            for attr, item in self.structure.items():
                item['original'] = current_data[attr]
            self.resetValues()
            self.modified = False
            self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

    def accept(self):
        self.saveItem()
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def retranslateUi(self):
        '''Translate labels into native language and assign them to widgets.'''
        _ = QCoreApplication.translate
        name = self.parent().name.capitalize()

        # Dialog title
        self.setWindowTitle(_('Client', 'Edit ' + name))
