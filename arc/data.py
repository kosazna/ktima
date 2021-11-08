# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module defines all information for the project so as ArcGIS can perform
# the tasks been provided

from status import *


class KTMode:
    """
    KTMode is the corner stone of the arc subpackage

    Attributes
    ----------
    - mode: mode for the current working session
    - otas: otas for the current working session
    - gdb: file geodatabase to store results
    - meleti: meleti of the project

    Methods
    -------
    - reset_mode
    - set_default_mode
    """

    def __init__(self, meleti, mode, otas):
        self.mode = mode
        self.otas = otas
        self.gdb = paths.gdbk if mode == KTIMA_MODE else paths.gdbs
        self.meleti = meleti

    def reset_mode(self, mode, otas):
        self.mode = mode
        self.otas = sorted(otas)
        self.gdb = paths.gdbk if mode == KTIMA_MODE else paths.gdbs
        status[self.mode].otas = otas

        pm('\nMODE : {}\n'.format(self.mode))
        pm('\nOTA : {}\n'.format('-'.join(self.otas)))

        if mode == STANDALONE_MODE:
            for shape in info.merging_list:
                status[mode].update('SHAPE', shape, False)

        log('Change Mode', log_list=str(mode))

    @staticmethod
    def set_default_mode(mode):
        data = load_json(kt_info_path)
        data['mode'] = mode
        write_json(kt_info_path, data)

        log('Set Default Mode', log_list=str(mode))


def df_now(command="list_layers"):
    """
    Chooses the way ListDataframes is to be executed.

    :param command: str, optional
        - 'list_layers' (default)
        - whatever else
    :return: Dataframe object of ArcGIS
    """

    if command == 'list_layers':
        _dataframes = arcpy.mapping.ListDataFrames(mxd)
    else:
        _dataframes = arcpy.mapping.ListDataFrames(mxd)[0]

    return _dataframes


def mdf(fc, importance='', out='general', ota=None, name=None):
    """
    Short for Make Directories and Files.

    :param fc: str
        Feature class or shapefile.
    :param importance: *str
        Importance of the generated result usually expressed with
        exclamation mark. '!!' is more important that '!'
    :param out: str, optional
        - 'general': general kind of output, one folder will be created.
        - 'ota': ota-based output, outputs of this type go to the
                folder (\\!!OTA\\shp)
        - 'formal': formal output based on the project structure
        (default: 'general')
    :param ota: str, optional
        Ota number (default: None)
    :param name: str, optional
        Name for the output shapefile (default: None)
    :return: Nothing
    """

    if out == 'general':
        outpath = paths.mdf(fc, importance, out)
        name = fc
    elif out == 'ota':
        outpath = paths.mdf(fc, importance, out)
        name = '{}_{}'.format(ota, fc)
    elif out == 'formal':
        name = name
        outpath = paths.ktima(ota, name)
    else:
        outpath = out
        name = fc

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    arcpy.FeatureClassToFeatureClass_conversion(fc, outpath, name)
    pm('Exported {}  ({})'.format(name, ota))

    if out == 'general':
        pm(r'--> {}\{}'.format(outpath, name))


def get_otas(companies):
    """
    Gets the otas which are under supervision of the companies provided.

    :param companies: list
        List of companies
    :return: list
        List with ota numbers
    """

    end_list = []

    if companies:
        for comp in companies:
            end_list += info.pool[comp]

    return end_list


if __name__ == 'ktima.arc.data':
    # DEFINING MELETI FOR THE SESSION

    arcpy.env.overwriteOutput = True

    mxd = arcpy.mapping.MapDocument("CURRENT")
    mxdPath = mxd.filePath
    mxdName = os.path.basename(mxdPath)

    mxdKtimaName = "Ktima.mxd"

    if get_pass():
        if mxdName == mxdKtimaName:
            MELETI = mxdPath.split('\\')[1]
            if MELETI in get_categories():
                can_process = True
            else:
                can_process = False
        else:
            MELETI = None
    else:
        MELETI = None
        can_process = False
        pm("\nAccess denied\n")
        print("\nAccess denied\n")

    # PATHS FOR THE PROJECT INFO AND NAMING SCHEMA
    kt_info_path = cp([MELETI, inputdata, docs_i, json_info])

    # DICTIONARIES OF THE PROJECT INFO AND NAMING SCHEMA
    info_data = load_json(kt_info_path)

    # INSTANTIATING CLASSES
    info = KTInfo(info_data)
    ns = KTNamingSchema(info)  # stands for naming schema
    paths = KTPaths(MELETI, info.mel_type, info.company_name)
    log = KTLog(MELETI)

    if info.mode == KTIMA_MODE:
        kt = KTMode(MELETI, info.mode, info.ota_list)
    else:
        kt = KTMode(MELETI, info.mode, info.mel_ota_list)

    if kt.mode == KTIMA_MODE:
        arcpy.env.workspace = paths.gdb_ktima
    else:
        arcpy.env.workspace = paths.gdb_standalone

    status = {KTIMA_MODE: KTStatus(MELETI, KTIMA_MODE, info.ota_list),
              STANDALONE_MODE: KTStatus(MELETI, STANDALONE_MODE, kt.otas)}
