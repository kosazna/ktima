# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
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
    """ data : name, type, length, precision, scale, aliasName, baseName, defaultValue"""

    fields = {'name': [k.name for k in arcpy.ListFields(fc)],
              'type': [k.type for k in arcpy.ListFields(fc)],
              'length': [k.length for k in arcpy.ListFields(fc)],
              'precision': [k.precision for k in arcpy.ListFields(fc)],
              'scale': [k.scale for k in arcpy.ListFields(fc)],
              'aliasName': [k.aliasName for k in arcpy.ListFields(fc)],
              'baseName': [k.baseName for k in arcpy.ListFields(fc)],
              'defaultValue': [k.defaultValue for k in arcpy.ListFields(fc)]}

    return fields[data] if data else fields
