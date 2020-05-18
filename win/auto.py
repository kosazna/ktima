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

from ktima.status import *
from update import update_from_server
from collections import Counter


MELETI = str(sys.argv[1].split('\\')[1])

# PATHS FOR THE PROJECT INFO AND NAMING SCHEMA
kt_info_path = cp([MELETI, inputdata, docs_i, 'KT_Info.json'])
naming_path = cp([MELETI, inputdata, docs_i, 'KT_Naming_Schema.json'])

# DICTIONARIES OF THE PROJECT INFO AND NAMING SCHEMA
info_data = load_json(kt_info_path)
naming_data = load_json(naming_path)

# INSTANTIATING CLASSES
lui = LookUpInfo(info_data, naming_data)
paths = KTPaths(MELETI, lui.mel_type, lui.company_name)
status = KTStatus(MELETI, KTIMA_MODE, lui.ota_list)
log = KTLog(MELETI)


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

    console = {'action_type': "(1) Export Shapefiles\n"
                              "(2) Organize Files\n"
                              "(3) Create Metadata\n"
                              "(4) Export new ROADS to InputData\n"
                              "(5) Status\n"
                              "(6) Delete Data\n"
                              "(7) Count Paradosi Files\n"
                              "(8) Get scanned files\n"
                              "(9) Update\n\n",
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

    sl = ['']
    ol = ['']
    [sl.append(i) for i in lui.local_list]
    [ol.append(i) for i in lui.ota_list]

    approved = {'action_type': ['', '1', '2', '3', '4', '5',
                                '6', '7', '8', '9', '1LPAA4PS5'],
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
    Gets shapefiles from server or localdata and pastes them
    on localdata or paradosi data.

    :return: Nothing
    """

    if action_type == "1LPAA4PS5":
        get_folder = "L"
        export_folder = "P"
        shapes = ""
        ota_code = ""
    else:
        get_folder = validate_input('get_folder')
        export_folder = validate_input('export_folder')
        shapes = validate_input('shapes')
        ota_code = validate_input('ota_code')

    user_shapes = shapes.split("-")
    user_ota_list = ota_code.split("-")

    shape_list = []
    log_status = []

    if get_folder == "S" and export_folder == "L":
        shape_list = lui.server_list
        log_status.append('Server')
        log_status.append('LocalData')

        if not shapes:
            for shape in lui.status_list:
                status.update('SHAPE', shape, False)
            status.update('EXPORTED', "FBOUND", False)
        else:
            for shape in user_shapes:
                status.update('SHAPE', shape, False)
    elif get_folder == "L" and export_folder == "P":
        shape_list = lui.local_list
        log_status.append('LocalData')
        log_status.append('ParadosiData')

    print("Initializing...\n")

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

        for fpath, fname, bname, ext in list_dir(inpath, match=['.shp',
                                                                '.shx',
                                                                '.dbf']):
            if bname == shp:
                shutil.copyfile(fpath, os.path.join(outpath, fname))

    progress_counter = 0

    if get_pass():
        if ota_code == "" and shapes == "":
            for ota in lui.ota_list:
                progress_counter += 1
                for shape in shape_list:
                    export(shape, ota)
                progress(progress_counter, len(lui.ota_list))
        elif ota_code != "" and shapes != "":
            for ota in user_ota_list:
                progress_counter += 1
                for shape in user_shapes:
                    export(shape, ota)
                progress(progress_counter, len(user_ota_list))
        elif ota_code != "":
            for ota in user_ota_list:
                progress_counter += 1
                for shape in shape_list:
                    export(shape, ota)
                progress(progress_counter, len(user_ota_list))
        elif shapes != "":
            for ota in lui.ota_list:
                progress_counter += 1
                for shape in user_shapes:
                    export(shape, ota)
                progress(progress_counter, len(lui.ota_list))

        log('Export Shapefiles', log_status)
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
                base = paths.old_roads.split('\\')[1:]
                base += fpath.split('\\')[4:]
                outpath = cp(base)
                c_copy(fpath, outpath)

        status.update("SHAPE", "iROADS", False)
        log('New ROADS to InputData')

        print("DONE !")
    else:
        pass


def clear():
    """
    Deletes files that are not neccesary for the project.

    :return: Nothing
    """

    if action_type == "1LPAA4PS5":
        clear_folder = "P"
        clear_type = "S"
    else:
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
                        and clear_folder == "P" and bname in lui.no_del_list:
                    pass
                else:
                    try:
                        os.remove(fpath)
                    except OSError:
                        print("Error while deleting file")

            log('Clear directories', log_status)
            print("DONE !")
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

    if action_type == "1LPAA4PS5":
        date = mod_date
    else:
        date = (raw_input("\nDate (xx/xx/xxxx) : \n").upper())

    try:
        with open(paths.block_pnt_xml, 'r') as block_pnt_f:
            block_pnt_cont = str(block_pnt_f.read())
    except IOError:
        pass

    try:
        with open(paths.geo_xml, 'r') as geo_f:
            geo_cont = str(geo_f.read())
    except IOError:
        pass

    try:
        with open(paths.roads_xml, 'r') as roads_f:
            roads_cont = str(roads_f.read())
    except IOError:
        pass

    if lui.mel_type == 1:
        try:
            metas = {'BLOCK_PNT_METADATA': block_pnt_cont,
                     'ROADS_METADATA': roads_cont,
                     'GEO_METADATA': geo_cont}
        except UnboundLocalError:
            metas = {'ROADS_METADATA': roads_cont,
                     'GEO_METADATA': geo_cont}

    else:
        metas = {'ROADS_METADATA': roads_cont,
                 'GEO_METADATA': geo_cont}

    if get_pass():
        progress_counter = 0
        for ota in lui.ota_list:
            progress_counter += 1
            for meta in metas:
                path = paths.meta(ota, meta)

                temp = metas[meta][:82] + str(ota) + metas[meta][87:]
                content = temp[:118] + date + temp[128:]

                with open(path, 'w') as meta_f:
                    meta_f.write(content)

            progress(progress_counter, len(lui.ota_list))

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
                for ota in lui.ota_list:
                    if ota in bname[9:14]:
                        outpath = os.path.join(paths.anakt_out, ota, fname)
                        c_copy(fpath, outpath)
        elif org_folder == 'S':
            log_status.append('Saromena')
            for fpath, fname, bname, ext in list_dir(paths.saromena_in):
                for ota in lui.ota_list:
                    if bname[0] == 'D' and ota in bname[1:6]:
                        outpath = os.path.join(paths.saromena_out, ota, fname)
                        c_copy(fpath, outpath)
                    elif ota in bname[:5]:
                        outpath = os.path.join(paths.saromena_out, ota, fname)
                        c_copy(fpath, outpath)
        elif org_folder == 'M':
            log_status.append("MDB's")
            for fpath, fname, bname, ext in list_dir(paths.mdb_in):
                for ota in lui.ota_list:
                    if ota in bname and 'VSTEAS_REL' in bname:
                        outpath = os.path.join(paths.mdb_vsteas, ota,
                                               'SHAPE', 'VSTEAS_REL', fname)
                        c_copy(fpath, outpath)
                    elif ota in bname:
                        outpath = os.path.join(paths.mdb_out, ota, fname)
                        c_copy(fpath, outpath)

        log("Organize files", log_status)
    else:
        pass

    print("DONE !")


def counter():
    """
    Counts the shapefiles for each OTA.

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

    cnt_shapes = Counter(shapes.names)
    c_mdb = Counter([i[6:] if not i == 'POWNERS.mdb' else i for i in mdb.names])
    c_xml = Counter(xml.names)

    ota_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}
    missing_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}

    for i in shapes.paths:
        path_list = i.split('\\')
        if lui.mel_type == 1:
            ota_counter[path_list[6]].append(int(path_list[4]))
        else:
            ota_counter[path_list[5]].append(int(path_list[4]))

    otas = list(map(int, lui.ota_list))

    for i in otas:
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
            print('{:<18} - {}'.format(i, missing_counter[i]))

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

    for ota in lui.ota_list:
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
        progress(progress_counter, len(lui.ota_list))

    pm('\n\n{} scanned documents extracted from {}:/\n\n'.format(files,
                                                                 drive_letter))


if get_pass():
    while True:
        print('\nGive a command:\n')
        action_type = validate_input('action_type')

        if action_type == "1LPAA4PS5":
            mod_date = (raw_input("\nMetadata Date (xx/xx/xxxx) : \n").upper())

        print('###############################################################')

        if action_type == "1":
            shapefiles()
        elif action_type == "2":
            organize()
        elif action_type == "3":
            metadata()
        elif action_type == "4":
            roads()
        elif action_type == "5":
            status.show()
        elif action_type == "6":
            clear()
        elif action_type == "7":
            counter()
        elif action_type == "8":
            get_scanned()
        elif action_type == '9':
            extract('Temp', ktl['temp'][USER])
            update_from_server()
        elif action_type == "1LPAA4PS5":
            shapefiles()
            clear()
            metadata()
        else:
            extract('Local', ktl['temp'][USER])

        print('###############################################################')
else:
    print("\nAccess denied\n")
    action_type = "None"
