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

meleti = "None"
mel_type = "None"


class Kt:
    def __init__(self, meleti_, mode, otas):
        self.mode = mode
        self.otas = otas
        self.meleti = meleti_

    def reset_mode(self, mode, otas):
        self.mode = mode
        self.otas = otas
        status[self.mode].otas = self.otas

        pm('''
        Mode Changed !\n
        Mode : {}
        OTA : {}
        '''.format(self.mode, self.otas))

        for shape in lut.merging_list:
            status[self.mode].update('SHAPE', shape, False)


if get_pass():
    if mxdName == mxdKtimaName:
        meleti = mxdPath.split('\\')[1]
    else:
        pass
else:
    pm("\nAccess denied\n")
    print("\nAccess denied\n")

arcpy.env.workspace = cp([meleti, gdbs, 'ktima.gdb'])
kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

data = load_json(kt_info_path)

# Instantiating Classes

lut = NamesAndLists(data)
paths = Paths(meleti, lut.mel_type, lut.company_name)
lut = NamesAndLists(data)
kt = Kt(meleti, ktima_m, lut.ota_list)
log = Log(meleti)

status = {ktima_m: Status(meleti, ktima_m, lut.ota_list),
          standalone_m: Status(meleti, standalone_m, kt.otas)}

gdb = {ktima_m: paths.gdbc,
       standalone_m: paths.gdbs}


def df_now(step="list_layers"):
    if step == 'list_layers':
        _dataframes = arcpy.mapping.ListDataFrames(mxd)
    else:
        _dataframes = arcpy.mapping.ListDataFrames(mxd)[0]

    return _dataframes


def mdf(fc, importance='', out='general', ota=None, _name=None):
    """Make directories and files"""
    if out == 'general':
        outpath = paths.mdf(fc, importance, out)
        name = fc
    elif out == 'ota':
        outpath = paths.mdf(fc, importance, out)
        name = '{}_{}'.format(fc, ota)
    elif out == 'formal':
        name = _name
        outpath = paths.ktima(ota, _name)
    else:
        outpath = out
        name = fc

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    arcpy.FeatureClassToFeatureClass_conversion(fc, outpath, name)
    pm('Exported {}  ({})'.format(name, ota))

    if out == 'general':
        pm(r'--> {}\{}'.format(outpath, name))
