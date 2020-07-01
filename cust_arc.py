# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module contains custom functions for ArcGIS internal use.

import arcpy


def pm(msg):
    """
    Custom function to print messages in ArcGIS.

    :param msg: str
        Text to be printed.
    :return: Nothing
    """

    arcpy.AddMessage(msg)


def get_count(fc):
    """
    Counts formatter many features a shapefile has.

    :param fc: str
        Shapefile or feature class .
    :return: int
        Number of features.
    """
    return int(arcpy.GetCount_management(fc)[0])


def clear_selection(fc):
    """
    Clears the selected features from a shapefile.

    :param fc: str
        Feature class or shapefile.
    :return: Nothing
    """

    arcpy.SelectLayerByAttribute_management(fc, "CLEAR_SELECTION")


def list_fields(fc, data=""):
    """
    Shows the fields and their additional information of a feature class.

    :param fc: str
        Feature class or shapefile.
    :param data: str
        'name', 'type', 'length', 'precision', 'scale',
        'aliasName', 'baseName', 'defaultValue'
    :return: list or dict
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
    """
    List the layers that are loaded in ArcGIS Table Of Contents.

    :return: list
        List of layers.
    """

    _mxd = arcpy.mapping.MapDocument("CURRENT")
    _dataframes = arcpy.mapping.ListDataFrames(_mxd)

    list_shapefiles = [str(_lyr.name) for _df in _dataframes for _lyr in
                       arcpy.mapping.ListLayers(_mxd, "", _df)]

    return list_shapefiles


def list_gdb(path):
    """
    List all the files of a File Geodatabase.

    :param path: str
        Path of the geodatabase.
    :return: list
        List with all the files in the gdb.
    """

    arcpy.env.workspace = path
    featureclasses = arcpy.ListFeatureClasses()

    fc_list = [str(fc) for fc in featureclasses]

    return fc_list


def clean_fields(fc1, fc2):
    """
    This function will create a list with the fields to be deleted.
    Given shapefile or feature class 'fc1' it will find it's field.
    The some will be done for 'fc2'

    It will be returned a list with the fields to be deleted, so that the
    fields of 'fc1' will remain in the final dataset. The fields which are
    not deleted are:
    'OBJECTID', 'FID', 'Shape_Length', 'Shape_Area', 'CAD_ADMIN'

    :param fc1: str
        Shapefile or feature class
    :param fc2: str
        Shapefile or feature class
    :return: list
        Fields to be deleted
    """

    s_fc1 = set(list_fields(fc1, 'name'))
    s_fc2 = set(list_fields(fc2, 'name'))

    no_del = ['OBJECTID', 'FID', 'Shape_Length', 'Shape_Area', 'CAD_ADMIN']

    diff = s_fc1.symmetric_difference(s_fc2)
    to_del = [str(i) for i in diff if i not in no_del]

    if 'Shape_Leng' in s_fc1:
        to_del.append('Shape_Leng')

    return to_del


def delete_fields(fc1, keep=None):
    """
    Given a shapefile or feature class, the function will create a list
    with it's field. The function will return all fields to be deleted
    if they are not in 'keep' list and the neccessary field list which is:
    'FID', 'OBJECTID', 'Shape'

    :param fc1: str
        Shapefile or feature class
    :param keep: list
        Fields to keep
    :return: list
        Fields to be deleted
    """

    if keep is None:
        no_del = ['FID', 'OBJECTID', 'Shape']
    else:
        no_del = keep + ['FID', 'OBJECTID', 'Shape']

    field_list = list_fields(fc1, 'name')

    to_del = [str(i) for i in field_list if i not in no_del]

    return to_del
