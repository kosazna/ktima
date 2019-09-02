# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
dataframes = arcpy.mapping.ListDataFrames(mxd)


def files(x):
    for i in dataframes:
        for lyr in arcpy.mapping.ListLayers(mxd, "", i):
            lyr.name = lyr.name + '_' + lyr.workspacePath.split('\\')[-x]

    arcpy.RefreshTOC()

    return
