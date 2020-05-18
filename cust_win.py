# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module has custom functions for the entire ktima project

import json
import time
import sys
import shutil
import copy


def time_it(func):
    """
    Decorator
    Calculates execution time of a function.
    Prints execution time.

    :param func: Function to be measured
    :return: Nothing
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('{} --> {:.0f} min {:.4f} sec'.format(func.__name__,
                                                    (end - start) // 60,
                                                    (end - start) % 60))

        return result

    return wrapper


def timestamp():
    """
    Gives current date and time in "xx/xx/xxxx - xx:xx:xx" format.

    :return: str
        Current date and time.
    """

    c_date = time.strftime("%d/%m/%Y")
    c_time = time.strftime("%H:%M:%S")
    datetime = c_date + " - " + c_time

    return datetime


# def cp(p_list=(), origin='C'):
#     """
#     Creates path from a list given the drive letter.
#
#     :param p_list: list or tuple or set
#         Items of path.
#     :param origin: str, optional
#         Drive letter (default: 'C').
#     :return: str
#         Full path for a given p_list else 'C:\\' if p_list is not provided.
#     """
#
#     _path = '{}:\\'.format(origin)
#     path = ""
#     for i in range(0, len(p_list)):
#         path = os.path.join(_path, p_list[i])
#         _path = path
#     return path if path else _path

def cp(members, origin='C'):
    """
    Creates path from a list given the drive letter.

    :param members: list or tuple or set
        Items of path.
    :param origin: str, optional
        Drive letter (default: 'C').
    :return: str
        Full path for a given p_list else 'C:\\' if p_list is not provided.
    """

    drive = '{}:'.format(origin)

    if members is None:
        return "{}\\".format(drive)
    else:
        temp_members = copy.copy(members)
        temp_members.insert(0, drive)
        return '\\'.join(temp_members)


def load_json(path):
    """
    Loads json file to a dictionary.

    :param path: str
        Path of json file.
    :return: dict
        Python dictionary of the json file.
    """

    try:
        with open(path, "r") as status_f:
            data = json.load(status_f)
        return data
    except IOError:
        print('\n!! NO SUCH FILE : {}\n'.format(path))


def write_json(path, data):
    """
    Writes python dictionary to a json file (indent=2).

    :param path: str
        Path to write the json file.
    :param data: dict
        Python dictionary.
    :return: Nothing
    """

    with open(path, "w") as p_file:
        json.dump(data, p_file, indent=2)


def c_copy(src, dst):
    """
    Copies file for one destination to another.

    :param src: str
        Source file path.
    :param dst: str
        Destination file path.
    :return: Nothing
    """

    try:
        shutil.copyfile(src, dst)
        print('!! OK !!')
    except IOError as e:
        print(e)


def progress(count, total):
    """
    Prints prograss bar to cmd.

    :param count: int
        Current count for progress bar.
    :param total: int
        Total count of progress bar.
    :return:
    """

    suffix = '{}/{}'.format(count, total)
    bar_len = 80
    filled_len = int(round(bar_len * count / float(total)))

    percents = int(round(100.0 * count / total, 0))
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s %s -- %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def add_mel_inpath(original_members, mel):
    """
    Given a meleti numbers it is added to the list members of a path

    :param original_members: list
        Items of path.
    :param mel: string
        Meleti.
    :return: list
        List of strins containing path members.
    """
    final_members = copy.copy(original_members)
    final_members.append(mel)

    return final_members


def strize(iterable):
    """
    Converts any type of string (unicode etc.) to utf-8 string.

    :param iterable: list
        list of strings.
    :return: list
        List of strings utf-8 encoded.
    """

    return [str(i) for i in iterable]
