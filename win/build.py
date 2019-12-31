# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from update import *

username = raw_input("\n\nUsername:\n")
password = getpass.getpass("\nPassword:\n")

if username == mdev.strip('! ') and password == build_pass:
    meleti = (raw_input("\n\nMeleti\n\n").upper())

    kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])


def buildtree():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'], origin=ktl['temp'][user])
    else:
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'], origin=ktl['temp'][user])

    target = r"C:\{}".format(meleti)

    try:
        shutil.copytree(repo, target)
    except WindowsError:
        print('"{}" directory already exists  or  Source directory missing'.format(target))


def update_folder_structure():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', meleti], origin=ktl['temp'][user])
    elif ktl.get('company_name', 'NOT_FOUND') == '2KP':
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'File_Structure', meleti], origin=ktl['temp'][user])
    else:
        print('"company_name" not defined in paths.json')

    def _d(x):
        for dirpath, dirnames, filenames in os.walk(repo):
            outpath = cp(dirpath.split('\\')[x:])
            if not os.path.exists(outpath):
                os.makedirs(outpath)

    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        _d(5)
    elif ktl.get('company_name', 'NOT_FOUND') == '2KP':
        _d(6)


def update_file_structure():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', meleti], origin=ktl['temp'][user])
    elif ktl.get('company_name', 'NOT_FOUND') == '2KP':
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'File_Structure', meleti], origin=ktl['temp'][user])
    else:
        print('"company_name" not defined in paths.json')

    def _d(x):
        for dirpath, dirnames, filenames in os.walk(repo):
            for filename in filenames:
                inpath = os.path.join(dirpath, filename)
                outpath = cp(inpath.split('\\')[x:])
                c_copy(inpath, outpath)

    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        _d(5)
    else:
        _d(6)


def make_empty_dirs():
    data = load_json(kt_info_path)

    mdb_out = cp([meleti, outputdata, paradosimdb_o])
    anakt_out = cp([meleti, outputdata, anakt])
    saromena_out = cp([meleti, outputdata, saromena])
    dirs = [anakt_out, saromena_out, mdb_out]

    for _dir in dirs:
        for ota in data['ota_list']:
            os.mkdir(os.path.join(_dir, ota))


def start_logs():
    kt_target = cp([meleti, '!{}_log.txt'.format(meleti)])
    user_target = cp([users, user, 'KT_log.txt'])

    with open(kt_target, 'w') as f:
        f.write('{:<22}{:<9}{:<25}{}'.format('DATETIME', 'MELETI', 'ACTION', 'COMMENTS'))

    if os.path.exists(user_target):
        print('User {} already logging'.format(user))
    else:
        with open(user_target, 'w') as f:
            f.write('{:<22}{:<9}{:<20}{:<9}{:<25}{}'.format('DATETIME', 'SERVER', 'USER', 'MELETI', 'ACTION', 'COMMENTS'))


def updatetree():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'], origin=ktl['temp'][user])
    elif ktl.get('company_name', 'NOT_FOUND') == '2KP':
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'], origin=ktl['temp'][user])
    else:
        print('"company_name" not defined in paths.json')

    def _d(x):
        for dirpath, dirnames, filenames in os.walk(repo):
            outpath = [meleti] + dirpath.split('\\')[x:]
            _dir = cp(outpath)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
                print('{} - Created'.format(_dir))

    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        _d(5)
    else:
        _d(6)


def update_ktima_info():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', meleti, inputdata, docs_i, 'KT_Info.json'], origin=ktl['temp'][user])
    else:
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'File_Structure', meleti, inputdata, docs_i, 'KT_Info.json'], origin=ktl['temp'][user])

    target = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

    c_copy(repo, target)


def update_temp_paths():
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        repo = cp([mdev, 'Diafora', 'ktima', 'paths.json'], origin=ktl['temp'][user])
    else:
        repo = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'paths.json'], origin=ktl['temp'][user])

    target = cp([users, user, 'paths.json'])

    c_copy(repo, target)


def get_binary():
    update_from_server()
