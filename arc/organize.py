# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from data import *

req_map = {'merge': lut.merging_list,
           'shapes': ['ASTENOT', 'ASTTOM', 'PST'],
           'export_per_ota': ['ASTOTA'],
           'fbound_geometry': ['FBOUND'],
           'pst': ['PST'],
           'asttom': ['ASTTOM'],
           'astenot': ['ASTENOT']}

locASTIK = set()
locASTOTA = set()
locASTENOT = set()
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


class Organizer:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

        self.mxdASTENOT = set()
        self.mxdASTIK = set()
        self.mxdASTOTA = set()
        self.mxdASTTOM = set()
        self.mxdBLD = set()
        self.mxdCBOUND = set()
        self.mxdDBOUND = set()
        self.mxdEAS = set()
        self.mxdPST = set()
        self.mxdVST = set()
        self.mxdRBOUND = set()
        self.mxdROADS = set()
        self.mxdFBOUND = set()
        self.mxdPRE_FBOUND = set()

        self.mxd_fl = {"ASTENOT": {"list": self.mxdASTENOT,
                                   "in_mxd": False},
                       "ASTIK": {"list": self.mxdASTIK,
                                 "in_mxd": False},
                       "ASTOTA": {"list": self.mxdASTOTA,
                                  "in_mxd": False},
                       "ASTTOM": {"list": self.mxdASTTOM,
                                  "in_mxd": False},
                       "BLD": {"list": self.mxdBLD,
                               "in_mxd": False},
                       "CBOUND": {"list": self.mxdCBOUND,
                                  "in_mxd": False},
                       "DBOUND": {"list": self.mxdDBOUND,
                                  "in_mxd": False},
                       "FBOUND": {"list": self.mxdFBOUND,
                                  "in_mxd": False},
                       "PRE_FBOUND": {"list": self.mxdPRE_FBOUND,
                                      "in_mxd": False},
                       "PST": {"list": self.mxdPST,
                               "in_mxd": False},
                       "ROADS": {"list": self.mxdROADS,
                                 "in_mxd": False},
                       "EAS": {"list": self.mxdEAS,
                               "in_mxd": False},
                       "VST": {"list": self.mxdVST,
                               "in_mxd": False},
                       "RBOUND": {"list": self.mxdRBOUND,
                                  "in_mxd": False}}

    def add_layer(self, features, lyr=False):
        if get_pass():
            dataframes = df_now('add_layers')

            if lyr:
                shapes_list = [str(shape.lower()) for shape in features]

                for feature in shapes_list:
                    try:
                        lyr_name = "{}.lyr".format(feature)

                        path = cp([meleti, lyr_i, lyr_name])

                        layer_to_add = arcpy.mapping.Layer(path)
                        arcpy.mapping.AddLayer(dataframes,
                                               layer_to_add,
                                               "AUTO_ARRANGE")
                    except ValueError:
                        pm("Den uparxei to lyr arxeio : {}".format(feature))
            else:
                for feature in features:
                    try:
                        layer_to_add = arcpy.mapping.Layer(self.gdb(feature))
                        arcpy.mapping.AddLayer(dataframes,
                                               layer_to_add,
                                               "AUTO_ARRANGE")
                    except ValueError:
                        pm("Den uparxei to arxeio : {}".format(feature))

            if not lyr:
                turn_off()

            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
        else:
            pass

    def mxdfiles(self):
        dataframes = df_now()

        for df in dataframes:
            for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
                lyr_name = _lyr.name[:-6]

                try:
                    if _lyr.name not in self.mxd_fl[lyr_name]['list']:
                        self.mxd_fl[lyr_name]['list'].add(str(_lyr.name))
                        if not self.mxd_fl[lyr_name]['in_mxd']:
                            self.mxd_fl[lyr_name]['in_mxd'] = True
                except KeyError:
                    pass

    def validate(self, validation_fc):
        def find_missing(shp_name, mxdlist, locallist):
            loc_miss = mxdlist.difference(locallist)
            mxd_miss = locallist.difference(mxdlist)

            lm = sorted([i[-5:] for i in loc_miss])
            mm = sorted([i[-5:] for i in mxd_miss])

            if not mm and not lm:
                pm("{} - missing : None".format(shp_name))
            elif mm:
                pm("MXD missing - {}: {}".format(shp_name, mm))
            elif lm:
                pm("LocalData missing - {}: {}".format(shp_name, lm))

        for shape in validation_fc:
            if self.mxd_fl[shape]['in_mxd']:
                find_missing(shape, self.mxd_fl[shape]['list'], loc_fl[shape])

    def available(self, feature, ota_num=False):
        _mxd = self.mxd_fl[feature]['list']
        _local = loc_fl[feature]

        common = sorted(list(_mxd.intersection(_local)))

        return [ota[-5:] for ota in common] if ota_num else common


def choose_roads(roads):
    if roads == 'old':
        rd_shape = "iROADS"
    else:
        rd_shape = "ROADS"

    return rd_shape


def turn_off():
    dataframes = df_now()

    chk = ['merge_', 'union_', '_sum', '_in', 'FBOUND']

    for df in dataframes:
        for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
            for ch in chk:
                if ch in _lyr.name:
                    _lyr.visible = False

    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()


def localfiles():
    for ota in lut.ota_list:
        for shape in lut.local_data_to_index_list:
            local_lyr = paths.ktima(ota, shape, ext=True)

            lyr_name = shape + "_" + ota

            if arcpy.Exists(local_lyr):
                try:
                    loc_fl[shape].add(str(lyr_name))
                except KeyError:
                    pass


def mxd(func):
    def wrapper(*args, **kwargs):
        if mxdName == mxdKtimaName and func.__name__ != 'merge':
            org[kt.mode].add_layer(req_map[func.__name__], lyr=True)
            # add_layer() for 'merge' is executed from the toolbox
        org[kt.mode].mxdfiles()
        org[kt.mode].validate(req_map[func.__name__])
        result = func(*args, **kwargs)

        return result

    return wrapper


localfiles()

org = {ktima_m: Organizer(ktima_m),
       standalone_m: Organizer(standalone_m)}
