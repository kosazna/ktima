# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from schemas import *


def base_ext(path):
    filename = os.path.split(path)[1]
    filename_parts = filename.split('.')
    quantity = len(filename_parts)

    if quantity == 2:
        basename, ext = os.path.splitext(filename)
    elif quantity == 3:
        basename = filename_parts[0]
        ext = '.{0[1]}.{0[2]}'.format(filename_parts)
    else:
        basename = filename
        ext = None

    return filename, basename, ext


def list_dir(path, match=None):
    files = Files(path)
    files.ls(match=match)

    for fullpath in files.paths:
        filename, basename, ext = base_ext(fullpath)

        yield fullpath, filename, basename, ext


class Compare:
    def __init__(self, path_1, path_2, match=None):
        self.path_1 = path_1
        self.path_2 = path_2
        self.dir_1 = Files(self.path_1)
        self.dir_2 = Files(self.path_2)
        self.dir_1.ls(match=match)
        self.dir_2.ls(match=match)
        self.map_1 = self.dir_1.mapper_nd
        self.map_2 = self.dir_2.mapper_nd
        self.dir_1_count = self.dir_1.file_counter
        self.dir_2_count = self.dir_2.file_counter
        self.path_1_miss = tuple(set(self.dir_2.names) - set(self.dir_1.names))
        self.path_2_miss = tuple(set(self.dir_1.names) - set(self.dir_2.names))
        self.mapper_all, self.mapper_common, self.mapper_diff = Compare.all_files_mapping(self.map_1, self.map_2)

    def show_missing(self):
        print('{} - missing:'.format(self.path_1))
        print('---------------------------')
        for i in sorted(self.path_1_miss):
            print(i)

        print('')
        print('***************************')
        print('')

        print('{} - missing:'.format(self.path_2))
        print('---------------------------')
        for i in sorted(self.path_2_miss):
            print(i)

    @staticmethod
    def all_files_mapping(_1, _2):
        map_all = {}
        map_common = {}
        map_diff = {}

        for i in _1:
            map_all[i] = [_1[i], _2.get(i, None)]

        for i in _2:
            if i not in map_all:
                map_all[i] = [_1.get(i, None), _2[i]]

        for i in map_all:
            if map_all[i][0] and map_all[i][1]:
                map_common[i] = [map_all[i][0], map_all[i][1]]
            else:
                map_diff[i] = [map_all[i][0], map_all[i][1]]

        return map_all, map_common, map_diff

    def extract_diff(self):
        if self.mapper_diff:
            target = self.path_1.split('\\')[1:-1] + ['Difference']
            path_1_miss = target + ['Missing_from_path_1_({})'.format(self.path_1.split('\\')[-1])]
            path_2_miss = target + ['Missing_from_path_2_({})'.format(self.path_2.split('\\')[-1])]
            p1p = cp(path_1_miss)
            p2p = cp(path_2_miss)

            if not os.path.exists(p1p):
                os.makedirs(p1p)

            if not os.path.exists(p2p):
                os.makedirs(p2p)

            for i in self.mapper_diff:
                if self.mapper_diff[i][0]:
                    _dst = os.path.join(p2p, os.path.split(self.mapper_diff[i][0])[1])
                    c_copy(self.mapper_diff[i][0], _dst)
                elif self.mapper_diff[i][1]:
                    _dst = os.path.join(p1p, os.path.split(self.mapper_diff[i][1])[1])
                    c_copy(self.mapper_diff[i][1], _dst)

            print('\n{} - was created for files missing'.format(p1p))
            print('\n{} - was created for files missing '.format(p2p))
        else:
            print('Directories are identical. No extraction was performed')

    def show(self, what='all'):
        if what == 'all':
            for i in self.mapper_all:
                print(' {:<20}  {:<75}  {:<75}'.format(i, self.mapper_all[i][0], self.mapper_all[i][1]))
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        elif what == 'common':
            for i in self.mapper_common:
                print(' {:<20}  {:<75}  {:<75}'.format(i, self.mapper_common[i][0], self.mapper_common[i][1]))
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        elif what == 'diff':
            for i in self.mapper_diff:
                print(' {:<20}  {:<75}  {:<75}'.format(i, self.mapper_diff[i][0], self.mapper_diff[i][1]))
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


class Files:
    def __init__(self, path):
        self.path = path
        self.names = []
        self.paths = []
        self.mapper = dict()
        self.mapper_nd = dict()
        self.c_mapper = dict()
        self.file_counter = 0

    @classmethod
    def from_list(cls, _list):
        new_path = cp(_list)
        return cls(new_path)

    @staticmethod
    def iter_dir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                fullpath = os.path.join(dirpath, filename)
                filename, basename, ext = base_ext(fullpath)

                yield fullpath, filename, basename, ext

    @staticmethod
    def matcher(match):
        if match is None:
            match_wildcard = []
        elif isinstance(match, list):
            match_wildcard = match
        else:
            match_wildcard = [match]

        return match_wildcard

    def ls(self, match=None):
        match_wildcard = Files.matcher(match)

        if match_wildcard:
            for _match in match_wildcard:
                for fullpath, filename, basename, ext in Files.iter_dir(self.path):
                    if ext == _match:
                        key = os.path.split(fullpath)[0]

                        if key not in self.mapper:
                            self.mapper[key] = []
                            self.c_mapper[key] = 0

                        self.paths.append(fullpath)
                        self.names.append(basename)
                        self.file_counter += 1
                        self.mapper[key].append(filename)
                        self.c_mapper[key] += 1
        else:
            for fullpath, filename, basename, ext in Files.iter_dir(self.path):
                key = os.path.split(fullpath)[0]

                if key not in self.mapper:
                    self.mapper[key] = []
                    self.c_mapper[key] = 0

                self.paths.append(fullpath)
                self.names.append(basename)
                self.file_counter += 1
                self.mapper[key].append(filename)
                self.c_mapper[key] += 1

        self.mapper_nd = dict(zip(self.names, self.paths))

    def show_names(self, split=False):
        print('-----  {} Files  -----'.format(self.file_counter))
        for i, j in enumerate(sorted(self.names)):
            print('{:>5})  {}'.format(i + 1, os.path.splitext(j)[0] if split else j))
        print('-----  {} Files  -----'.format(self.file_counter))

    def show_paths(self):
        print('-----  {} Files  -----'.format(self.file_counter))
        for i, j in enumerate(sorted(self.paths)):
            print('{:>5})  {}'.format(i + 1, j))
        print('-----  {} Files  -----'.format(self.file_counter))

    def show_tree(self):
        for i in sorted(self.mapper):
            print('{}  --  {} files'.format(i, self.c_mapper[i]))
            for j in self.mapper[i]:
                print("|----- {}".format(j))
            print('\n')

    def extract(self, what='filepaths', split=False):
        with open(os.path.join(self.path, 'File_List.txt'), 'w') as f:
            if what == 'filepaths':
                for i in self.paths:
                    f.write('{}\n'.format(i))
            else:
                for i in self.names:
                    f.write('{}\n'.format(os.path.splitext(i)[0] if split else i))

    def gather(self, new_path):
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        for fullpath, filename in zip(self.paths, self.names):
            c_copy(fullpath, os.path.join(new_path, filename))

    # def __getattr__(self, item):
    #     return self.mapper_nd[item]

    def __getitem__(self, item):
        return self.mapper_nd[item]

    def __setitem__(self, key, value):
        self.mapper_nd[key] = value
