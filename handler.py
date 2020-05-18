# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# File handling module for creating list of files on a directory
# or comparing files between two directories

import os
from schemas import *


def base_ext(path):
    """
    Splits from a filename the extension. Works even if a file has
    multiple extensions.

    :param path: str
        Path of the filename.
    :return: str, str, str
        Filename, basename, extension.
    """

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
    """
    Yields for the given directory and for every file its
    fullpath, filename, basename and extension.

    :param path: str
        Path of the filename.
    :param match: str, list
        Filter for extension in '.py' format.
        It can be a string with 1 extension or a list with multiple extensions.
        (default: None) -> yields all files.
    :return: str, str, str, str,
        Fullpath, filename, basename, extension
    """

    files = Files(path)
    files.explore(match=match)

    for fullpath in files.paths:
        filename, basename, ext = base_ext(fullpath)

        yield fullpath, filename, basename, ext


def file_path_dict(path, match=None):
    """
    Creates a dictionary with file basename as key and
    file fullpath as it's value.

    :param path: str
        Path of the filename.
    :param match: str, list
        Filter for extension in '.py' format.
        It can be a string with 1 extension or a list with multiple extensions.
        (default: None) -> yields all files.
    :return: dict
        basename: fullpath
    """
    files = Files(path)
    files.explore(match=match)

    fp_dict = {}

    for fullpath in files.paths:
        filename, basename, ext = base_ext(fullpath)

        fp_dict[basename] = fullpath

    return fp_dict


class Compare:
    """
    Given two paths will make a list of the files.
    For the files which are not common in both paths can copy them in
    a new directory

    Attributes
    ----------
    - path_1: First path
    - path_2: Second path
    - map_1: Dictionary mapping every file of path_1 ({basename: fullpath})
    - map_2: Dictionary mapping every file of path_2 ({basename: fullpath})
    - dir_1_count: number of files in path_1
    - dir_2_count: number of files in path_2
    - path_1_miss: Files from path_2 that are missing from path_1
    - path_2_miss: Files from path_1 that are missing from path_2
    - all: Dict of all files (basename: [path_1_fullpath, path_2_fullpath]})
    - common: Dictionary of common files
    - diff: Dictionary of files that are not in both paths

    Methods
    -------
    - show_missing
    - extract_diff
    - show

    """

    def __init__(self, path_1, path_2, match=None):
        """
        :param path_1: str
            First path.
        :param path_2: str
            Second path.
        :param match: str, list
            Filter for extension in '.py' format.
            It can be a string with 1 extension or
            a list with multiple extensions.
            (default: None) -> yields all files.
        """
        self.path_1 = path_1
        self.path_2 = path_2
        self.dir_1 = Files(self.path_1)
        self.dir_2 = Files(self.path_2)
        self.dir_1.explore(match=match)
        self.dir_2.explore(match=match)
        self.map_1 = self.dir_1.mapper_nd
        self.map_2 = self.dir_2.mapper_nd
        self.dir_1_count = self.dir_1.file_counter
        self.dir_2_count = self.dir_2.file_counter
        self.path_1_miss = tuple(set(self.dir_2.names) - set(self.dir_1.names))
        self.path_2_miss = tuple(set(self.dir_1.names) - set(self.dir_2.names))
        self.all, self.common, self.diff = Compare.all_files_mapping(self.map_1,
                                                                     self.map_2)

    def show_missing(self):
        """
        Prints missing files that are not common in both paths.

        :return: Nothing
        """

        print('{} - missing:'.format(self.path_1))
        print('---------------------------')
        for i in sorted(self.path_1_miss):
            print(i)

        print('')
        print('*')
        print('')

        print('{} - missing:'.format(self.path_2))
        print('---------------------------')
        for i in sorted(self.path_2_miss):
            print(i)

    @staticmethod
    def all_files_mapping(mapping_1, mapping_2):
        """
        Creates dictionaries with mapping af all, common and not common files.

        :param mapping_1: dict
            File mapping of path_1
        :param mapping_2: dict
            File mapping of path_2
        :return: dict, dict, dict
            Returns dictionaries with the mapping of the files
        """

        map_all = {}
        map_common = {}
        map_diff = {}

        for i in mapping_1:
            map_all[i] = [mapping_1[i], mapping_2.get(i, None)]

        for i in mapping_2:
            if i not in map_all:
                map_all[i] = [mapping_1.get(i, None), mapping_2[i]]

        for i in map_all:
            if map_all[i][0] and map_all[i][1]:
                map_common[i] = [map_all[i][0], map_all[i][1]]
            else:
                map_diff[i] = [map_all[i][0], map_all[i][1]]

        return map_all, map_common, map_diff

    def extract_diff(self):
        """
        Files that are not common between the provided paths will be copied
        in the parent directory of the first path under the name
        "root_dir_of_path_1\\Difference".

        :return: Nothing
        """

        if self.diff:
            target = self.path_1.split('\\')[1:-1] + ['Difference']
            path_1_miss = target + [
                'Missing_from_path_1_({})'.format(self.path_1.split('\\')[-1])]
            path_2_miss = target + [
                'Missing_from_path_2_({})'.format(self.path_2.split('\\')[-1])]
            p1p = cp(path_1_miss)
            p2p = cp(path_2_miss)

            if not os.path.exists(p1p):
                os.makedirs(p1p)

            if not os.path.exists(p2p):
                os.makedirs(p2p)

            for i in self.diff:
                if self.diff[i][0]:
                    _dst = os.path.join(p2p,
                                        os.path.split(self.diff[i][0])[1])
                    c_copy(self.diff[i][0], _dst)
                elif self.diff[i][1]:
                    _dst = os.path.join(p1p,
                                        os.path.split(self.diff[i][1])[1])
                    c_copy(self.diff[i][1], _dst)

            print('\n{} - was created for files missing'.format(p1p))
            print('\n{} - was created for files missing '.format(p2p))
        else:
            print('Directories are identical. No extraction was performed')

    def show(self, what='all'):
        """
        Prints formatted columns of the filename and the fullpath of each
        provided directory.

        :param what: str
            - 'all': Prints all files.
            - 'common': prints common files.
            - 'diff': prints files that are not common in both paths

            (default: 'all')
        :return:Nothing
        """

        if what == 'all':
            for i in self.all:
                print('{:<20}  {:<75}  {:<75}'.format(i,
                                                      self.all[i][0],
                                                      self.all[i][1]))
                print('-------------------------------------------------------')
        elif what == 'common':
            for i in self.common:
                print('{:<20}  {:<75}  {:<75}'.format(i,
                                                      self.common[i][0],
                                                      self.common[i][1]))
                print('-------------------------------------------------------')
        elif what == 'diff':
            for i in self.diff:
                print('{:<20}  {:<75}  {:<75}'.format(i,
                                                      self.diff[i][0],
                                                      self.diff[i][1]))
                print('-------------------------------------------------------')


