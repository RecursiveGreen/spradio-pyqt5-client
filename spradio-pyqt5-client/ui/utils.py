#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Various helpful functions for use in displaying the UI.
'''


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
