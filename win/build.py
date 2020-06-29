# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from update import *


class Builder:
    """
    Builder exists for creating project folder schema for each meleti
    in any pc.

    Attributes
    ----------
    - meleti: meleti of the project
    - company: company (server paths depend on that)
    - kt_info_path: all info regarding the project

    Methods
    -------
    - mel_change
    - buildtree
    - update_folder_structure
    - update_file_structure
    - make_empty_dirs
    - start_logs
    - updatetree
    - update_ktima_info
    - update_temp_paths
    - get_binary
    """

    def __init__(self, meleti, company=ktl.get('company_name', c_NA)):
        """
        :param meleti: str
            Meleti.
        :param company: str, optional
            Company (default: defined in paths.json).
        """

        self.meleti = meleti
        self.company = company
        self.kt_info_path = cp([meleti, inputdata, docs_i, json_info])

    def mel_change(self, new_meleti):
        """
        Changes meleti of the Builder object.

        :param new_meleti: str
            New meleti for the object.
        :return: Nothing
        """

        self.meleti = new_meleti
        self.kt_info_path = cp([new_meleti, inputdata, docs_i, json_info])

    def buildtree(self):
        """
        Builds the basic folder structure which is common for all projects.

        :return: Nothing
        """

        if self.company == c_NA:
            repo = cp(build_folder_NA, origin=ktl['temp'][USER])
        elif self.company == c_2P:
            repo = cp(build_folder_2P, origin=ktl['temp'][USER])
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
        """
        Updates the folder structure depending on the project.

        :return: Nothing
        """

        if self.company == c_NA:
            repo = cp(add_mel_inpath(build_file_NA, self.meleti),
                      origin=ktl['temp'][USER])
        elif self.company == c_2P:
            repo = cp(add_mel_inpath(build_file_2P, self.meleti),
                      origin=ktl['temp'][USER])
        else:
            print('"company_name" not defined in paths.json')
            return

        pointer = len(repo.split('\\')) - 1

        for dirpath, dirnames, filenames in os.walk(repo):
            outpath = cp(dirpath.split('\\')[pointer:])
            if not os.path.exists(outpath):
                os.makedirs(outpath)

    def update_file_structure(self):
        """
        Update the files of each project depending on the project.

        :return: Nothing
        """
        if self.company == c_NA:
            repo = cp(add_mel_inpath(build_file_NA, self.meleti),
                      origin=ktl['temp'][USER])
        elif self.company == c_2P:
            repo = cp(add_mel_inpath(build_file_2P, self.meleti),
                      origin=ktl['temp'][USER])
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
        """
        Makes empty directories for the otas of each project.

        :return: Nothing
        """

        data = load_json(self.kt_info_path)

        mdb_out = cp([self.meleti, outputdata, paradosimdb_o])
        anakt_out = cp([self.meleti, outputdata, anakt])
        saromena_out = cp([self.meleti, outputdata, saromena])
        dirs = [anakt_out, saromena_out, mdb_out]

        for _dir in dirs:
            for ota in data['ota_list']:
                os.mkdir(os.path.join(_dir, ota))

    def start_logs(self):
        """
        Starts logs for each project and each USER.

        :return: Nothing
        """

        kt_target = cp([self.meleti, '!{}_log.txt'.format(self.meleti)])
        user_target = cp([users, USER, txt_log])

        with open(kt_target, 'w') as f:
            f.write('{:<22}{:<9}{:<25}{}'.format('DATETIME', 'MELETI',
                                                 'ACTION', 'COMMENTS'))

        if os.path.exists(user_target):
            print('User {} already logging'.format(USER))
        else:
            with open(user_target, 'w') as f:
                f.write('{:<22}{:<9}{:<20}{:<9}{:<25}{}'.format('DATETIME',
                                                                'SERVER',
                                                                'USER',
                                                                'MELETI',
                                                                'ACTION',
                                                                'COMMENTS'))

    def updatetree(self):
        """
        Update basic folder schema of all projects.

        :return: Nothing
        """

        if self.company == c_NA:
            repo = cp(build_folder_NA, origin=ktl['temp'][USER])
        elif self.company == c_2P:
            repo = cp(build_folder_2P, origin=ktl['temp'][USER])
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
        """
        Updates KT_Info.json file for each project.

        :return: Nothing
        """
        if self.company == c_NA:
            components = add_mel_inpath(build_file_NA, self.meleti)
            components.extend([inputdata, docs_i, json_info])
            repo = cp(components, origin=ktl['temp'][USER])
        elif self.company == c_2P:
            components = add_mel_inpath(build_file_2P, self.meleti)
            components.extend([inputdata, docs_i, json_info])
            repo = cp(components, origin=ktl['temp'][USER])
        else:
            print('"company_name" not defined in paths.json')
            return

        target = cp([self.meleti, inputdata, docs_i, json_info])

        c_copy(repo, target)

    def update_temp_paths(self):
        """
        Updates paths.json file for the USER.

        :return: Nothing
        """

        if self.company == c_NA:
            repo = cp(build_json_path_NA, origin=ktl['temp'][USER])
        elif self.company == c_2P:
            repo = cp(build_json_path_2P, origin=ktl['temp'][USER])
        else:
            print('"company_name" not defined in paths.json')
            return

        target = cp([users, USER, json_paths])

        c_copy(repo, target)

    @staticmethod
    def get_binary():
        """
        Gets the '.pyc' files from the server.

        :return: Nothing
        """

        update_from_server()


def _validate_input(_func):
    """
    Custom function for USER input.
    Given a _func a custom message will be displayed for the USER.

    After USER selects one action function checks against all possible
    compinations. If USER input is in the approved actions the execution
    proceeds. While his registered action is not within the approved list USER
    is prompted to give an action again.

    :param _func: str
        Function which is called. This function name should me in both the
        console dict and the approved dict else KeyError is raised.
    :return: str
        User action after validation
    """
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


if __name__ == '__main__':
    username = raw_input("\n\nUsername:\n")
    password = getpass.getpass("\nPassword:\n")
    if username == mdev.strip('! ') and password == build_pass:
        print('\nMeleti: \n')

        builder = Builder(_validate_input('meleti'))

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
            action_type = _validate_input('action')

            print('#' * 60)

            if action_type == "1":
                for _func in func_mapper[action_type]:
                    _func()
            elif action_type == "2":
                sub_action = _validate_input('custom_build')
                func_mapper[action_type][sub_action]()
            elif action_type == "3":
                sub_action = _validate_input('update')
                func_mapper[action_type][sub_action]()
            elif action_type == "4":
                builder.mel_change(_validate_input('meleti'))
            elif action_type == "5":
                builder.get_binary()

            print('#' * 60)
    else:
        print("\nAccess denied\n")
