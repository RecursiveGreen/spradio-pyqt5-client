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


class ArtistDialog(QDialog):
    '''
    Dialog object for an artist item.
    '''
    def __init__(self, **kwargs):
        super().__init__()

        self.modified = False
        self.original = {}
        self.original['id'] = kwargs.get('id', '')
        self.original['first_name'] = kwargs.get('first_name', '')
        self.original['alias'] = kwargs.get('alias', '')
        self.original['last_name'] = kwargs.get('last_name', '')

        self.initUi()
        self.resetValues()

    def initUi(self):
        self.setObjectName('dialogArtist')
        self.resize(450, 300)
        self.setMinimumSize(QSize(255, 165))
        self.setMaximumSize(QSize(450, 300))

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName('verticalLayoutArtist')

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName('formLayoutArtist')

        # Id
        self.labelId = QLabel(self)
        self.labelId.setObjectName('labelIdArtist')
        self.labelIdValue = QLabel(self)
        self.labelIdValue.setObjectName('labelIdValueArtist')
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelId)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.labelIdValue)

        # Spacer 1
        spacer_1 = QSpacerItem(20, 40,
                               QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(1, QFormLayout.FieldRole, spacer_1)

        # First Name
        self.labelFirstName = QLabel(self)
        self.labelFirstName.setObjectName('labelFirstNameArtist')
        self.lineEditFirstName = QLineEdit(self)
        self.lineEditFirstName.setObjectName('lineEditFirstNameArtist')
        self.formLayout.setWidget(2,
                                  QFormLayout.LabelRole,
                                  self.labelFirstName)
        self.formLayout.setWidget(2,
                                  QFormLayout.FieldRole,
                                  self.lineEditFirstName)

        # Spacer 2
        spacer_2 = QSpacerItem(20, 40,
                               QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(3, QFormLayout.FieldRole, spacer_2)

        # Alias
        self.labelAlias = QLabel(self)
        self.labelAlias.setObjectName('labelAliasArtist')
        self.lineEditAlias = QLineEdit(self)
        self.lineEditAlias.setObjectName('lineEditAliasArtist')
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelAlias)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEditAlias)

        # Spacer 3
        spacer_3 = QSpacerItem(20, 40,
                               QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(5, QFormLayout.FieldRole, spacer_3)

        # Last Name
        self.labelLastName = QLabel(self)
        self.labelLastName.setObjectName('labelLastNameArtist')
        self.lineEditLastName = QLineEdit(self)
        self.lineEditLastName.setObjectName('lineEditLastNameArtist')
        self.formLayout.setWidget(6,
                                  QFormLayout.LabelRole,
                                  self.labelLastName)
        self.formLayout.setWidget(6,
                                  QFormLayout.FieldRole,
                                  self.lineEditLastName)

        # Spacer 4
        spacer_4 = QSpacerItem(20, 40,
                               QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(7, QFormLayout.FieldRole, spacer_4)

        self.lineEditFirstName.textEdited.connect(self.textModified)
        self.lineEditAlias.textEdited.connect(self.textModified)
        self.lineEditLastName.textEdited.connect(self.textModified)

        # Button Box
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName('buttonBoxArtist')
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Reset)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        apply = self.buttonBox.button(QDialogButtonBox.Apply)
        apply.clicked.connect(self.saveArtist)
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
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        if self.original['id'] == '':
            font.setItalic(True)
            self.labelIdValue.setText('[NOT CREATED YET]')
        else:
            self.labelIdValue.setText(str(self.original['id']))
        self.labelIdValue.setFont(font)
        self.lineEditFirstName.setText(self.original['first_name'])
        self.lineEditAlias.setText(self.original['alias'])
        self.lineEditLastName.setText(self.original['last_name'])

        self.modified = False
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

    def saveArtist(self):
        current_data = {}
        current_data['first_name'] = self.lineEditFirstName.text()
        current_data['alias'] = self.lineEditAlias.text()
        current_data['last_name'] = self.lineEditLastName.text()

        if self.original['id'] == '':
            status, results = post_server_data('artists', current_data)
            current_data['id'] = results['id']
        else:
            current_data['id'] = self.original['id']
            status, results = put_server_data('artists/' +
                                              str(current_data['id']),
                                              current_data)

        if status in [200, 201]:
            self.original = current_data
            self.resetValues()
            self.modified = False
            self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

    def accept(self):
        self.saveArtist()
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def retranslateUi(self):
        '''Translate labels into native language and assign them to widgets.'''
        _ = QCoreApplication.translate

        # Dialog title
        self.setWindowTitle(_('Client', 'Edit Artist'))

        self.labelId.setText(_('Client', 'Id:'))
        self.labelFirstName.setText(_('Client', 'First Name:'))
        self.labelAlias.setText(_('Client', 'Alias:'))
        self.labelLastName.setText(_('Client', 'Last Name:'))
