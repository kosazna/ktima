# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module is for authentication purposes

from subprocess import check_output
from paths import *


def get_user_uid():
    arguments = "-A ktima"
    authorizer = os.path.join(os.environ.get('USERPROFILE'), '.ktima', 'auth.exe')
    if os.path.exists(authorizer):
        authdata = check_output("{} {}".format(authorizer, arguments))
    else:
        authdata = None

    return eval(authdata)

mapping_auth = get_user_uid()


def get_pass():
    if mapping_auth is not None:
        try:
            return mapping_auth[USER]['arcgis']
        except KeyError:
            return False
    else:
        return False

def get_categories():
    return mapping_auth[USER]['categories']
