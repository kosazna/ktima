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
from cust_arc import *

local_ktima_version = '8.0'
warning_counter = 0


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
            new_version = keys['ktima_version']
    except IOError:
        c_date = time.strftime("%d/%m/%Y")
        try:
            with open(tpp, 'r') as h_f:
                hash_k = hashlib.sha256(
                    '{}-{}'.format(c_date, USER)).hexdigest()
                keys = json.load(h_f)
                new_version = local_ktima_version
        except IOError:
            hash_k = None
            keys = {}
            new_version = local_ktima_version

    return hash_k, keys, new_version


hk, key, recent_ktima_version = get_user_uid()


def get_pass():
    global warning_counter

    try:
        ehk = key[USER]
    except KeyError:
        ehk = "No Key"

    if mdev.strip('! ') == USER:
        return True
    elif hk == ehk:
        if local_ktima_version != recent_ktima_version:
            if 4 < warning_counter < 8:
                pm('\n! There is an updated "ktima" version !')
                pm('Your realease : {}'.format(local_ktima_version))
                pm('Newer release: {}\n'.format(recent_ktima_version))
            warning_counter += 1
        return True
    else:
        return False
