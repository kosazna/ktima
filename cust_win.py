# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import os
import json
import time
import sys
import shutil


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
        shutil.copyfile(s, d)
        print('!! OK !!')
    except IOError:
        print('!! File Not Found or Target Directory missing!!')


def progress(count, total):
    suffix = '{}/{}'.format(count, total)
    bar_len = 80
    filled_len = int(round(bar_len * count / float(total)))

    percents = int(round(100.0 * count / total, 0))
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s %s -- %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()
