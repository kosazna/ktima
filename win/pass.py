# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.uasm import *


def p_pass():
    _user = raw_input('\nUser :\n')
    if _user == "":
        _user = user

    _hk = hashlib.sha1(_user).hexdigest()

    data = {"{}".format(_user): "{}".format(_hk)}

    write_json(r"{}:\Google Drive\Work\ktima\passes\{}.json".format(gd[user],
                                                                    _user),
               data)


def t_pass():
    _user = raw_input('\nUser :\n')
    if _user == "":
        _user = user

    c_date = time.strftime("%d/%m/%Y")

    _hk = hashlib.sha1('{}-{}'.format(c_date, _user)).hexdigest()

    data = {"{}".format(_user): "{}".format(_hk)}

    if _user == "":
        write_json(r"C:\Users\{}\ipass.json".format(_user), data)
    else:
        try:
            os.mkdir(
                r"{}:\Google Drive\Work\ktima\passes\temp\{}".format(gd[_user],
                                                                     _user))
        except WindowsError:
            pass

        write_json(
            r"{}:\Google Drive\Work\ktima\passes\temp\{}\ipass.json".format(
                gd[_user], _user), data)


action = raw_input('Pass :\n').upper()

if action == "P":
    p_pass()
elif action == "T":
    t_pass()
else:
    print("No pass")
