# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from schemas import *


def base_ext(path):
    filename = os.path.split(path)[1]
    basename, ext = os.path.splitext(filename)

    return filename, basename, ext


def list_dir(path, match=None):
    files = Files(path)
    files.list_files(match=match)

    for fullpath in files.filepaths:
        filename, basename, ext = base_ext(fullpath)

        yield fullpath, filename, basename, ext


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

    file_mapping = {i: [k, l]
                    for i, j, k, l in zip(dir1.filenames, dir2.filenames, dir1.filepaths, dir2.filepaths)
                    if i == j}

    return file_mapping if file_mapping else []

    # return file_mapping if not path1_miss and not path2_miss else None


class Files:
    def __init__(self, path):
        self.path = path
        self.filenames = []
        self.filepaths = []

    @staticmethod
    def iter_dir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                fullpath = os.path.join(dirpath, filename)
                basename, ext = os.path.splitext(filename)

                yield fullpath, basename, ext

    def list_files(self, match=None):
        if match is None:
            match_wildcard = []
        elif isinstance(match, list):
            match_wildcard = match
        else:
            match_wildcard = [match]

        if match_wildcard:
            for _match in match_wildcard:
                for fullpath, basename, ext in Files.iter_dir(self.path):
                    if ext == _match:
                        self.filepaths.append(fullpath)
                        self.filenames.append(basename + ext)
        else:
            for fullpath, basename, ext in Files.iter_dir(self.path):
                self.filepaths.append(fullpath)
                self.filenames.append(basename + ext)

        return {filename: fullpath for filename, fullpath in zip(self.filenames, self.filepaths)}

    def show_filenames(self, split=False):
        for i in self.filenames:
            print(os.path.splitext(i)[0] if split else i)

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
