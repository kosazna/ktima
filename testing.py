# -*- coding: utf-8-sig -*-
from paths import *
import fnmatch

meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
ktdata = load_json(paths.kt_info_path)
kt = NamesAndLists(ktdata)

# for ota in kt.ota_list:
#     os.mkdir(os.path.join(paths.mdb_out, ota))

#####################################

# for _ in kt.status_list:
#     print(_)

# print(kt.__class__)

# for _ in dir(kt):
#     if '_list' not in _ and '__' not in _:
#         print('{} =
#         {}'.format(str(_), str(getattr(kt, _))))

# for k, v in vars(kt).iteritems():
#     print(k, v)

clearlocalpath = paths.localdata


def counter():
    astenot = []
    astik = []
    astota = []
    asttom = []
    bld = []
    cbound = []
    dbound = []
    oik = []
    poi = []
    pre_coastline = []
    pre_fbound = []
    pst = []
    rbound = []
    roads = []
    fbound = []
    eas = []
    vst = []

    kt_map = {"ASTENOT": astenot,
              "ASTIK": astik,
              "ASTOTA": astota,
              "ASTTOM": asttom,
              "BLD": bld,
              "CBOUND": cbound,
              "DBOUND": dbound,
              "OIK": oik,
              "POI": poi,
              "FBOUND": fbound,
              "PRE_COASTLINE": pre_coastline,
              "PRE_FBOUND": pre_fbound,
              "PST": pst,
              "ROADS": roads,
              "EAS": eas,
              "VST": vst,
              "RBOUND": rbound}

    for rootDir, subdirs, filenames in os.walk(clearlocalpath):
        for filename in fnmatch.filter(filenames, '*shp'):
            kt_map[os.path.splitext(filename)[0]].append(os.path.join(rootDir, filename))

    for i in kt_map:
        if len(kt_map[i]):
            print('{} --> {}'.format(i, len(kt_map[i])))


counter()
