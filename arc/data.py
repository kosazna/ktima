# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.status import *

arcpy.env.overwriteOutput = True

mxd = arcpy.mapping.MapDocument("CURRENT")
mxdPath = mxd.filePath
mxdName = os.path.basename(mxdPath)

mxdKtimaName = "Ktima.mxd"

MELETI = "None"
# MEL_TYPE = "None"


class Kt:
    def __init__(self, meleti, mode, otas):
        self.mode = mode
        self.otas = otas
        self.meleti = meleti

    def reset_mode(self, mode, otas):
        self.mode = mode
        self.otas = sorted(otas)
        status[self.mode].otas = otas

        pm('\nMODE : {}\n'.format(self.mode))
        pm('\nOTA : {}\n'.format(self.otas))

        for shape in lut.merging_list:
            status[mode].update('SHAPE', shape, False)

    @staticmethod
    def set_default_mode(mode):
        data = load_json(kt_info_path)
        data['mode'] = mode
        write_json(kt_info_path, data)


if get_pass():
    if mxdName == mxdKtimaName:
        MELETI = mxdPath.split('\\')[1]
    else:
        pass
else:
    pm("\nAccess denied\n")
    print("\nAccess denied\n")

# arcpy.env.workspace = cp([meleti, gdbs, 'ktima.gdb'])

kt_info_path = cp([MELETI, inputdata, docs_i, 'KT_Info.json'])
naming_path = cp([MELETI, inputdata, docs_i, 'KT_Naming_Schema.json'])

info_data = load_json(kt_info_path)
naming_data = load_json(naming_path)

# Instantiating Classes

lut = LookUpInfo(info_data, naming_data)
paths = Paths(MELETI, lut.mel_type, lut.company_name)
log = Log(MELETI)

if lut.mode == KTIMA_MODE:
    kt = Kt(MELETI, lut.mode, lut.ota_list)
else:
    kt = Kt(MELETI, lut.mode, lut.mel_ota_list)

if kt.mode == KTIMA_MODE:
    arcpy.env.workspace = paths.gdb_ktima
else:
    arcpy.env.workspace = paths.gdb_standalone

status = {KTIMA_MODE: Status(MELETI, KTIMA_MODE, lut.ota_list),
          STANDALONE_MODE: Status(MELETI, STANDALONE_MODE, kt.otas)}

gdb = {KTIMA_MODE: paths.gdbc,
       STANDALONE_MODE: paths.gdbs}


def df_now(command="list_layers"):
    if command == 'list_layers':
        _dataframes = arcpy.mapping.ListDataFrames(mxd)
    else:
        _dataframes = arcpy.mapping.ListDataFrames(mxd)[0]

    return _dataframes


def mdf(fc, importance='', out='general', ota=None, name=None):
    if out == 'general':
        outpath = paths.mdf(fc, importance, out)
        name = fc
    elif out == 'ota':
        outpath = paths.mdf(fc, importance, out)
        name = '{}_{}'.format(fc, ota)
    elif out == 'formal':
        name = name
        outpath = paths.ktima(ota, name)
    else:
        outpath = out
        name = fc

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    arcpy.FeatureClassToFeatureClass_conversion(fc, outpath, name)
    pm('Exported {}  ({})'.format(name, ota))

    if out == 'general':
        pm(r'--> {}\{}'.format(outpath, name))


def get_otas(companies):
    end_list = []

    if companies:
        for comp in companies:
            end_list += lut.koinopraksia[comp]

    return end_list
