# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from win.update import *

meleti = (raw_input("\n\nMeleti\n\n").upper())

kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])


def build_structure():
    # repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'Folder_Structure'], origin=ktl['temp'][user])
    repo = r"C:\Users\aznavouridis.k\Desktop\repo\Folder_Structure"
    target = r"C:\{}".format(meleti)

    try:
        copytree(repo, target)
    except WindowsError:
        print('"{}" directory already exists'.format(target))


def update_basic_structure():
    # repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'Folder_Structure'], origin=ktl['temp'][user])
    repo = r"C:\Users\aznavouridis.k\Desktop\repo\Folder_Structure"
    for dirpath, dirnames, filenames in os.walk(repo):
        outpath = [meleti] + dirpath.split('\\')[6:]
        _dir = cp(outpath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            print('{} - Created'.format(_dir))


def update_folder_structure():
    # repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'File_Structure', meleti], origin=ktl['temp'][user])
    repo = r"C:\Users\aznavouridis.k\Desktop\repo\File_Structure\{}".format(meleti)
    for dirpath, dirnames, filenames in os.walk(repo):
        outpath = cp(dirpath.split('\\')[6:])
        if not os.path.exists(outpath):
            os.makedirs(outpath)


def update_file_structure():
    # repo = cp([mdev, 'Diafora', 'logs', 'scripts', 'File_Structure', meleti], origin=ktl['temp'][user])
    repo = r"C:\Users\aznavouridis.k\Desktop\repo\File_Structure\{}".format(meleti)
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
