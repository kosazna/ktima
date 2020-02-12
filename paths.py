# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from handler import *


class Paths:
    def __init__(self, meleti, mel_type, company_name):
        self.mel_type = mel_type
        self.company_name = company_name
        self.meleti = meleti

        self.company_gdb_name = 'ktima.gdb'
        self.standalone_gdb_name = 'standalone.gdb'

        self.mdb_general = cp([meleti, gdbs, 'archive.mdb'])
        self.gdb_standalone = cp([meleti, gdbs, self.standalone_gdb_name])
        self.gdb_company = cp([meleti, gdbs, self.company_gdb_name])

        self.rdoutpath = cp([meleti, inputdata, shapefiles_i])
        self.rdinpath = cp([meleti, inputdata, shapefiles_i, 'ROADS_ALL.shp'])

        self.fboundoutpath = cp([meleti, inputdata, shapefiles_i])
        self.fboundinpath = cp([meleti, inputdata, shapefiles_i,
                                'FBOUND_ALL.shp'])

        self.prefboundoutpath = cp([meleti, inputdata, shapefiles_i])
        self.prefboundinpath = cp([meleti, inputdata, shapefiles_i,
                                   'PRE_FBOUND_ALL.shp'])

        self.claimoutpath = cp([meleti, inputdata, shapefiles_i])
        self.claiminpath = cp([meleti, inputdata, shapefiles_i,
                               'FBOUND_CLAIM.shp'])

        self.predasinpath = cp([meleti, inputdata, shapefiles_i, po_i,
                                'KYR_PO_PARCELS.shp'])
        self.dasinpath = cp([meleti, inputdata, shapefiles_i, po_i,
                             'PO_PARCELS.shp'])

        self.locality = cp([meleti, inputdata, docs_i, 'LOCALITY.txt'])
        self.fbounddoc = cp([meleti, inputdata, docs_i, 'FBOUND_DOCS.txt'])
        self.status_path = cp([meleti, inputdata, docs_i, 'KT_Status.json'])
        self.kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

        self.mdb_in = cp([meleti, inputdata, databases_i])
        self.mdb_out = cp([meleti, outputdata, paradosimdb_o])
        self.mdb_vsteas = cp([meleti, outputdata, paradosidata_o])

        self.old_roads = cp([meleti, inputdata, shapefiles_i, roadsold_i])
        self.new_roads = cp([meleti, outputdata, paradosidata_o])

        self.localdata = cp([meleti, outputdata, localdata_o])
        self.paradosidata = cp([meleti, outputdata, paradosidata_o])

        self.block_pnt_xml = cp([meleti, inputdata, xml_i,
                                 'BLOCK_PNT_METADATA.xml'])
        self.geo_xml = cp([meleti, inputdata, xml_i, 'GEO_METADATA.xml'])
        self.roads_xml = cp([meleti, inputdata, xml_i, 'ROADS_METADATA.xml'])

        self.anakt_in = cp([meleti, inputdata, anakt])
        self.anakt_out = cp([meleti, outputdata, anakt])

        self.saromena_in = cp([meleti, inputdata, saromena])
        self.saromena_out = cp([meleti, outputdata, saromena])

        self.checks_out = cp([mdev, '! --CHECKS-- !', meleti],
                             origin=ktl['temp'][user])


    def server(self, ota, shp):
        if self.company_name == 'NAMA':
            return cp([ota, 'SHP', shp + '.shp'], origin=ktl['data'][user])
        elif self.company_name == '2KP':
            return cp([ota, 'SHP', shp, shp + '.shp'], origin=ktl['data'][user])

    def ktima(self, ota_folder, fc, ext=False, spatial_folder=localdata_o):
        if ext:
            if self.mel_type == 1:
                return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                           "SHAPE", fc, fc + ".shp"])
            else:
                return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                           fc, fc + ".shp"])
        else:
            if self.mel_type == 1:
                return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                           "SHAPE", fc])
            else:
                return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                           fc])

    def meta(self, ota, meta):
        if self.mel_type == 1:
            return cp([self.meleti, outputdata, paradosidata_o, ota,
                       'METADATA', meta + '.xml'])
        else:
            return cp([self.meleti, outputdata, paradosidata_o, ota,
                       meta + '.xml'])

    def mdf(self, fc, importance, out):
        if out == 'general':
            return cp([self.meleti, outputdata, shapefiles_o,
                       importance + fc])
        elif out == 'ota':
            return cp([self.meleti, outputdata, shapefiles_o,
                       importance + 'OTA', fc])

    def gdbc(self, fc=None):
        if fc is None:
            return self.gdb_company
        else:
            return os.path.join(self.gdb_company, fc)

    def gdbs(self, fc=None):
        if fc is None:
            return self.gdb_standalone
        else:
            return os.path.join(self.gdb_standalone, fc)

    def mdb(self, fc=None):
        if fc is None:
            return self.mdb_general
        else:
            return os.path.join(self.mdb_general, fc)

    def server_folder(self, ota, shp):
        if self.company_name == 'NAMA':
            return cp([ota, 'SHP'], origin=ktl['data'][user])
        elif self.company_name == '2KP':
            return cp([ota, 'SHP', shp], origin=ktl['data'][user])

    def ktima_folder(self, ota_folder, fc, spatial_folder=localdata_o):
        if self.mel_type == 1:
            return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                       "SHAPE", fc])
        else:
            return cp([self.meleti, outputdata, spatial_folder, ota_folder,
                       fc])
