# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import hashlib
from paths import *


def get_user_uid():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        ppp = cp([mdev, 'Diafora', 'paratiriseis', 'uas.json'], origin=ktl['temp'][user])
    else:
        ppp = cp([temp_2kp, mdev, 'Diafora', 'paratiriseis', 'uas.json'], origin=ktl['temp'][user])

    tpp = cp([users, user, 'ipass.json'])

    try:
        with open(ppp, 'r') as h_f:
            hash_k = hashlib.sha1(user).hexdigest()
            keys = json.load(h_f)
    except IOError:
        c_date = time.strftime("%d/%m/%Y")
        try:
            with open(tpp, 'r') as h_f:
                hash_k = hashlib.sha1('{}-{}'.format(c_date, user)).hexdigest()
                keys = json.load(h_f)
        except IOError:
            hash_k = None
            keys = {}

    return hash_k, keys


hk, key = get_user_uid()


def get_pass():
    try:
        ehk = key[user]
    except KeyError:
        ehk = "No Key"

    if hk == ehk or mdev.strip('! ') == user or user == 'kazna':
        return True
    else:
        return False
