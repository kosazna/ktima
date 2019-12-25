# -*- coding: utf-8 -*-
from handler import *
from collections import Counter
import copy
import fnmatch
import shutil
import getpass
import sys

##################################################
meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
kt_map = load_json(paths.kt_info_path)
kt = NamesAndLists(kt_map)

##################################################


# ls = dir_compare(cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']), cp(['Google Drive', 'Work', 'ktima', 'ktima 5'], origin='D'), match='.py')

# for i in ls:
#     print(i, ls[i])

# code = Files(cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']))
# mapping = code.list_files(match='.py')
#
# code.extract('filepaths')


# def all_files():
#     src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
#     dst = cp(['Google Drive', 'Work', 'ktima', 'ktima 5'], origin=gd[user])
#
#     mapping = dir_compare(src, dst, match='.py')
#
#     if mapping:
#         for i in mapping:
#             print(mapping[i][0], mapping[i][1])
#     else:
#         print("\nWARNING! - Directories don't match\n")
#
#
# all_files()

files = Files(cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']))
files.list_files(match='.py')

for i in files.filepaths:
    basename, ext = base_ext(i)
    print(basename, ext)
