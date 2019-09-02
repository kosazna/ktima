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

meleti = ""
mel_type = ""

if get_pass():
    if mxdName == mxdGeneralName or mxdName == mxdKtimaName:
        meleti = mxdPath.split('\\')[1]
    else:
        pass
else:
    pm("\nAccess denied\n")
    print("\nAccess denied\n")

arcpy.env.workspace = cp([meleti, geodatabases, 'checks.gdb'])

gdb_check = cp([meleti, geodatabases, 'checks.gdb'])
mdb_general = cp([meleti, geodatabases, 'archive.mdb'])
gdb_misc = cp([meleti, geodatabases, 'misc.gdb'])

rdoutpath = cp([meleti, inputdata, shapefiles_i])
rdinpath = cp([meleti, inputdata, shapefiles_i, 'ROADS_ALL.shp'])

fboundoutpath = cp([meleti, inputdata, shapefiles_i])
fboundinpath = cp([meleti, inputdata, shapefiles_i, 'FBOUND_ALL.shp'])

prefboundoutpath = cp([meleti, inputdata, shapefiles_i])
prefboundinpath = cp([meleti, inputdata, shapefiles_i, 'PRE_FBOUND_ALL.shp'])

claimoutpath = cp([meleti, inputdata, shapefiles_i])
claiminpath = cp([meleti, inputdata, shapefiles_i, 'FBOUND_CLAIM.shp'])

dasinpath = cp([meleti, inputdata, shapefiles_i, po_i, 'PO_PARCELS.shp'])
predasinpath = cp([meleti, inputdata, shapefiles_i, po_i, 'KYR_PO_PARCELS.shp'])

locality = cp([meleti, inputdata, docs_i, 'LOCALITY.txt'])
fbounddoc = cp([meleti, inputdata, docs_i, 'FBOUND_DOCS.txt'])
status_path = cp([meleti, inputdata, docs_i, 'KT_Status.json'])
kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

if get_pass():
    ktdata = load_json(kt_info_path)
    if mxdName == mxdGeneralName or mxdName == mxdKtimaName:
        mel_type = ktdata["mel_type"]
        ktima_paths = KtimaPaths(meleti, mel_type)
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


def gdbc(fc=None):
    if fc is None:
        return gdb_check
    else:
        return os.path.join(gdb_check, fc)


def gdbm(fc=None):
    if fc is None:
        return gdb_misc
    else:
        return os.path.join(gdb_misc, fc)


def mdb(fc=None):
    if fc is None:
        return mdb_general
    else:
        return os.path.join(mdb_general, fc)


def mdf(fc, importance='', out='general', ota=None, _name=None):
    """Make directories and files"""
    if out == 'general':
        outpath = cp([meleti, outputdata, shapefiles_o, importance + fc])
        name = fc
    elif out == 'ota':
        outpath = cp([meleti, outputdata, shapefiles_o, importance + 'OTA', fc])
        name = '{}_{}'.format(fc, ota)
    elif out == 'formal':
        name = _name
        outpath = ktima_paths(ota, _name)
    else:
        outpath = out
        name = fc

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    arcpy.FeatureClassToFeatureClass_conversion(fc, outpath, name)
    pm('Exported {}  ({})'.format(name, ota))

    if out == 'general':
        pm(r'--> {}\{}'.format(outpath, name))
