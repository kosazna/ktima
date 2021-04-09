# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This modules has all the neccesary functions for all tasks
# on the windows side of the project

import re
from status import *
from update import update_from_server
from build import Builder
from collections import Counter


MELETI = str(sys.argv[1].split('\\')[1])

# PATHS FOR THE PROJECT INFO AND NAMING SCHEMA
kt_info_path = cp([MELETI, inputdata, docs_i, 'KT_Info.json'])

# DICTIONARIES OF THE PROJECT INFO AND NAMING SCHEMA
info_data = load_json(kt_info_path)

# INSTANTIATING CLASSES
info = KTInfo(info_data)
paths = KTPaths(MELETI, info.mel_type, info.company_name)
status = KTStatus(MELETI, KTIMA_MODE, info.ota_list)
log = KTLog(MELETI)


def fmt2list(formatter, full_list):
    """
    Tranforms user input to a list of elements

    :param formatter: str
        User input format.
    :param full_list: list
        list that will be formatted accordingly
    :return: list
        Final list of elements
    """

    if not formatter:
        final_list = full_list
    elif formatter == "~":
        final_list = None
    elif formatter.startswith('~'):
        no_need = formatter.split('-')[1:]
        final_list = [_i for _i in full_list if _i not in no_need]
    elif formatter.startswith('info.'):
        final_list = eval(formatter)
    else:
        final_list = formatter.split('-')

    return sorted(final_list)


def fmt2path(formatter):
    """
    Transforms user input to a path

    :param formatter: str
        User input format.
    :return: str
        Path.
    """
    if formatter.startswith('paths.'):
        folder_base = eval(formatter)
    else:
        folder_base = formatter

    return folder_base


