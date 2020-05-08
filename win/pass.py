# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module is for creating temporary or permanent passes for users

from ktima.uasm import *


def p_pass():
    """
    Creates permanent pass for given user

    :return: Nothing
    """

    _user = raw_input('\nUser :\n')
    if _user == "":
        _user = USER

    _hk = hashlib.sha256(_user).hexdigest()

    data = {"{}".format(_user): "{}".format(_hk)}

    write_json(
        cp([google_drive, work, ktima_folder, passes, '{}.json'.format(_user)],
           origin=gd[USER]), data)


def t_pass():
    """
    Creates temporary pass for given user.

    :return: Nothing
    """

    _user = raw_input('\nUser :\n')
    if _user == "":
        _user = USER

    c_date = time.strftime("%d/%m/%Y")

    _hk = hashlib.sha256('{}-{}'.format(c_date, _user)).hexdigest()

    data = {"{}".format(_user): "{}".format(_hk)}

    if _user == "":
        write_json(cp([users, _user, json_ipass]), data)
    else:
        try:
            os.mkdir(
                cp([google_drive, work, ktima_folder, passes, passes_temp,
                    _user],
                   origin=gd[_user]))

        except WindowsError:
            pass

        write_json(
            cp([google_drive, work, ktima_folder, passes, passes_temp, _user,
                json_ipass], origin=gd[USER]), data)


action = raw_input('Pass :\n').upper()

if action == "P":
    p_pass()
elif action == "T":
    t_pass()
else:
    print("No pass")
