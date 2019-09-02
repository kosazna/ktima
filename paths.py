# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import getpass
from cust_win import *

user = getpass.getuser()

gd = {'aznavouridis.k': 'D',
      'user1': 'C'}

inputdata = "!InputData"
outputdata = "!OutputData"
geodatabases = "Geodatabases"
shapefiles_i = "Shapefiles"
docs_i = "Docs"
po_i = "PO"
databases_i = "Databases"
roadsold_i = "RoadsOld"
xml_i = "XML_Prototypes"
lyr_i = "LYR_Packages"
shapefiles_o = "Shapefiles"
localdata_o = "LocalData"
paradosidata_o = "ParadosiData"
paradosimdb_o = "ParadosiMDB"
users = "Users"
mdev = "! aznavouridis.k"


class KtimaPaths:
    def __init__(self, meleti, mel_type):
        self.meleti = meleti
        self.mel_type = mel_type

    def __call__(self, ota_folder, fc, ext=False, spatial_folder=localdata_o):
        if ext:
            if self.mel_type == 1:
                fc_path = cp([self.meleti, outputdata, spatial_folder, ota_folder, "SHAPE", fc, fc + ".shp"])
            else:
                fc_path = cp([self.meleti, outputdata, spatial_folder, ota_folder, fc, fc + ".shp"])
        else:
            if self.mel_type == 1:
                fc_path = cp([self.meleti, outputdata, spatial_folder, ota_folder, "SHAPE", fc])
            else:
                fc_path = cp([self.meleti, outputdata, spatial_folder, ota_folder, fc])

        return fc_path
