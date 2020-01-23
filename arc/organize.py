# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from data import *


mxdASTENOT = set()
mxdASTIK = set()
mxdASTOTA = set()
mxdASTTOM = set()
mxdBLD = set()
mxdCBOUND = set()
mxdDBOUND = set()
mxdEAS = set()
mxdPST = set()
mxdVST = set()
mxdRBOUND = set()
mxdROADS = set()
mxdFBOUND = set()
mxdPRE_FBOUND = set()

locASTENOT = set()
locASTIK = set()
locASTOTA = set()
locASTTOM = set()
locBLD = set()
locCBOUND = set()
locDBOUND = set()
locEAS = set()
locPST = set()
locVST = set()
locRBOUND = set()
locROADS = set()
locFBOUND = set()
locPRE_FBOUND = set()

mxd_fl = {"ASTENOT": {"list": mxdASTENOT, "in_mxd": False},
          "ASTIK": {"list": mxdASTIK, "in_mxd": False},
          "ASTOTA": {"list": mxdASTOTA, "in_mxd": False},
          "ASTTOM": {"list": mxdASTTOM, "in_mxd": False},
          "BLD": {"list": mxdBLD, "in_mxd": False},
          "CBOUND": {"list": mxdCBOUND, "in_mxd": False},
          "DBOUND": {"list": mxdDBOUND, "in_mxd": False},
          "FBOUND": {"list": mxdFBOUND, "in_mxd": False},
          "PRE_FBOUND": {"list": mxdPRE_FBOUND, "in_mxd": False},
          "PST": {"list": mxdPST, "in_mxd": False},
          "ROADS": {"list": mxdROADS, "in_mxd": False},
          "EAS": {"list": mxdEAS, "in_mxd": False},
          "VST": {"list": mxdVST, "in_mxd": False},
          "RBOUND": {"list": mxdRBOUND, "in_mxd": False}}

loc_fl = {"ASTENOT": locASTENOT,
          "ASTIK": locASTIK,
          "ASTOTA": locASTOTA,
          "ASTTOM": locASTTOM,
          "BLD": locBLD,
          "CBOUND": locCBOUND,
          "DBOUND": locDBOUND,
          "FBOUND": locFBOUND,
          "PRE_FBOUND": locPRE_FBOUND,
          "PST": locPST,
          "ROADS": locROADS,
          "EAS": locEAS,
          "VST": locVST,
          "RBOUND": locRBOUND}

req_map = {'merge': kt.merging_list,
           'shapes': ['ASTENOT', 'ASTTOM', 'PST'],
           'export_per_ota': ['ASTOTA'],
           'fbound_geometry': ['FBOUND'],
           'pst': ['PST'],
           'asttom': ['ASTTOM'],
           'astenot': ['ASTENOT']}


def choose_roads(roads):
    if roads == 'old':
        rd_shape = "iROADS"
    else:
        rd_shape = "ROADS"

    return rd_shape


def turn_off():
    dataframes = df_now()

    for df in dataframes:
        for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if "merge_" in _lyr.name or "union_" in _lyr.name or "_sum" in _lyr.name or "_in" in _lyr.name or "FBOUND" in _lyr.name:
                _lyr.visible = False

    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()


def add_layer(features, lyr=False):
    if get_pass():
        dataframes = df_now('add_layers')

        if lyr:
            shapes_list = [str(shape.lower()) for shape in features]

            for feature in shapes_list:
                try:
                    if mode:
                        lyr_name = "{}_all.lyr".format(feature)
                    else:
                        lyr_name = "{}.lyr".format(feature)

                    path = cp([meleti, lyr_i, lyr_name])

                    layer_to_add = arcpy.mapping.Layer(path)
                    arcpy.mapping.AddLayer(dataframes, layer_to_add, "AUTO_ARRANGE")
                except ValueError:
                    pm("Den uparxei to lyr arxeio : {}".format(feature))
        else:
            for feature in features:
                try:
                    layer_to_add = arcpy.mapping.Layer(paths.gdbm(feature))
                    arcpy.mapping.AddLayer(dataframes, layer_to_add, "AUTO_ARRANGE")
                except ValueError:
                    pm("Den uparxei to arxeio : {}".format(feature))

        if not lyr:
            turn_off()

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
    else:
        pass


def mxdfiles():
    dataframes = df_now()

    for df in dataframes:
        for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
            lyr_name = _lyr.name[:-6]

            try:
                if _lyr.name not in mxd_fl[lyr_name]['list']:
                    mxd_fl[lyr_name]['list'].add(str(_lyr.name))
                    if not mxd_fl[lyr_name]['in_mxd']:
                        mxd_fl[lyr_name]['in_mxd'] = True
            except KeyError:
                pass


def localfiles():
    for ota in kt.ota_list:
        for shape in kt.local_data_to_index_list:
            local_lyr = paths.ktima(ota, shape, ext=True)

            lyr_name = shape + "_" + ota

            if arcpy.Exists(local_lyr):
                try:
                    loc_fl[shape].add(str(lyr_name))
                except KeyError:
                    pass


def validate():
    def find_missing(mxdlist, locallist):
        loc_miss = mxdlist.difference(locallist)
        mxd_miss = locallist.difference(mxdlist)

        lm = sorted(loc_miss)
        mm = sorted(mxd_miss)

        if not mm and not lm:
            pm("OK")
        elif mm:
            pm("MXD missing --> {}".format(mm))
        elif lm:
            pm("LocalData missing --> {}".format(lm))

    for shape in mxd_fl:
        if mxd_fl[shape]['in_mxd']:
            find_missing(mxd_fl[shape]['list'], loc_fl[shape])


def change_mode():
    kt.ota_list = ['06005', '06013', '06041', '06060', '06062', '06075', '06111', '06132', '06191', '06199', '06200', '06212']
    mode.append('ALL')
    localfiles()
    pm('\n\nChanged Mode for {}\nMode : {}\n'.format(meleti, mode))


def mxd(func):
    def wrapper(*args, **kwargs):
        if mxdName == mxdKtimaName and func.__name__ != 'merge':
            add_layer(req_map[func.__name__], lyr=True)  # add_layer() from 'merge' is executed from the toolbox
            mxdfiles()
            validate()
            result = func(*args, **kwargs)
        else:
            mxdfiles()
            validate()
            result = func(*args, **kwargs)

        return result

    return wrapper


localfiles()
