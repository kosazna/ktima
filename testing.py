# -*- coding: utf-8 -*-
from paths import *
import re
from datetime import datetime, timedelta
from subprocess import check_output
import os

# print(check_output("C:/Users/aznavouridis.k/.ktima/auth.exe --appname ktima"))
print(os.environ.get("USERPROFILE"))


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

# meleti = 'KT5-14'
# company_name = 'NAMA'
# mel_type = 2

# # paths = Paths(meleti, mel_type, company_name)
# info_data = load_json(cp([meleti, inputdata, docs_i,
#                           'KT_Info.json']))
# naming_data = load_json(cp([meleti, inputdata, docs_i,
#                             'KT_Naming_Schema.json']))
# info = KTInfo(info_data)
# paths = KTPaths(meleti, mel_type, company_name)
# names = KTNamingSchema(info)

##################################################

src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
dst = cp(['Google Drive', 'Work', 'ktima', 'ktima_8'], origin=gd[USER])

all_ktima = [
    "ASTENOT",
    "ASTIK",
    "ASTOTA",
    "ASTTOM",
    "BLD",
    "BLOCK_PNT",
    "CBOUND",
    "DBOUND",
    "OIK",
    "POI",
    "POL",
    "FBOUND",
    "PRE_FBOUND",
    "PRE_COASTLINE",
    "PST",
    "ROADS",
    "EAS",
    "VST",
    "EIA_PNT",
    "EIA",
    "MRT",
    "NOMI",
    "VSTEAS_REL",
    "RBOUND"]
