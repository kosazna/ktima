# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from win.update import *

meleti = (raw_input("\nMeleti\n").upper())

kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])


def build_structure():
    repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'Folder_Structure'], origin=ktl['temp'][user])
    target = r"C:\{}".format(meleti)

    try:
        copytree(repo, target)
    except WindowsError:
        print('"{}" directory already exists'.format(target))


def update_structure():
    repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'File_Structure'], origin=ktl['temp'][user])

    for dirpath, dirnames, filenames in os.walk(repo):
        for filename in filenames:
            inpath = os.path.join(dirpath, filename)
            outpath = cp(inpath.split('\\')[6:])
            c_copy(inpath, outpath)


def start_logs():
    kt_target = cp([meleti, '!{}_log.txt'.format(meleti)])
    user_target = cp([users, user, 'KT_log.txt'])

    with open(kt_target, 'w') as f:
        f.write('DATETIME\tMELETI\tACTION\tCOMMENTS')

    if os.path.exists(user_target):
        print('User {} already logging'.format(user))
    else:
        with open(user_target, 'w') as f:
            f.write('DATETIME\tMELETI\tACTION\tCOMMENTS')


def make_empty_dirs():
    data = load_json(kt_info_path)

    mdb_out = cp([meleti, outputdata, paradosimdb_o])
    anakt_out = cp([meleti, outputdata, anakt])
    saromena_out = cp([meleti, outputdata, saromena])
    dirs = [anakt_out, saromena_out, mdb_out]

    for _dir in dirs:
        for ota in data['ota_list']:
            os.mkdir(os.path.join(_dir, ota))
