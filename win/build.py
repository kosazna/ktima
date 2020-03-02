# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from update import *

username = raw_input("\n\nUsername:\n")
password = getpass.getpass("\nPassword:\n")


# def buildtree():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     target = r"C:\{}".format(meleti)
#
#     try:
#         shutil.copytree(repo, target)
#     except WindowsError:
#         print('"{}" already exists or Source directory missing'.format(target))
#
#
# def update_folder_structure():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', meleti],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure', meleti],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     pointer = len(repo.split('\\')) - 1
#
#     for dirpath, dirnames, filenames in os.walk(repo):
#         outpath = cp(dirpath.split('\\')[pointer:])
#         if not os.path.exists(outpath):
#             os.makedirs(outpath)
#
#
# def update_file_structure():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', meleti],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure', meleti],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     pointer = len(repo.split('\\')) - 1
#
#     for dirpath, dirnames, filenames in os.walk(repo):
#         for filename in filenames:
#             inpath = os.path.join(dirpath, filename)
#             outpath = cp(inpath.split('\\')[pointer:])
#             c_copy(inpath, outpath)
#
#
# def make_empty_dirs():
#     data = load_json(kt_info_path)
#
#     mdb_out = cp([meleti, outputdata, paradosimdb_o])
#     anakt_out = cp([meleti, outputdata, anakt])
#     saromena_out = cp([meleti, outputdata, saromena])
#     dirs = [anakt_out, saromena_out, mdb_out]
#
#     for _dir in dirs:
#         for ota in data['ota_list']:
#             os.mkdir(os.path.join(_dir, ota))
#
#
# def start_logs():
#     kt_target = cp([meleti, '!{}_log.txt'.format(meleti)])
#     user_target = cp([users, user, 'KT_log.txt'])
#
#     with open(kt_target, 'w') as f:
#         f.write('{:<22}{:<9}{:<25}{}'.format('DATETIME', 'MELETI',
#                                              'ACTION', 'COMMENTS'))
#
#     if os.path.exists(user_target):
#         print('User {} already logging'.format(user))
#     else:
#         with open(user_target, 'w') as f:
#             f.write('{:<22}{:<9}{:<20}{:<9}{:<25}{}'.format('DATETIME',
#                                                             'SERVER',
#                                                             'USER',
#                                                             'MELETI',
#                                                             'ACTION',
#                                                             'COMMENTS'))
#
#
# def updatetree():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     pointer = len(repo.split('\\'))
#
#     for dirpath, dirnames, filenames in os.walk(repo):
#         outpath = [meleti] + dirpath.split('\\')[pointer:]
#         _dir = cp(outpath)
#         if not os.path.exists(_dir):
#             os.makedirs(_dir)
#             print('{} - Created'.format(_dir))
#
#
# def update_ktima_info():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure',
#                    meleti, inputdata, docs_i, 'KT_Info.json'],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure',
#                    meleti, inputdata, docs_i, 'KT_Info.json'],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     target = cp([meleti, inputdata, docs_i, 'KT_Info.json'])
#
#     c_copy(repo, target)
#
#
# def update_temp_paths():
#     if ktl.get('company_name', 'NOT_FOUND') == c_NA:
#         repo = cp([mdev, 'Diafora', 'ktima', 'paths.json'],
#                   origin=ktl['temp'][user])
#     elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
#         repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'paths.json'],
#                   origin=ktl['temp'][user])
#     else:
#         print('"company_name" not defined in paths.json')
#         return
#
#     target = cp([users, user, 'paths.json'])
#
#     c_copy(repo, target)
#
#
# def get_binary():
#     update_from_server()


