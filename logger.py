# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module is for logging all activities within the project
# for internal and external validations and research

from uasm import *
import datetime


def extract(mode, folder):
    """
    Copies the USER KT_log.txt in the server or in the USER desktop.

    :param mode: str
        - 'local': copies the log file to USER desktop
        - 'temp': copies the log file to the server
    :param folder: str
        Server drive letter of current USER.
    :return: Nothing
    """

    inpath = cp([users, USER, txt_log])
    filename = '{}_logs.txt'.format(USER)

    if mode == "Local":
        try:
            outpath = cp([users, USER, desktop, filename])
            shutil.copyfile(inpath, outpath)
        except IOError:
            pass
    else:
        try:
            outpath = cp([mdev, diafora, ktima_folder, logs, filename],
                         origin=folder)
            shutil.copyfile(inpath, outpath)
        except IOError:
            print('No such drive')


class KTLog:
    """
    Log exists so that each USER action can for the project is logged.

    Attributes
    ----------
    - meleti: meleti of the project.
    - kt_log: procect logger
    - company_log: server logger
    - general_log: USER logger
    - temp_log: temp logger

    Methods
    -------
    - write_to_file
    - __call__
    """

    def __init__(self, meleti):
        self.meleti = meleti
        self.kt_log = cp([self.meleti, '!{}_log.txt'.format(self.meleti)])
        self.company_log = cp([txt_server_log], origin=ktl['data'][USER])
        self.general_log = cp([users, USER, txt_log])
        self.temp_log = cp([mdev, diafora, ktima_folder, logs, 'KT_logs.txt'],
                           origin=ktl['temp'][USER])

    def write_to_file(self, dt, msgf, commentsf):
        """
        Opens logger and writes content.
        
        :param dt: str
            Datetime timestamp.
        :param msgf: str
            Action of the USER that is being registered.
        :param commentsf: str
            Comments for the USER action.
        :return: Nothing
        """

        try:
            _user = ktl['users'][USER]
        except KeyError:
            _user = USER

        try:
            with open(self.company_log, 'a') as company_f:
                company_f.write('\n{}   {:<20}{:<9}{:<25}{}'.format(dt,
                                                                    _user,
                                                                    self.meleti,
                                                                    msgf,
                                                                    commentsf))

                server_loged = 'YES'
        except IOError:
            server_loged = 'NO'

        try:
            with open(self.temp_log, 'a') as company_f:
                company_f.write('\n{}   {:<20}{:<9}{:<25}{}'.format(dt,
                                                                    _user,
                                                                    self.meleti,
                                                                    msgf,
                                                                    commentsf))
        except IOError:
            pass

        with open(self.general_log, 'a') as general_f:
            with open(self.kt_log, 'a') as local_f:
                general_f.write(
                    '\n{}   {:<9}{:<20}{:<9}{:<25}{}'.format(dt,
                                                             server_loged,
                                                             _user, self.meleti,
                                                             msgf, commentsf))
                local_f.write('\n{}   {:<9}{:<25}{}'.format(dt,
                                                            self.meleti,
                                                            msgf,
                                                            commentsf))

    def __call__(self, msg, log_list=None):
        """
        Object gets called and executes the write_to_file depending
        on the content.

        :param msg: str
            Action of the USER that is being registered.
        :param log_list: list
            List containing neccesary info for USER actions
        :return: Nothing
        """

        log_mapper = {
            'Check Overlaps': "%s / ASTTOM- [%d] / ASTENOT- [%d] / PST- [%d]",
            'Check PST Geometry': 'Self Intersections - [%d] // OTA : %s',
            'Check ROADS': 'Intersections: ALL - [%d]',
            'Check DBOUND': 'DBOUND missing "DEC_ID" or "DEC_DATE" : [%d]',
            'Check BLD': 'BLD missing "BLD_T_C" or "BLD_NUM" : [%d]',
            'Fix Geometry': 'Repaired geometry in OTA : %s',
            'Fix ROADS': 'ROADS fixed',
            'Fields PST': 'Fixed PST Fields "ORI_TYPE"/"DEC_ID"/"ADDRESS"',
            'Fields ASTTOM': 'Deleting "ACQ_SCALE" field from ASTTOM',
            'Fields ASTENOT': 'Added "LOCALITY" info to ASTENOT fields',
            'Create FBOUND': 'Created New FBOUND',
            'Create ROADS': 'Created New ROADS',
            'Create FBOUND Claims': 'FBOUND claims in [%d] KAEK',
            'Create PRE_FBOUND': 'Created New PRE_FBOUND',
            'Export Shapefiles': 'Copied files from %s to %s',
            'Organize files': "Organized %s to !OutputData",
            'Clear directories': 'Deleted from %s - %s files',
            'Merge Shapefiles': "Merged LocalData shp_list for testing : %s",
            'Check FBOUND Geometry': 'Self Intersections - [%d] // OTA : %s',
            'Fix FBOUND Geometry': 'Repaired FBOUND geometry in OTA : %s',
            'Copied iROADS to Local': 'Copied old Roads to LocalData',
            'Metadata': "Created Metadata for ParadosiData",
            'Update': 'Updated ktima to version: [%s]',
            'Change Mode': 'Changed mode to: [%s]',
            'Set Default Mode': 'Default mode set to: [%s]',
            'Count Shapefiles': '%s',
            'Check Numbering': "Wrong KAEK: ASTENOT - [%d] / PST - [%d]",
            'Check ASTOTA': "Check with: %s // Overlaps: [%d]",
            'Empty Shapefiles': 'Created empty shapefiles for : %s',
            'Docs update': 'Updated json schemas',
            'Fields FBOUND': 'Added DOC_ID info to FBOUNDs'}

        time_now = datetime.datetime.now().replace(microsecond=0)

        if log_list is None:
            comments = log_mapper[msg]
        elif isinstance(log_list, (str, int)):
            comments = log_mapper[msg] % log_list
        else:
            try:
                comments = log_mapper[msg] % tuple(log_list)
            except TypeError:
                comments = log_mapper[msg] % '-'.join(log_list)

        self.write_to_file(time_now, msg, comments)
