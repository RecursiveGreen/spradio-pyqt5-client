#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Various helpful functions for use in displaying the UI.
'''

import json

import keyring

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import qApp

import requests


def full_name(artist):
    '''
    String representing the artist's full name including an alias, if
    available.
    '''
    if artist['alias']:
        if artist['first_name'] or artist['last_name']:
            return '{} "{}" {}'.format(artist['first_name'],
                                       artist['alias'],
                                       artist['last_name'])
        return artist['alias']
    return '{} {}'.format(artist['first_name'], artist['last_name'])


def _prepare_server_request(endpoint, page=0):
    '''
    Return a tuple of information to setup a RESTful request to the server.
    '''
    settings = QSettings()
    base_url = settings.value('server/api_base_url', type=str)
    url = base_url + endpoint + '/'
    if page > 0:
        url = url + '?page=' + str(page)
    password = 'Token ' + keyring.get_password(qApp.applicationName(),
                                               'Token')
    headers = {'content-type': 'application/json', 'authorization': password}
    return url, headers


def delete_server_data(endpoint):
    '''
    Given the name of the endpoint, delete an item on the server.
    '''
    url, headers = _prepare_server_request(endpoint)
    req = requests.delete(url, headers=headers)
    return req.status_code, ''


def get_server_data(endpoint, page):
    '''
    Given the name of the endpoint, and an optional page number, retrieve the
    data from the server RESTful API and return as a dict.
    '''
    url, headers = _prepare_server_request(endpoint, page)
    req = requests.get(url, headers=headers)
    return req.status_code, req.json()


def post_server_data(endpoint, data):
    '''
    Given the name of the endpoint, create a new item on the server.
    '''
    url, headers = _prepare_server_request(endpoint)
    req = requests.post(url, headers=headers, data=json.dumps(data))
    return req.status_code, req.json()


def put_server_data(endpoint, data):
    '''
    Given the name of the endpoint, update an existing item on the server.
    '''
    url, headers = _prepare_server_request(endpoint)
    req = requests.put(url, headers=headers, data=json.dumps(data))
    return req.status_code, req.json()
