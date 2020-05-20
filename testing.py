# -*- coding: utf-8 -*-
from paths import *


def count_lines(path):
    files = Files(path)
    files.explore(match='.py')

    c = 0

    for i in files.paths:
        count = len(open(i).readlines())
        c += count
    print(c)


def show_files(path, match=None):
    for fullpath, filename, basename, ext in list_dir(path, match=match):
        print('{:<100}{:<20}{:<20}{:<10}'.format(fullpath,
                                                 filename,
                                                 basename,
                                                 ext))


##################################################

# meleti = 'KT2-11'
# company_name = 'NAMA'
# mel_type = 1
# 
# paths = Paths(meleti, mel_type, company_name)
# info_data = load_json(cp([meleti, inputdata, docs_i,
#                           'KT_Info.json']))
# naming_data = load_json(cp([meleti, inputdata, docs_i,
#                             'KT_Naming_Schema.json']))
# lui = NamesAndLists(info_data, naming_data)

##################################################

src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
dst = cp(['Google Drive', 'Work', 'ktima', 'ktima_7'], origin=gd[USER])

count_lines(src)
