# -*- coding: utf-8 -*-
from paths import *


def count_lines():
    files = Files(cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']))
    files.ls(match='.py')
    c = 0
    for i in files.paths:
        count = len(open(i).readlines())
        c += count
    print(c)


def show_files(path, match=None):
    for fullpath, filename, basename, ext in list_dir(path, match=match):
        print('{:<100}{:<20}{:<20}{:<10}'.format(fullpath, filename, basename, ext))


##################################################
meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1
paths = Paths(meleti, mel_type, company_name)
kt_map = load_json(paths.kt_info_path)
kt = NamesAndLists(kt_map)

##################################################
src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
dst = cp(['Google Drive', 'Work', 'ktima', 'ktima_6'], origin=gd[user])

# src = r"C:\Users\kazna\Desktop\compare\new"
# dst = r"C:\Users\kazna\Desktop\compare\old"

# compare = Compare(src, dst, match='.py')

# src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
#
#
# files = Files(src)
# files.ls()

count_lines()
