# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module contains within the Paths class all the necessary paths for
# the project

from handler import *


class KTPaths:
    """
    Paths has as attributes all the necessary file locations of the project
    and all the methods needed to create paths for different tasks

    Attributes
    ----------
    - mel_type : Type of project
    - company_name: Name of the company
    - meleti: Project
    - mdb_general: path for archive.mdb
    - gdb_standalone: path for standalone.gdb
    - gdb_ktima: path for ktima.gdb
    - localdata: path of localdata folder
    - paradosidata: path of paradosidata folder
    - ckecks_out: path for the server folder where checks are exported
    - locality: path of txt file containing ASTENOT locality ns
    - fbounddoc: path of txt file containing FBOUND DOC_ID ns
    - status_path: path of json file with the status of the project
    - kt_info_path: path of json file with all the info of the project
    - geo_xml: path of GEO_METADATA.xml
    - roads_xml: path of ROADS_METADATA.mxl
    - block_pnt_xml: path of BLOCK_PNT_METADATA.xml
    - anakt_in: folder path for the anaktiseis to be organized
    - anakt_out: folder path to organize anaktiseis
    - saromena_in: folder path for the scanned files to be organized
    - saromena_out: folder path to organize scanned files
    - rdoutpath: path for the merged ROADS shapefile to be exported
    - rdinpath: path of the merged ROADS shapefile
    - old_roads: path of the old roads (InputData)
    - new_roads: path for the new roads (LocalData)
    - fboundoutpath: path for the merged FBOUND shapefile to be exported
    - fboundinpath: path of the merged FBOUND shapefile
    - prefboundoutpath: path for the merged PRE_FBOUND shapefile to be exported
    - prefboundinpath: path of the merged PRE_FBOUND shapefile
    - claimoutpath: path for the forest claims shapefile to be exported
    - claiminpath: path of the forest claims shapefile
    - predasinpath: path of the forest shapefile given by authorities
    - dasinpath: path of the forest shapefile given by authorities
    - mdb_in: folder path to read mdbs
    - mdb_out: folder path to copy mdbs
    - mdb_vsteas: folder path for the VSTEAS mdbs

    Methods
    -------
    - server
    - ktima
    - meta
    - mdf
    - gdbc
    - gdbs
    - mdb
    - server_folder
    - ktima_folder
    """

    def __init__(self, meleti, mel_type, company_name):
        self.mel_type = mel_type
        self.company_name = company_name
        self.meleti = meleti

        # BASIC DATABASES
        self.mdb_general = cp([meleti, gdbs, ARCHIVE_MDB])
        self.gdb_standalone = cp([meleti, gdbs, STANDALONE_GDB])
        self.gdb_ktima = cp([meleti, gdbs, KTIMA_GDB])

        # BASIC PROJECT PATHS
        self.inputdata = cp([meleti, inputdata])
        self.localdata = cp([meleti, outputdata, localdata_o])
        self.paradosidata = cp([meleti, outputdata, paradosidata_o])
        self.checks_out = cp([mdev, '! --CHECKS-- !', meleti],
                             origin=ktl['temp'][USER])

        # BASIC DOCS
        self.locality = cp([meleti, inputdata, docs_i, 'LOCALITY.txt'])
        self.fbounddoc = cp([meleti, inputdata, docs_i, 'FBOUND_DOCS.txt'])
        self.status_path = cp([meleti, inputdata, docs_i, json_status])
        self.kt_info_path = cp([meleti, inputdata, docs_i, json_info])
        self.kt_naming = cp([meleti, inputdata, docs_i, json_naming])

        # XML DOCS
        self.geo_xml = cp([meleti, inputdata, xml_i, 'GEO_METADATA.xml'])
        self.roads_xml = cp([meleti, inputdata, xml_i, 'ROADS_METADATA.xml'])
        self.block_pnt_xml = cp([meleti, inputdata, xml_i,
                                 'BLOCK_PNT_METADATA.xml'])

        # TIFS
        self.anakt_in = cp([meleti, inputdata, anakt])
        self.anakt_out = cp([meleti, outputdata, anakt])
        self.saromena_in = cp([meleti, inputdata, saromena])
        self.saromena_out = cp([meleti, outputdata, saromena])

        # ROADS
        self.rdoutpath = cp([meleti, inputdata, shapefiles_i])
        self.rdinpath = cp([meleti, inputdata, shapefiles_i, 'ROADS_ALL.shp'])
        self.old_roads = cp([meleti, inputdata, shapefiles_i, roadsold_i])
        self.new_roads = cp([meleti, outputdata, paradosidata_o])

        # FOREST
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
        self.kyrdasinpath = cp([meleti, inputdata, shapefiles_i, po_i,
                                'KYR_PO_PARCELS.shp'])
        self.input_po = cp([meleti, inputdata, shapefiles_i, po_i])

        # MDBS
        self.mdb_in = cp([meleti, inputdata, databases_i])
        self.mdb_out = cp([meleti, outputdata, paradosimdb_o])
        self.mdb_vsteas = cp([meleti, outputdata, paradosidata_o])

        # EMPTY SHAPEFILES
        self.empty_shps = cp([meleti, inputdata, shapefiles_i, empty_shps])

    def server(self, ota, shp):
        """
        Creates server paths given ota_number and shp.
        The path is company and mel_type dependent

        :param ota: str
            Ota number.
        :param shp: str
            Spatial data shapefile of Greek Cadastre.
        :return: str
            Path of the shapefile.
        """

        if self.company_name == c_NA:
            return cp([ota, 'SHP', shp + '.shp'], origin=ktl['data'][USER])
        elif self.company_name == c_2P:
            return cp([ota, 'SHP', shp, shp + '.shp'], origin=ktl['data'][USER])

    def ktima(self, ota, shp, ext=False, spatial_folder=localdata_o):
        """
        Creates path for the local folder project

        :param ota: str
            Ota number.
        :param shp: str
            Spatial data shapefile of Greek Cadastre.
        :param ext: bolean, optional
            Whether or not the extension '.shp' will be added
            (default: False)
        :param spatial_folder: str, optional
            To whick folder will the shp_list be copied.
            (default: localdata_o)
        :return: str
            Final path depending on the mel_type
        """

        if ext:
            if self.mel_type == 1:
                return cp([self.meleti, outputdata, spatial_folder, ota,
                           "SHAPE", shp, shp + ".shp"])
            else:
                return cp([self.meleti, outputdata, spatial_folder, ota,
                           shp, shp + ".shp"])
        else:
            if self.mel_type == 1:
                return cp([self.meleti, outputdata, spatial_folder, ota,
                           "SHAPE", shp])
            else:
                return cp([self.meleti, outputdata, spatial_folder, ota,
                           shp])

    def meta(self, ota, meta):
        """
        Creates path for the given metadata type.

        :param ota: str
            Ota number.
        :param meta: str
            Type of metadata.
        :return: str
            Path for the metadata.
        """

        if self.mel_type == 1:
            return cp([self.meleti, outputdata, paradosidata_o, ota,
                       'METADATA', meta + '.xml'])
        else:
            return cp([self.meleti, outputdata, paradosidata_o, ota,
                       meta + '.xml'])

    def mdf(self, fc, importance, out):
        """
        mdf short for : Make Directories Files
        Creates paths for general purpose spatial data.

        :param fc: str
            Feature class or shapefile.
        :param importance: str
            Importance of the generated result usually expressed with
            exclamation mark. '!!' is more important that '!'
        :param out: str
            - 'general': general kind of output, one folder will be created.
            - 'ota': ota-based output, outputs of this type go to the
                    folder (\\!!OTA\\shp)
        :return: str
            Path for the output
        """

        if out == 'general':
            return cp([self.meleti, outputdata, shapefiles_o,
                       importance + fc])
        elif out == 'ota':
            return cp([self.meleti, outputdata, shapefiles_o,
                       importance + 'OTA', fc])

    def gdbk(self, fc=None):
        """
        Creates path for ktima gdb given a shapefile name.

        :param fc: str, optional
            Feature class or shapefile (default: None)
        :return: str
            Path for the feature class if given 'shp' else path of gdb
        """

        if fc is None:
            return self.gdb_ktima
        else:
            return os.path.join(self.gdb_ktima, fc)

    def gdbs(self, fc=None):
        """
        Creates path for standalone gdb given a shapefile name.

        :param fc: str, optional
            Feature class or shapefile (default: None)
        :return: str
            Path for the feature class if given 'shp' else path of gdb
        """

        if fc is None:
            return self.gdb_standalone
        else:
            return os.path.join(self.gdb_standalone, fc)

    def mdb(self, fc=None):
        """
        Creates path for archive mdb given a shapefile name.

        :param fc: str, optional
            Feature class or shapefile (default: None)
        :return: str
            Path for the feature class if given 'shp' else path of gdb
        """

        if fc is None:
            return self.mdb_general
        else:
            return os.path.join(self.mdb_general, fc)

    def server_folder(self, ota, shp):
        """
        Creates server paths for the folders given ota_number and shp.
        The path is company and mel_type dependent

        :param ota: str
            Ota number.
        :param shp: str
            Spatial data shapefile of Greek Cadastre.
        :return: str
            Path of the shapefile folder.
        """
        if self.company_name == c_NA:
            return cp([ota, 'SHP'], origin=ktl['data'][USER])
        elif self.company_name == c_2P:
            return cp([ota, 'SHP', shp], origin=ktl['data'][USER])

    def ktima_folder(self, ota, shp, spatial_folder=localdata_o):
        """
        Creates path for the local folder project.

        :param ota: str
            Ota number.
        :param shp: str
            Spatial data shapefile of Greek Cadastre.
        :param spatial_folder: str, optional
            To whick folder will the shp_list be copied.
            (default: localdata_o)
        :return: str
            Final folder depending on the mel_type
        """

        if self.mel_type == 1:
            return cp([self.meleti, outputdata, spatial_folder, ota,
                       "SHAPE", shp])
        else:
            return cp([self.meleti, outputdata, spatial_folder, ota,
                       shp])
