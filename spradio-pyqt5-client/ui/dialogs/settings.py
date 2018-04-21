#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Classes for the Settings Dialog.
'''

import keyring

from PyQt5.QtCore import QCoreApplication, QObject, QSettings, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (qApp, QDialog, QDialogButtonBox, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QSizePolicy, QStackedWidget,
                             QVBoxLayout, QWidget)

from .. import resources


class ServerSettingsWidget(QWidget):
    '''Widget for the settings involving server connectivity.'''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.initUi()
        self.loadSettings()

    def initUi(self):
        self.setObjectName('widgetServerSettings')

        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName('formLayoutServerSettings')

        self.labelApiUrl = QLabel(self)
        self.labelApiUrl.setObjectName('labelApiUrl')
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelApiUrl)
        self.lineEditApiUrl = QLineEdit(self)
        self.lineEditApiUrl.setObjectName('lineEditApiUrl')
        self.formLayout.setWidget(0,
                                  QFormLayout.FieldRole,
                                  self.lineEditApiUrl)

        self.labelApiToken = QLabel(self)
        self.labelApiToken.setObjectName('labelApiToken')
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelApiToken)
        self.lineEditApiToken = QLineEdit(self)
        self.lineEditApiToken.setEchoMode(QLineEdit.Password)
        self.lineEditApiToken.setObjectName('lineEditApiToken')
        self.formLayout.setWidget(1,
                                  QFormLayout.FieldRole,
                                  self.lineEditApiToken)

        self.lineEditApiUrl.textEdited.connect(self.modified)
        self.lineEditApiToken.textEdited.connect(self.modified)

    def loadSettings(self):
        if self.parent:
            settings = self.parent.settings
            self.lineEditApiUrl.setText(settings.value('server/api_base_url',
                                                       type=str))
            if keyring.get_password(qApp.applicationName(), 'Token'):
                # Don't put the real token in there. Fill it with fluff.
                # http://bash.org/?244321=
                self.lineEditApiToken.setText('hunter2')

    def modified(self, *args, **kwargs):
        if self.sender().objectName() not in self.parent.modified_settings:
            self.parent.modified_settings.append(self.sender().objectName())
        self.parent.buttonBox.button(QDialogButtonBox.Apply).setEnabled(True)


class SettingsDialog(QDialog):
    '''
    Dialog object for application settings.
    '''
    def __init__(self):
        super().__init__()

        self.settings = QSettings()
        self.modified_settings = []
        self.initUi()

    def initUi(self):
        self.setObjectName('dialogSettings')
        self.resize(725, 475)

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName('horizontalLayoutSettings')

        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName('listWidgetSettings')
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget
                                     .sizePolicy()
                                     .hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setSortingEnabled(False)
        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalWidget = QWidget(self)
        self.verticalWidget.setObjectName('verticalWidgetSettings')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget
                                     .sizePolicy()
                                     .hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.verticalWidget)

        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName('verticalLayoutSettings')

        self.stackedWidget = QStackedWidget(self.verticalWidget)
        self.stackedWidget.setObjectName('stackedWidgetSettings')
        self.verticalLayout.addWidget(self.stackedWidget)

        self.buttonBox = QDialogButtonBox(self.verticalWidget)
        self.buttonBox.setObjectName('buttonBoxSettings')
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox
                                     .sizePolicy()
                                     .hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        apply = self.buttonBox.button(QDialogButtonBox.Apply)
        apply.clicked.connect(self.saveSettings)
        apply.setEnabled(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.initSettingGroups()

        self.retranslateUi()
        self.listWidget.setCurrentRow(0)
        self.stackedWidget.setCurrentIndex(0)

    def initSettingGroups(self):
        '''
        Adds setting groups as ListItems and connects them to their specific
        widgets.
        '''
        # Server settings - Index 0
        item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(QPixmap(':/icons/network.svg'), QIcon.Normal, QIcon.On)
        item.setIcon(icon)
        self.listWidget.addItem(item)

        self.widgetServerSettings = ServerSettingsWidget(self)
        self.stackedWidget.addWidget(self.widgetServerSettings)

    def saveSettings(self):
        for setting in self.modified_settings:
            widget = self.findChild(QObject, setting)
            if setting == 'lineEditApiUrl':
                self.settings.setValue('server/api_base_url', widget.text())
            if setting == 'lineEditApiToken':
                if widget.text().strip() == '':
                    keyring.delete_password(qApp.applicationName(), 'Token')
                else:
                    keyring.set_password(qApp.applicationName(),
                                         'Token',
                                         widget.text())
        self.settings.sync()
        self.modified_settings = []
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

    def accept(self):
        self.saveSettings()
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def retranslateUi(self):
        '''Translate labels into native language and assign them to widgets.'''
        _ = QCoreApplication.translate

        # Dialog title
        self.setWindowTitle(_('Client', 'Settings'))

        # Server settings
        item = self.listWidget.item(0)
        item.setText(_('Client', ' Server'))
        self.widgetServerSettings.labelApiUrl.setText(_('Client',
                                                        'API Base URL:'))
        self.widgetServerSettings.labelApiToken.setText(_('Client',
                                                          'API Token:'))