def validate_input(_func):
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

    console = {'action_type': " (1) Export Shapefiles\n"
                              " (2) Organize Files\n"
                              " (3) Create Metadata\n"
                              " (4) Create Empty Shapefiles\n"
                              " (5) Status\n"
                              " (6) Delete Data\n"
                              " (7) Count Files\n"
                              " (8) Get scanned files\n"
                              " (9) Create Directories\n"
                              "(10) Update ktima\n\n",
               'get_folder': "\nGet from : (S)erver  /  (L)ocal \n\n",
               'export_folder': "\nExport to : (L)ocal  /  (P)aradosi\n\n",
               'shapes': "\nSHAPEFILE: (Enter for ALL, or split with '-')\n\n",
               'ota_code': "\nOTA: (Enter for ALL, or split with '-')\n\n",
               'clear_folder': "\nDelete from :\n\n"
                               "(I)nputData\n"
                               "(L)ocal\n"
                               "(P)aradosi\n"
                               "(M)DB's\n\n"
                               "(A)naktiseis\n"
                               "(S)aromena\n\n",
               'clear_type': "\nDelete method : (A)ll  /  (S)tandard\n\n",
               'org_folder': "\nFiles:(A)naktiseis / (S)aromena / (M)DB's\n\n",
               'get_scanned': "\nDrive letter : [Enter for default ('W')]\n\n",
               'path_to_count': "\nCount files from:\n\n"
                                "(L)ocalData\n"
                                "(P)aradosiData\n\n"}

    sl = ['', '~']
    ol = ['', '~']
    [sl.append(i) for i in info.all_ktima]
    [ol.append(i) for i in info.ota_list]

    approved = {'action_type': ['', '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '10'],
                'get_folder': ['S', 'L'],
                'export_folder': ['L', 'P'],
                'shapes': sl,
                'ota_code': ol,
                'clear_folder': ['I', 'L', 'P', 'A', 'S', 'M'],
                'clear_type': ['A', 'S'],
                'org_folder': ['A', 'S', 'M'],
                'get_scanned': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'path_to_count': ['L', 'P']}

    if _func == 'shapes' or _func == 'ota_code':
        user_action = raw_input(console[_func]).upper()
        _action = user_action.split('-')
        count = 0

        if len(_action) != 1:
            for i in _action:
                if i in approved[_func]:
                    count += 1

            while count != len(_action):
                print('\n\n!! Action Not Recognised. Try Again !!\n\n')
                count = 0
                user_action = raw_input(console[_func]).upper()
                _action = user_action.split('-')
                for i in _action:
                    if i in approved[_func]:
                        count += 1
        else:
            while user_action not in approved[_func]:
                print('\n\n!! Action Not Recognised. Try Again !!\n\n')
                user_action = raw_input(console[_func]).upper()
    else:
        user_action = raw_input(console[_func]).upper()
        while user_action not in approved[_func]:
            print('\n\n!! Action Not Recognised. Try Again !!\n\n')
            user_action = raw_input(console[_func]).upper()

    return user_action


def shapefiles():
    """
    Gets shp_list from server or localdata and pastes them
    on localdata or paradosi data.

    :return: Nothing
    """

    def export(shp, ota_num):
        inpath = ""
        outpath = ""

        if get_folder == "S" and export_folder == "L":
            inpath = paths.server_folder(ota_num, shp)
            outpath = paths.ktima_folder(ota_num, shp)
        elif get_folder == "L" and export_folder == "P":
            inpath = paths.ktima_folder(ota_num, shp)
            outpath = paths.ktima_folder(ota_num, shp,
                                         spatial_folder=paradosidata_o)

        for fpath, fname, bname, ext in list_dir(inpath, match='.shp'):
            if bname == shp:
                copy_shp(inpath, outpath, bname)

    get_folder = validate_input('get_folder')
    export_folder = validate_input('export_folder')
    shapes = validate_input('shapes')
    ota_code = validate_input('ota_code')

    user_shapes = fmt2list(shapes, info.all_ktima)
    user_ota_list = fmt2list(ota_code, info.ota_list)

    log_status = []

    if get_folder == "S" and export_folder == "L":
        log_status.append('Server')
        log_status.append('LocalData')

        if not shapes:
            for shape in info.status_list:
                status.update('SHAPE', shape, False)
            status.update('EXPORTED', "FBOUND", False)
        else:
            for shape in user_shapes:
                status.update('SHAPE', shape, False)
    elif get_folder == "L" and export_folder == "P":
        log_status.append('LocalData')
        log_status.append('ParadosiData')

    print("Initializing...\n")

    progress_counter_ota = 0

    if get_pass():
        for ota in user_ota_list:
            progress_counter_ota += 1
            for shape in user_shapes:
                export(shape, ota)
            progress(progress_counter_ota, len(user_ota_list))

        log('Export Shapefiles', log_list=log_status)
    else:
        pass


def roads():
    """
    Exports roads from LocalData to InputData.

    :return: Nothing
    """

    if get_pass():
        for fpath, fname, bname, ext in list_dir(paths.new_roads,
                                                 match=['.shp',
                                                        '.shx',
                                                        '.dbf']):
            if bname == 'ROADS':
                _base = paths.old_roads.split('\\')[1:]
                _base += fpath.split('\\')[4:]
                outpath = cp(_base)
                c_copy(fpath, outpath)

        status.update("SHAPE", "iROADS", False)
        log('New ROADS to InputData')

        print("\nDONE !\n")
    else:
        pass


def clear():
    """
    Deletes files that are not neccesary for the project.

    :return: Nothing
    """

    clear_folder = validate_input('clear_folder')
    if clear_folder == 'L' or clear_folder == 'P' or clear_folder == 'I':
        clear_type = validate_input('clear_type')
    else:
        clear_type = 'None'

    log_status = []
    clearlocalpath = ""

    if clear_folder == "L":
        clearlocalpath = paths.localdata
        log_status.append('LocalData')
    elif clear_folder == "P":
        clearlocalpath = paths.paradosidata
        log_status.append('ParadosiData')
    elif clear_folder == "I":
        clearlocalpath = paths.old_roads
        log_status.append('InputRoads')
    elif clear_folder == 'A':
        clearlocalpath = paths.anakt_out
    elif clear_folder == 'S':
        clearlocalpath = paths.saromena_out
    elif clear_folder == 'M':
        clearlocalpath = paths.mdb_out

    del_list = []

    if clear_type == "A":
        del_list = ['.sbn', '.sbx', '.shp.xml', '.prj',
                    '.idx', '.cpg', '.shp', '.shx', '.dbf', '.mdb', '.lock']
        log_status.append('all')
    elif clear_type == "S":
        del_list = ['.sbn', '.sbx', '.shp.xml', '.prj', '.idx', '.cpg', '.lock']
        log_status.append('standard')

    if get_pass():

        if clear_folder == 'L' or clear_folder == 'P' or clear_folder == 'I':
            for fpath, fname, bname, ext in list_dir(clearlocalpath,
                                                     match=del_list):
                if clear_type == "A" \
                        and clear_folder == "P" and bname in info.no_del_list:
                    pass
                else:
                    try:
                        os.remove(fpath)
                    except OSError:
                        print("Error while deleting file")

            log('Clear directories', log_list=log_status)
            print("\nDONE !\n")
        else:
            for fpath, fname, bname, ext in list_dir(clearlocalpath):
                try:
                    os.remove(fpath)
                except OSError:
                    print("Error while deleting file")
    else:
        pass


def metadata():
    """
    Creates metadata given a date.

    :return: Nothing
    """

    def create_new_content(data, ota_value, date_value):
        ota_end = re.search(r'<CODE_OKXE>(\d*)', data).end()
        date_end = re.search(r'<DeliveryDate>(\d*/\d*/\d*)', data).end()

        ota_start = ota_end - 5
        date_start = date_end - 10

        temp = data[:ota_start] + str(ota_value) + data[ota_end:]
        data = temp[:date_start] + date_value + temp[date_end:]

        return data

    date = (raw_input("\nDate (xx/xx/xxxx) : \n").upper())

    try:
        with open(paths.block_pnt_xml, 'r') as block_pnt_f:
            block_pnt_cont = str(block_pnt_f.read())
            has_block = True
    except IOError:
        block_pnt_cont = ''
        has_block = False

    try:
        with open(paths.geo_xml, 'r') as geo_f:
            geo_cont = str(geo_f.read())
            has_geo = True
    except IOError:
        geo_cont = ''
        has_geo = False

    try:
        with open(paths.roads_xml, 'r') as roads_f:
            roads_cont = str(roads_f.read())
            has_road = True
    except IOError:
        roads_cont = ''
        has_road = False

    metas = {'BLOCK_PNT_METADATA': {'exists': has_block,
                                    'data': block_pnt_cont},
             'ROADS_METADATA': {'exists': has_road,
                                'data': roads_cont},
             'GEO_METADATA': {'exists': has_geo,
                              'data': geo_cont}}

    if get_pass():
        progress_counter = 0
        for ota in info.ota_list:
            progress_counter += 1
            for meta in metas:
                path = paths.meta(ota, meta)

                if metas[meta]['exists']:
                    to_write = metas[meta]['data']
                    with open(path, 'w') as meta_f:
                        meta_f.write(create_new_content(to_write, ota, date))

            progress(progress_counter, len(info.ota_list))

        log("Metadata")

        print('\nDONE !\n')
    else:
        pass


def organize():
    """
    Organizes the files provided form the InputData to the OutputData.

    :return: Nothing
    """

    org_folder = validate_input('org_folder')
    log_status = []

    if get_pass():
        if org_folder == 'A':
            log_status.append('Anaktiseis')
            for fpath, fname, bname, ext in list_dir(paths.anakt_in):
                for ota in info.ota_list:
                    if ota in bname[9:14]:
                        outpath = os.path.join(paths.anakt_out, ota, fname)
                        c_copy(fpath, outpath)
        elif org_folder == 'S':
            log_status.append('Saromena')
            for fpath, fname, bname, ext in list_dir(paths.saromena_in):
                for ota in info.ota_list:
                    if bname[0] == 'D' and ota in bname[1:6]:
                        outpath = os.path.join(paths.saromena_out, ota, fname)
                        c_copy(fpath, outpath)
                    elif ota in bname[:5]:
                        outpath = os.path.join(paths.saromena_out, ota, fname)
                        c_copy(fpath, outpath)
        elif org_folder == 'M':
            log_status.append("MDB's")
            for fpath, fname, bname, ext in list_dir(paths.mdb_in):
                for ota in info.ota_list:
                    if ota in bname and 'VSTEAS_REL' in bname:
                        outpath = os.path.join(paths.mdb_vsteas, ota,
                                               'SHAPE', 'VSTEAS_REL', fname[6:])
                        c_copy(fpath, outpath)
                    elif ota in bname:
                        outpath = os.path.join(paths.mdb_out, ota, fname)
                        c_copy(fpath, outpath)

        log("Organize files", log_list=log_status)
    else:
        pass

    print("\nDONE !\n")


def counter():
    """
    Counts the shp_list for each OTA.

    :return: Nothing
    """

    path = validate_input('path_to_count')

    if path == 'L':
        path_to_count = paths.localdata
    else:
        path_to_count = paths.paradosidata

    shapes = Files(path_to_count)
    mdb = Files(path_to_count)
    xml = Files(path_to_count)

    shapes.explore(match='.shp')
    mdb.explore(match='.mdb')
    xml.explore(match='.xml')

    cnt_shapes = Counter(map(str.upper, shapes.names))
    c_mdb = Counter(mdb.names)
    c_xml = Counter(xml.names)

    ota_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}
    missing_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}

    for i in shapes.paths:
        path_list = i.split('\\')
        if info.mel_type == 1:
            ota_counter[path_list[6]].append(str(path_list[4]))
        else:
            ota_counter[path_list[5]].append(str(path_list[4]))

    for i in info.ota_list:
        for shp in ota_counter:
            if i not in ota_counter[shp]:
                missing_counter[shp].append(i)

    print("\nSHAPEFILES")
    print("------------------")

    for i in sorted(cnt_shapes):
        name, ext = os.path.splitext(i)
        print('{:<18} - {}'.format(name, cnt_shapes[i]))

    print("\nMBD's")
    print('------------------')

    for i in sorted(c_mdb):
        name, ext = os.path.splitext(i)
        print('{:<18} - {}'.format(name, c_mdb[i]))

    print("\nMETADATA")
    print('------------------')

    for i in sorted(c_xml):
        name, ext = os.path.splitext(i)
        print('{:<18} - {}'.format(name, c_xml[i]))

    print('')

    print("\nMISSING")
    print("------------------")

    for i in sorted(missing_counter, key=lambda x: len(missing_counter[x])):
        if missing_counter[i]:
            print('{:<18} - {}'.format(i, '-'.join(missing_counter[i])))

    log_counter = ' - '.join(
        str(sorted(list(cnt_shapes.items()), key=lambda x: x[0])).strip(
            '[]').split("', '"))

    log('Count Shapefiles', log_list=log_counter)
    print('')


