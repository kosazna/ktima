# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import os
import json
import time
import sys
from shutil import copyfile, copytree


# sys.tracebacklimit = 0


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('{} --> {:.0f} min {:.4f} sec'.format(func.__name__, (end - start) // 60, (end - start) % 60))

        return result

    return wrapper


def timestamp():
    c_date = time.strftime("%d/%m/%Y")
    c_time = time.strftime("%H:%M:%S")
    datetime = c_date + " - " + c_time

    return datetime


def cp(p_list=(), origin='C'):
    _path = '{}:\\'.format(origin)
    path = ""
    for i in range(0, len(p_list)):
        path = os.path.join(_path, p_list[i])
        _path = path
    return path if path else _path


def load_json(path):
    try:
        with open(path, "r") as status_f:
            data = json.load(status_f)
        return data
    except IOError:
        print('\n!! NO SUCH FILE : {}\n'.format(path))

    return


def write_json(path, data):
    with open(path, "w") as p_file:
        json.dump(data, p_file, indent=2)


def c_copy(s, d):
    try:
        copyfile(s, d)
        print('!! OK !!')
    except IOError:
        print('!! File Not Found !!')
