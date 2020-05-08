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
        ppp = cp([mdev, diafora, paratiriseis, json_uas],
                 origin=ktl['temp'][USER])
    else:
        ppp = cp([temp2p, mdev, diafora, paratiriseis, json_uas],
                 origin=ktl['temp'][USER])

    tpp = cp([users, USER, json_ipass])

    try:
        with open(ppp, 'r') as h_f:
            hash_k = hashlib.sha256(USER).hexdigest()
            keys = json.load(h_f)
    except IOError:
        c_date = time.strftime("%d/%m/%Y")
        try:
            with open(tpp, 'r') as h_f:
                hash_k = hashlib.sha256(
                    '{}-{}'.format(c_date, USER)).hexdigest()
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

    if hk == ehk or mdev.strip('! ') == USER:
        return True
    else:
        return False