def get_scanned():
    """
    Creates a txt file with the fullpath of every file in the scanned folder.

    :return: Nothing
    """

    drive_letter = validate_input('get_scanned')

    if drive_letter == '':
        drive_letter = 'W'

    progress_counter = 0
    files = 0

    for ota in info.ota_list:
        with open(cp([MELETI, outputdata,
                      'Scanned_List',
                      '{}_Scanned_Files'.format(ota)]), 'w') as f:

            progress_counter += 1
            repo = cp([ota], origin=drive_letter)
            for dirpath, dirnames, fnames in os.walk(repo):
                for fname in fnames:
                    if fname.endswith('.tif') or fname.endswith('.TIF'):
                        files += 1
                        f.write('{}\n'.format(os.path.join(dirpath, fname)))
        progress(progress_counter, len(info.ota_list))

    print('\n\n{} scanned documents extracted from {}:/\n\n'.format(
        files,
        drive_letter))


def create_empty_dirs(base_folder, how, ota_list=None, shp_list=None):
    """
    Creates empty directories according to a format provided by the user.

    :param base_folder: str
        Path to where the folders must be created
    :param how: str
        Formatter
    :param ota_list: list
        List with otas
    :param shp_list: list
        List of shapefiles
    :return: Nothing
    """

    if '<ota>' in how or '<shapefile>' in how:
        if '<ota>' in how and ota_list is None:
            print('<ota> exists without ota_list')
            return
        if '<shapefile>' in how and shp_list is None:
            print('<shapefile> exists without shapefile list')
            return
    else:
        print('At least one of <ota> or <shapefile> must be provided')
        return

    if ota_list is not None and shp_list is not None:
        for ota in ota_list:
            for shp in shp_list:
                plus = how.replace('<ota>', ota).replace('<shapefile>', shp)
                try:
                    os.makedirs(os.path.join(base_folder, plus))
                except WindowsError:
                    pass
    elif ota_list is not None and shp_list is None:
        for ota in ota_list:
            plus = how.replace('<ota>', ota)
            try:
                os.makedirs(os.path.join(base_folder, plus))
            except WindowsError:
                pass
    elif ota_list is None and shp_list is not None:
        for shp in shp_list:
            plus = how.replace('<shapefile>', shp)
            try:
                os.makedirs(os.path.join(base_folder, plus))
            except WindowsError:
                pass


