# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This modules performs all subprocesses for the core processes.
# It also makes dictionaries with the available shapefiles

from data import *

# REQUIREMENTS FOR EACH FUNCTION FOR USE IN THE MXD DECORATOR
req_map = {'merge': info.merging_list,
           'shapes': ['ASTENOT', 'ASTTOM', 'PST'],
           'export_per_ota': ['ASTOTA'],
           'fbound_geometry': ['FBOUND'],
           'pst': ['PST'],
           'asttom': ['ASTTOM'],
           'astenot': ['ASTENOT']}

all_ktima = [
    "ASTENOT",
    "ASTIK",
    "ASTOTA",
    "ASTTOM",
    "BLD",
    "BLOCK_PNT",
    "CBOUND",
    "DBOUND",
    "OIK",
    "POI",
    "FBOUND",
    "PST",
    "ROADS",
    "IROADS"
    "EAS",
    "VST",
    "EIA_PNT",
    "EIA",
    "MRT",
    "NOMI",
    "VSTEAS_REL"]


def toc_layer(shape, ota):
    if shape == 'iROADS':
        return r'{}\ROADS_{}'.format(shape.lower(), ota)
    return r'{}\{}_{}'.format(shape.lower(), shape, ota)


class KTOrganizer:
    def __init__(self):
        self.loc_fl = {shape: set() for shape in all_ktima}
        self.mxd_fl = {shape: set() for shape in all_ktima}
        self.mxd_indexing = {shape: False for shape in all_ktima}
        self.available = dict.fromkeys(all_ktima)

    def localfiles(self):
        """
        Makes a list with the shapefiles of each spatial data category
        of Greek Cadastre.

        :return: Nothing
        """

        for shape in self.loc_fl.keys():
            for ota in info.ota_list:
                local_lyr = paths.ktima(ota, shape, ext=True)

                if os.path.exists(local_lyr):
                    self.loc_fl[shape].add(str(ota))

    def mxdfiles(self):
        """
        Scans the lyr packages loaded in the TOC and makes a list for
        eac category.

        :return: Nothing
        """

        dataframes = df_now()

        for df in dataframes:
            for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
                shape = _lyr.name[:-6]
                ota = _lyr.name[-5:]

                try:
                    self.mxd_fl[shape].add(str(ota))
                except KeyError:
                    pass

        for shape, otas in self.mxd_fl.items():
            if not self.mxd_indexing[shape]:
                if otas:
                    self.mxd_indexing[shape] = True
                    common = self.mxd_fl[shape].intersection(self.loc_fl[shape])
                    self.available[shape] = common

    def validate(self, validation_fc):
        """
        Finds and prints missing files.

        :param validation_fc: list
            Shapefile categories of Greek Cadastre to validate against.
        :return: Nothing
        """

        def find_missing(shp_name, mxdlist, locallist):
            loc_miss = mxdlist.difference(locallist)
            mxd_miss = locallist.difference(mxdlist)

            lm = sorted(loc_miss)
            mm = sorted(mxd_miss)

            if not mm and not lm:
                pm("{} - missing : None".format(shp_name))
            elif mm:
                pm("MXD missing - {}: {}".format(shp_name, mm))
            elif lm:
                pm("LocalData missing - {}: {}".format(shp_name, lm))

        pm('\n')

        for shape in validation_fc:
            if self.mxd_indexing[shape]:
                find_missing(shape, self.mxd_fl[shape], self.loc_fl[shape])

    @staticmethod
    def add_layer(features, lyr=False):
        """
        Function add feature class from a geodatabase or lyr package
        from LYR_Packages folder.

        :param features: list
            List of shapefiles to be added.
        :param lyr: boolean, optional
            If True layer is added from LYR_Packages.
            If False layer is added from geodatabase
            (default: False)
        :return: Nothing
        """

        if get_pass():
            dataframes = df_now('add_layers')

            if lyr:
                shapes_list = [str(shape.lower()) for shape in features]

                for feature in shapes_list:
                    try:
                        lyr_name = "{}.lyr".format(feature)

                        path = cp([MELETI, lyr_i, lyr_name])

                        layer_to_add = arcpy.mapping.Layer(path)
                        arcpy.mapping.AddLayer(dataframes,
                                               layer_to_add,
                                               "AUTO_ARRANGE")
                    except ValueError:
                        pm("LYR package does not exist : {}".format(feature))
            else:
                for feature in features:
                    try:
                        layer_to_add = arcpy.mapping.Layer(kt.gdb(feature))
                        arcpy.mapping.AddLayer(dataframes,
                                               layer_to_add,
                                               "AUTO_ARRANGE")
                    except ValueError as e:
                        pm(e)
                        pm("\n\nFile does not exist : {}".format(feature))

            if not lyr:
                turn_off()

            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
        else:
            pass

    def fetch(self, shape, missing='raise'):
        """
        Determines which for which otas shapefiles can be merged
        based on their availability and USER command

        :param shape: str
            Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
        :param missing: str, {'raise', 'ignore'}, optional
            Whether or nor missing shapefiles should be ignored
            (default: 'raise')
        :return: list
            List of otas
        """
        if shape == 'iROADS':
            shapefile = 'ROADS'
        else:
            shapefile = shape

        user_otas = set(kt.otas)
        end_otas = user_otas.intersection(self.available[shapefile])

        missing_from_user = end_otas.difference(user_otas)
        missing_ota = self.available[shapefile].difference(
            self.mxd_fl[shapefile])

        if kt.mode == KTIMA_MODE:
            if missing == 'raise':
                fcs = [toc_layer(shape, ota) for ota in self.mxd_fl[shapefile]]
                return sorted(fcs)
            elif missing == 'ignore':
                if missing_ota:
                    for ota in sorted(missing_ota):
                        pm('{}_{} source file not available.\n'.format(
                            shapefile,
                            ota))
                    pm('\nProcess continues. Missing files IGNORED.\n')
                fcs = [toc_layer(shape, ota) for ota in
                       self.available[shapefile]]
                return sorted(fcs)
        elif kt.mode == STANDALONE_MODE:
            if missing == 'raise':
                fcs = [toc_layer(shape, ota) for ota in kt.otas]
                return sorted(fcs)
            elif missing == 'ignore':
                if missing_from_user:
                    for ota in sorted(missing_from_user):
                        pm('{}_{} source file not available.\n'.format(
                            shapefile,
                            ota))
                    pm('\nProcess continues. Missing files IGNORED.\n')
                fcs = [toc_layer(shape, ota) for ota in end_otas]
                return sorted(fcs)


def choose_roads(roads_type):
    """
    Chooses roads for processing.

    :param roads_type: str
        - 'old': old roads in InpusData
        - 'new': new roads from localdata
    :return: str
        'iROADS' if 'old' else 'ROADS' if 'new'
    """

    if roads_type == 'old':
        rd_shape = "iROADS"
    else:
        rd_shape = "ROADS"

    return rd_shape


def turn_off():
    """
    Turns off layers in ArcGIS.

    :return: Nothing
    """

    dataframes = df_now()

    chk = ['merge_', 'union_', '_sum', '_in', 'FBOUND']

    for df in dataframes:
        for _lyr in arcpy.mapping.ListLayers(mxd, "", df):
            for ch in chk:
                if ch in _lyr.name:
                    _lyr.visible = False

    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()


def mxd(func):
    def wrapper(*args, **kwargs):
        if mxdName == mxdKtimaName and func.__name__ != 'merge':
            org.add_layer(req_map[func.__name__], lyr=True)
            # add_layer() for 'merge' is executed from the toolbox
        org.mxdfiles()
        org.validate(req_map[func.__name__])
        result = func(*args, **kwargs)

        return result

    return wrapper


org = KTOrganizer()

org.localfiles()
