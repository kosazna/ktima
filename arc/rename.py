# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module has a single function for renaming layers in the ArcGIS TOC
# based on the ota number (SHP_OTA)

import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
dataframes = arcpy.mapping.ListDataFrames(mxd)


def files(x):
    """
    Renames the file to the format (PST_22000).

    :param x: **int**
        How many parent folders back is the ota number.
    :return: Nothing
    """
    
    for i in dataframes:
        for lyr in arcpy.mapping.ListLayers(mxd, "", i):
            lyr.name = lyr.name + '_' + lyr.workspacePath.split('\\')[-x]

    arcpy.RefreshTOC()

    return
