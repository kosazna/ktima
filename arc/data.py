# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.status import *

arcpy.env.overwriteOutput = True

mxd = arcpy.mapping.MapDocument("CURRENT")
mxdPath = mxd.filePath
mxdName = os.path.basename(mxdPath)

mxdStandaloneName = "Standalone.mxd"
mxdKtimaName = "Ktima.mxd"

meleti = "None"
mel_type = "None"


class Kt:
    def __init__(self, mode, otas):
        self.mode = mode
        self.otas = otas

    def reset_mode(self, mode, otas):
        self.mode = mode
        self.otas = otas


if get_pass():
    if mxdName == mxdStandaloneName or mxdName == mxdKtimaName:
        meleti = mxdPath.split('\\')[1]
    else:
        pass
else:
    pm("\nAccess denied\n")
    print("\nAccess denied\n")

arcpy.env.workspace = cp([meleti, gdbs, 'company.gdb'])
kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

data = load_json(kt_info_path)

# Instantiating Classes

lut = NamesAndLists(data)
paths = Paths(meleti, lut.mel_type, lut.company_name)
lut = NamesAndLists(data)
kt = Kt('company', lut.ota_list)
log = Log(meleti)

status = {'company': Status(meleti, 'company'),
          'standalone': Status(meleti, 'standalone')}

gdb = {'company': paths.gdbc,
       'standalone': paths.gdbs}


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
