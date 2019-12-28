# -*- coding: utf-8 -*-
from paths import *
from collections import Counter
import copy
import fnmatch
import shutil
import getpass
import sys


def count_lines():
    files = Files(cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']))
    files.list_files(match='.py')
    c = 0
    for i in files.filepaths:
        count = len(open(i).readlines())
        c += count
    print(c)


##################################################
meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1
paths = Paths(meleti, mel_type, company_name)
kt_map = load_json(paths.kt_info_path)
kt = NamesAndLists(kt_map)
##################################################

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