class Builder:
    def __init__(self, meleti, company=ktl.get('company_name', 'NOT_FOUND')):
        self.meleti = meleti
        self.company = company
        self.kt_info_path = cp([meleti, inputdata, docs_i, 'KT_Info.json'])

    def mel_change(self, new_meleti):
        self.meleti = new_meleti
        self.kt_info_path = cp([new_meleti, inputdata, docs_i, 'KT_Info.json'])

    def buildtree(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'],
                      origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        target = r"C:\{}".format(self.meleti)

        try:
            shutil.copytree(repo, target)
        except WindowsError:
            print('"{}" already exists or Source directory missing'.format(
                target))

    def update_folder_structure(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', self.meleti],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp(
                [temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure',
                 self.meleti],
                origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        pointer = len(repo.split('\\')) - 1

        for dirpath, dirnames, filenames in os.walk(repo):
            outpath = cp(dirpath.split('\\')[pointer:])
            if not os.path.exists(outpath):
                os.makedirs(outpath)

    def update_file_structure(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure', self.meleti],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp(
                [temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure',
                 self.meleti],
                origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        pointer = len(repo.split('\\')) - 1

        for dirpath, dirnames, filenames in os.walk(repo):
            for filename in filenames:
                inpath = os.path.join(dirpath, filename)
                outpath = cp(inpath.split('\\')[pointer:])
                c_copy(inpath, outpath)

    def make_empty_dirs(self):
        data = load_json(self.kt_info_path)

        mdb_out = cp([self.meleti, outputdata, paradosimdb_o])
        anakt_out = cp([self.meleti, outputdata, anakt])
        saromena_out = cp([self.meleti, outputdata, saromena])
        dirs = [anakt_out, saromena_out, mdb_out]

        for _dir in dirs:
            for ota in data['ota_list']:
                os.mkdir(os.path.join(_dir, ota))

    def start_logs(self):
        kt_target = cp([self.meleti, '!{}_log.txt'.format(self.meleti)])
        user_target = cp([users, user, 'KT_log.txt'])

        with open(kt_target, 'w') as f:
            f.write('{:<22}{:<9}{:<25}{}'.format('DATETIME', 'MELETI',
                                                 'ACTION', 'COMMENTS'))

        if os.path.exists(user_target):
            print('User {} already logging'.format(user))
        else:
            with open(user_target, 'w') as f:
                f.write('{:<22}{:<9}{:<20}{:<9}{:<25}{}'.format('DATETIME',
                                                                'SERVER',
                                                                'USER',
                                                                'MELETI',
                                                                'ACTION',
                                                                'COMMENTS'))

    def updatetree(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'Folder_Structure'],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'Folder_Structure'],
                      origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        pointer = len(repo.split('\\'))

        for dirpath, dirnames, filenames in os.walk(repo):
            outpath = [self.meleti] + dirpath.split('\\')[pointer:]
            _dir = cp(outpath)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
                print('{} - Created'.format(_dir))

    def update_ktima_info(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'File_Structure',
                       self.meleti, inputdata, docs_i, 'KT_Info.json'],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'File_Structure',
                       self.meleti, inputdata, docs_i, 'KT_Info.json'],
                      origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        target = cp([self.meleti, inputdata, docs_i, 'KT_Info.json'])

        c_copy(repo, target)

    def update_temp_paths(self):
        if self.company == c_NA:
            repo = cp([mdev, 'Diafora', 'ktima', 'paths.json'],
                      origin=ktl['temp'][user])
        elif self.company == c_2P:
            repo = cp([temp2kp, mdev, 'Diafora', 'ktima', 'paths.json'],
                      origin=ktl['temp'][user])
        else:
            print('"company_name" not defined in paths.json')
            return

        target = cp([users, user, 'paths.json'])

        c_copy(repo, target)

    @staticmethod
    def get_binary():
        update_from_server()


def user_in_build(_func):
    console = {'meleti': "(1) KT1-05\n"
                         "(2) KT2-11\n"
                         "(3) KT5-14\n"
                         "(4) KT5-16\n"
                         "(5) KT5-17\n"
                         "(6) KT5-22\n\n",
               'action': "(1) Auto Build\n"
                         "(2) Custom Build\n"
                         "(3) Update\n"
                         "(4) Change Meleti\n"
                         "(5) Get Binary\n\n",
               'custom_build': "(1) Build Tree\n"
                               "(2) Update Folder Structure\n"
                               "(3) Update File Structure\n"
                               "(4) Make Empty Directories\n"
                               "(5) Start Logging\n\n",
               'update': "(1) Update Tree\n"
                         "(2) Update Meleti Info\n"
                         "(3) Update User Paths\n\n"}

    approved = {'meleti': ['1', '2', '3', '4', '5', '6'],
                'action': ['1', '2', '3', '4', '5'],
                'custom_build': ['1', '2', '3', '4', '5'],
                'update': ['1', '2', '3']}

    user_action = raw_input(console[_func]).upper()
    while user_action not in approved[_func]:
        print('\n\n!! Action Not Recognised. Try Again !!\n\n')
        user_action = raw_input(console[_func]).upper()

    mel_mapper = {'1': 'KT1-05',
                  '2': 'KT2-11',
                  '3': 'KT5-14',
                  '4': 'KT5-16',
                  '5': 'KT5-17',
                  '6': 'KT5-22'}

    if _func == 'meleti':
        return mel_mapper[user_action]

    return user_action


if username == mdev.strip('! ') and password == build_pass:
    print('\nMeleti: \n')

    builder = Builder(user_in_build('meleti'))

    func_mapper = {'1': [builder.buildtree,
                         builder.update_folder_structure,
                         builder.update_file_structure,
                         builder.make_empty_dirs,
                         builder.start_logs],
                   '2': {'1': builder.buildtree,
                         '2': builder.update_folder_structure,
                         '3': builder.update_file_structure,
                         '4': builder.make_empty_dirs,
                         '5': builder.start_logs},
                   '3': {'1': builder.updatetree,
                         '2': builder.update_ktima_info,
                         '3': builder.update_temp_paths}}
    while True:
        print('\nGive a command:\n')
        action_type = user_in_build('action')

        print('##########################################################')

        if action_type == "1":
            for _func in func_mapper[action_type]:
                _func()
        elif action_type == "2":
            sub_action = user_in_build('custom_build')
            func_mapper[action_type][sub_action]()
        elif action_type == "3":
            sub_action = user_in_build('update')
            func_mapper[action_type][sub_action]()
        elif action_type == "4":
            builder.mel_change(user_in_build('meleti'))
        elif action_type == "5":
            builder.get_binary()

        print('##########################################################')
else:
    print("\nAccess denied\n")
