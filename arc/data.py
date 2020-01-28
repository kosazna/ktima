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

mxdGeneralName = "General.mxd"
mxdKtimaName = "Ktima.mxd"

meleti = "None"
mel_type = "None"
mode = []

if get_pass():
    if mxdName == mxdGeneralName or mxdName == mxdKtimaName:
        meleti = mxdPath.split('\\')[1]
    else:
        pass
else:
    pm("\nAccess denied\n")
    print("\nAccess denied\n")

arcpy.env.workspace = cp([meleti, geodatabases, 'checks.gdb'])
kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

if get_pass():
    data = load_json(kt_info_path)
    lut = NamesAndLists(data)
    if mxdName == mxdGeneralName or mxdName == mxdKtimaName:
        paths = Paths(meleti, lut.mel_type, lut.company_name)
        status = Status(meleti)
        log = Log(meleti)
else:
    pass


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