class Files:
    """
    Given a path will make a list of the files.

    Attributes
    ----------
    - path: Path
    - ns: list of all filenams
    - paths: list of all filepaths
    - mapper: Dictionary mapping every file ({directory: [filenames]})
    - mapper_nd: Dictionary mapping every file ({basename: fullpath})
    - c_mapper: Dictionary counting every file ({directory: number of files})
    - file_counter: counter for all files in the given path

    Methods
    -------
    - explorer
    - show_names
    - show_paths
    - show_tree
    - extract
    - gather

    """

    def __init__(self, path):
        """
        :param path: str
            Path.
        """
        self.path = path
        self.names = []
        self.paths = []
        self.mapper = dict()
        self.mapper_nd = dict()
        self.c_mapper = dict()
        self.file_counter = 0

    @classmethod
    def from_list(cls, path_items):
        """
        Creates Files object from a list of elements of the path.

        :param path_items: list
            Elements of the path.
        :return: Files object
        """

        new_path = cp(path_items)
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

    def explore(self, match=None):
        """
        Explores the self.path and catalogs every file.

        :param match: str, list
            Filter for extension in '.py' format.
            It can be a string with 1 extension or
            a list with multiple extensions.
            (default: None) -> yields all files.
        :return: Nothing
        """

        match_wildcard = Files.matcher(match)

        if match_wildcard:
            for _match in match_wildcard:
                for fullpath, filename, basename, ext in Files.iter_dir(
                        self.path):
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
        """
        Prints the filenames for the given directory.

        :param split: boolean, optional
            If True only the basename will be printed.
            If False only the filename will be printed (basename.extension).
            (default: False)
        :return: Nothing
        """

        print('-----  {} Files  -----'.format(self.file_counter))
        for i, j in enumerate(sorted(self.names)):
            print('{:>5})  {}'.format(i + 1,
                                      os.path.splitext(j)[0] if split else j))
        print('-----  {} Files  -----'.format(self.file_counter))

    def show_paths(self):
        """
        Prints the fullpath of the files.

        :return: Nothing
        """

        print('-----  {} Files  -----'.format(self.file_counter))
        for i, j in enumerate(sorted(self.paths)):
            print('{:>5})  {}'.format(i + 1, j))
        print('-----  {} Files  -----'.format(self.file_counter))

    def show_tree(self):
        """
        Prints the entire directory tree.

        :return: Nothing
        """

        for i in sorted(self.mapper):
            print('{}  --  {} files'.format(i, self.c_mapper[i]))
            for j in self.mapper[i]:
                print("|----- {}".format(j))
            print('\n')

    def extract(self, what='filepaths', split=False):
        """
        Creates a txt file with either all the filepaths or the filenames.

        :param what: str, optional
            - 'filepaths' (default)
            - 'filenames'
        :param split: boolean, optional
            If True only the basename will be printed.
            If False only the filename will be printed (basename.extension).
            (default: False)
        :return: Nothing
        """

        with open(os.path.join(self.path, 'File_List.txt'), 'w') as f:
            if what == 'filepaths':
                for i in self.paths:
                    f.write('{}\n'.format(i))
            else:
                for i in self.names:
                    f.write(
                        '{}\n'.format(os.path.splitext(i)[0] if split else i))

    def gather(self, dst):
        """
        Copies all the files from the given directory to a new destination
        without their parent folders.

        :param dst: str
            Destination path.
        :return:
        """
        if not os.path.exists(dst):
            os.makedirs(dst)

        for path in self.mapper.keys():
            for mapper_file in self.mapper[path]:
                inpath = os.path.join(path, mapper_file)
                outpath = os.path.join(dst, mapper_file)
                c_copy(inpath, outpath)

    def __getitem__(self, item):
        return self.mapper_nd[item]

    def __setitem__(self, key, value):
        self.mapper_nd[key] = value
