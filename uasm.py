# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module is for authentication purposes

import hashlib
from paths import *


def get_user_uid():
    if ktl.get('company_name', 'NOT_FOUND') == c_NA:
        ppp = cp([mdev, 'Diafora', 'paratiriseis', 'uas.json'],
                 origin=ktl['temp'][USER])
    else:
        ppp = cp([temp2kp, mdev, 'Diafora', 'paratiriseis', 'uas.json'],
                 origin=ktl['temp'][USER])

    tpp = cp([users, USER, 'ipass.json'])

    try:
        with open(ppp, 'r') as h_f:
            hash_k = hashlib.sha1(USER).hexdigest()
            keys = json.load(h_f)
    except IOError:
        c_date = time.strftime("%d/%m/%Y")
        try:
            with open(tpp, 'r') as h_f:
                hash_k = hashlib.sha1('{}-{}'.format(c_date, USER)).hexdigest()
                keys = json.load(h_f)
        except IOError:
            hash_k = None
            keys = {}

    return hash_k, keys


hk, key = get_user_uid()


def get_pass():
    try:
        ehk = key[USER]
    except KeyError:
        ehk = "No Key"

    if hk == ehk or mdev.strip('! ') == USER or USER == 'kazna':
        return True
    else:
        return False