def fill_empty_shp(ota_list=None, shp_list=None):
    """
    Fills folders with empty shapefiles.

    :param ota_list: list
        List with otas
    :param shp_list: list
        List of shapefiles
    :return: Nothing
    """

    for ota in ota_list:
        for shp in shp_list:
            check_path = paths.ktima(ota, shp, ext=True,
                                     spatial_folder=paradosidata_o)
            if not os.path.exists(check_path):
                inpath = os.path.join(paths.empty_shps, shp)
                outpath = paths.ktima_folder(ota, shp,
                                             spatial_folder=paradosidata_o)
                copy_shp(inpath, outpath, shp)

    log('Empty Shapefiles', log_list=shp_list)

    print('DONE !')


def update_jsons():
    constructor = Builder(MELETI, info.company_name)
    constructor.update_ktima_info()
    constructor.update_temp_paths()

    log('Docs update')


def formal_copy(path):
    for fpath, fname, bname, ext in list_dir(path,
                                             match=['.shp', '.shx', '.dbf']):
        ota = bname[-5:]
        name = bname[:-6]

        out = os.path.join(paths.ktima_folder(ota, name),
                           '{}{}'.format(name, ext))
        c_copy(fpath, out)


if __name__ == '__main__':
    if get_pass():
        while True:
            check_ktima_version()
            print('\nGive a command:\n')
            action_type = validate_input('action_type')

            print('\n')
            print('=#' * 40)

            if action_type == "1":
                shapefiles()
            elif action_type == "2":
                organize()
            elif action_type == "3":
                metadata()
            elif action_type == "4":
                otas_to_create = validate_input('ota_code')
                shapes_to_create = validate_input('shapes')

                empty = Files(paths.empty_shps)
                empty.explore()
                empty_shp = list(set(empty.names))

                new_otas = fmt2list(otas_to_create, info.ota_list)
                new_shapes = fmt2list(shapes_to_create, empty_shp)

                fill_empty_shp(new_otas, new_shapes)
            elif action_type == "5":
                status.show()
            elif action_type == "6":
                clear()
            elif action_type == "7":
                counter()
            elif action_type == "8":
                get_scanned()
            elif action_type == "9":
                base = raw_input('Give folder path to create directories\n')
                method = raw_input('Give method of creation\n')
                otas_to_create = validate_input('ota_code')
                print('Available Shapefiles:\n')
                print(strize(info.all_ktima))
                shapes_to_create = validate_input('shapes')

                folder = fmt2path(base)
                new_otas = fmt2list(otas_to_create, info.ota_list)
                new_shapes = fmt2list(shapes_to_create, info.all_ktima)

                create_empty_dirs(folder, method, new_otas, new_shapes)
            elif action_type == "10":
                extract('Temp', ktl['temp'][USER])
                update_jsons()
                update_from_server()
                log('Update', log_list=str(local_ktima_version))
            else:
                extract('Local', ktl['temp'][USER])

            print('\n')
            print('=#' * 40)
    else:
        print("\nAccess denied\n")
        action_type = "None"
