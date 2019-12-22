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
import shutil


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('{} --> {:.0f} min {:.4f} sec'.format(func.__name__, (end - start) // 60, (end - start) % 60))

        return result

    return wrapper


def iter_dir(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            basename, ext = os.path.splitext(filename)

            yield fullpath, basename, ext


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


def dir_compare(path1, path2, match=None):
    dir1 = Files(path1)
    dir2 = Files(path2)

    dir1.list_files(match=match)
    dir2.list_files(match=match)

    path2_miss = tuple(set(dir1.filenames) - set(dir2.filenames))
    path1_miss = tuple(set(dir2.filenames) - set(dir1.filenames))

    print('{} - missing:'.format(path2))
    print('---------------------------')
    for i in sorted(path2_miss):
        print(i)

    print('')
    print('===========================')
    print('')

    print('{} - missing:'.format(path1))
    print('---------------------------')
    for i in sorted(path1_miss):
        print(i)


class Files:
    def __init__(self, path):
        self.path = path
        self.filenames = []
        self.filepaths = []

    def list_files(self, match=None, filenames_only=False):
        if match is None:
            match_wildcard = []
        elif isinstance(match, list):
            match_wildcard = match
        else:
            match_wildcard = [match]

        if match_wildcard:
            for _match in match_wildcard:
                for fullpath, basename, ext in iter_dir(self.path):
                    if ext == _match:
                        self.filepaths.append(fullpath)
                        self.filenames.append(basename + ext)
        else:
            for fullpath, basename, ext in iter_dir(self.path):
                self.filepaths.append(fullpath)
                self.filenames.append(basename + ext)

        return self.filenames if filenames_only else self.filepaths

    def show_filenames(self):
        for i in self.filenames:
            print(i)

    def show_filepaths(self):
        for i in self.filepaths:
            print(i)

    def extract(self, what='filepaths'):
        with open(os.path.join(self.path, 'File_List.txt'), 'w') as f:
            if what == 'filepaths':
                for i in self.filepaths:
                    f.write('{}\n'.format(i))
            else:
                for i in self.filenames:
                    f.write('{}\n'.format(i))
