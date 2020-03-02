# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import arcpy


def pm(msg):
    arcpy.AddMessage(msg)


def get_count(fc):
    return int(arcpy.GetCount_management(fc)[0])


def clear_selection(fc):
    arcpy.SelectLayerByAttribute_management(fc, "CLEAR_SELECTION")


def list_fields(fc, data=""):
    """
    Shows the fields and their additional information of a feature class.

    :param fc: **str**
        Feature class or shapefile.
    :param data: **str**
        'name', 'type', 'length', 'precision', 'scale',
        'aliasName', 'baseName', 'defaultValue'
    :return: **list** or **dict**
        Returns a list if param "data" is specified.
        Returns a dict if param "data" is "" (default).
    """

    fields = {'name': [k.name for k in arcpy.ListFields(fc)],
              'type': [k.type for k in arcpy.ListFields(fc)],
              'length': [k.length for k in arcpy.ListFields(fc)],
              'precision': [k.precision for k in arcpy.ListFields(fc)],
              'scale': [k.scale for k in arcpy.ListFields(fc)],
              'aliasName': [k.aliasName for k in arcpy.ListFields(fc)],
              'baseName': [k.baseName for k in arcpy.ListFields(fc)],
              'defaultValue': [k.defaultValue for k in arcpy.ListFields(fc)]}

    return fields[data] if data else fields


def list_layers():
    _mxd = arcpy.mapping.MapDocument("CURRENT")
    _dataframes = arcpy.mapping.ListDataFrames(_mxd)

    list_shapefiles = [str(_lyr.name) for _df in _dataframes for _lyr in
                       arcpy.mapping.ListLayers(_mxd, "", _df)]

    return list_shapefiles


def list_gdb(path):
    arcpy.env.workspace = path
    featureclasses = arcpy.ListFeatureClasses()

    fc_list = [str(fc) for fc in featureclasses]

    return fc_list
