# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from uasm import *
from cust_arc import *
import datetime


def extract(mode, folder):
    inpath = cp([users, user, 'KT_log.txt'])
    filename = '{}_logs.txt'.format(user)

    if mode == "Local":
        try:
            outpath = cp([users, user, 'Desktop', filename])
            shutil.copyfile(inpath, outpath)
        except IOError:
            pass
    else:
        try:
            outpath = cp([mdev, 'Diafora', 'ktima', 'logs', filename], origin=folder)
            shutil.copyfile(inpath, outpath)
        except IOError:
            print('No such drive')


class Log:
    def __init__(self, meleti):
        self.meleti = meleti
        self.kt_log = cp([self.meleti, '!{}_log.txt'.format(self.meleti)])
        self.company_log = cp(['KTHMA_log.txt'], origin="K")
        self.general_log = cp([users, user, 'KT_log.txt'])

    def write_to_file(self, _datetime, msgf, commentsf):
        try:
            _user = ktl['users'][user]
        except KeyError:
            _user = user

        try:
            with open(self.company_log, 'a') as company_f:
                company_f.write('\n{}\t{}\t{}\t{}\t{}'.format(_datetime, _user, self.meleti, msgf, commentsf))
                server_loged = 'YES'
        except IOError:
            pm('\n\n! Logging !\n\n')
            server_loged = 'NO'

        with open(self.general_log, 'a') as general_f:
            with open(self.kt_log, 'a') as local_f:
                general_f.write('\n{}\t{}\t{}\t{}\t{}\t{}'.format(_datetime, server_loged, _user, self.meleti, msgf, commentsf))
                local_f.write('\n{}\t{}\t{}\t{}'.format(_datetime, self.meleti, msgf, commentsf))

    def __call__(self, msg, log_list=None):
        time_now = datetime.datetime.now().replace(microsecond=0)

        if msg == 'Check Shapefiles':
            comments = 'Check with: {0[0]} // Overlaps: ASTTOM - [{0[3]}] / ASTENOT - [{0[2]}] / PST - [{0[1]}] // Wrong KAEK: ASTENOT-ASTTOM - [{0[5]}] / PST-ASTENOT - [{0[4]}]'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Check PST Geometry':
            comments = 'Self Intersections - [{0[0]}] // OTA : {0[1]}'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Check ROADS':
            comments = 'Intersections : ALL - [{0[0]}] / Possible problems - [{0[1]}]'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Check DBOUND':
            comments = 'DBOUND missing "DEC_ID" or "DEC_DATE" : [{}]'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Check BLD':
            comments = 'BLD missing "BLD_T_C" or "BLD_NUM" : [{}]'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fix Geometry':
            comments = 'Repaired geometry in OTA : {}'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fix ROADS':
            comments = 'ROADS fixed'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fields PST':
            comments = 'Fixed PST Fields "ORI_TYPE"/"DEC_ID"/"ADDRESS"'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fields ASTTOM':
            comments = 'Deleting "ACQ_SCALE" field from ASTTOM'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fields ASTENOT':
            comments = 'Added "LOCALITY" info to ASTENOT fields'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Create FBOUND':
            comments = 'Created New FBOUND'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Create ROADS':
            comments = 'Created New ROADS'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Create FBOUND Claims':
            comments = 'FBOUND claims in [{}] KAEK'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Create PRE_FBOUND':
            comments = 'Created New PRE_FBOUND'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Export Shapefiles':
            comments = 'Copied files from {0[0]} to {0[1]}'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == "Organize files":
            comments = "Organized {} to !OutputData".format(log_list[0])
            self.write_to_file(time_now, msg, comments)
        elif msg == 'New ROADS to InputRoads folder':
            comments = "Copied new ROADS to Inputs folder for future testing".format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Clear directories':
            if log_list[1] == 'all':
                comments = 'Deleted all files from {}'.format(log_list[0])
            else:
                comments = "Deleted spare files from {}".format(log_list[0])
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Merge Shapefiles':
            comments = "Merged LocalData shapefiles for testing : {}".format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Check FBOUND Geometry':
            comments = 'Self Intersections - [{0[0]}] // OTA : {0[1]}'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Fix FBOUND Geometry':
            comments = 'Repaired FBOUND geometry in OTA : {}'.format(log_list)
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Copied old Roads to LocalData':
            comments = 'Copied old Roads to LocalData'
            self.write_to_file(time_now, msg, comments)
        elif msg == 'Metadata':
            comments = "Created Metadata for ParadosiData"
            self.write_to_file(time_now, msg, comments)
