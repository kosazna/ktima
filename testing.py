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
kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])
naming_path = cp([meleti, inputdata, docs_i, 'KT_Naming_Schema.json'])
info_data = load_json(kt_info_path)
naming_data = load_json(naming_path)
lut = NamesAndLists(info_data, naming_data)

##################################################

src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
dst = cp(['Google Drive', 'Work', 'ktima', 'ktima_6'], origin=gd[user])

count_lines()
