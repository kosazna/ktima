# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.status import *
from update import update_from_server
from collections import Counter
import fnmatch

arcpy.env.overwriteOutput = True

meleti = str(sys.argv[1].split('\\')[1])
data = load_json(cp([meleti, inputdata, docs_i, 'KT_Info.json']))

kt = NamesAndLists(data)
paths = Paths(meleti, kt.mel_type, kt.company_name)
status = Status(meleti)
log = Log(meleti)


def user_in(_func):
    console = {'action_type': "(1) Export Shapefiles\n"
                              "(2) Organize Files\n"
                              "(3) Create Metadata\n"
                              "(4) Export new ROADS to InputData\n"
                              "(5) Status\n"
                              "(6) Delete Data\n"
                              "(7) Count Paradosi Files\n"
                              "(8) Get scanned files\n"
                              "(9) Update\n\n",
               'get_folder': "\nGet from : (S)erver  or  (L)ocal \n\n",
               'export_folder': "\nExport to : (L)ocal  or  (P)aradosi\n\n",
               'shapes': "\nSHAPEFILE to export: (Enter for ALL, or split with '-')\n\n",
               'ota_code': "\nOTA to export from: (Enter for ALL, or split with '-')\n\n",
               'clear_folder': "\nDelete from :\n\n"
                               "(I)nputData\n"
                               "(L)ocal\n"
                               "(P)aradosi\n"
                               "(M)DB's\n\n"
                               "(A)naktiseis\n"
                               "(S)aromena\n\n",
               'clear_type': "\nDelete method : (A)ll  or  (S)tandard\n\n",
               'org_folder': "\nFiles : (A)naktiseis  or  (S)aromena  or  (M)DB's\n\n",
               'get_scanned': "\nGive drive letter : [Enter for default ('W')]\n\n"}

    sl = ['']
    ol = ['']
    [sl.append(i) for i in kt.local_list]
    [ol.append(i) for i in kt.ota_list]

    approved = {'action_type': ['', '1', '2', '3', '4', '5', '6', '7', '8', '9', '1LPAA4PS5'],
                'get_folder': ['S', 'L'],
                'export_folder': ['L', 'P'],
                'shapes': sl,
                'ota_code': ol,
                'clear_folder': ['I', 'L', 'P', 'A', 'S', 'M'],
                'clear_type': ['A', 'S'],
                'org_folder': ['A', 'S', 'M'],
                'get_scanned': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

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


if get_pass():
    action_type = user_in('action_type')

    if action_type == "1LPAA4PS5":
        mod_date = (raw_input("\nDate for Metadata (xx/xx/xxxx) : \n").upper())
else:
    print("\nAccess denied\n")
    action_type = "None"


def shapefiles():
    if action_type == "1LPAA4PS5":
        get_folder = "L"
        export_folder = "P"
        shapes = ""
        ota_code = ""
    else:
        get_folder = user_in('get_folder')
        export_folder = user_in('export_folder')
        shapes = user_in('shapes')
        ota_code = user_in('ota_code')

    user_shapes = shapes.split("-")
    user_ota_list = ota_code.split("-")

    shape_list = []
    missing_list = []
    log_status = []

    if get_folder == "S" and export_folder == "L":
        shape_list = kt.server_list
        log_status.append('Server')
        log_status.append('LocalData')

        if not shapes:
            for shape in kt.status_list:
                status.update('SHAPE', shape, False)
            status.update('EXPORTED', "FBOUND", False)
        else:
            for shape in user_shapes:
                status.update('SHAPE', shape, False)
    elif get_folder == "L" and export_folder == "P":
        shape_list = kt.local_list
        log_status.append('LocalData')
        log_status.append('ParadosiData')

    print("Initializing...\n")

    def export(e_shape, e_ota):
        inpath = ""
        outpath = ""

        if get_folder == "S" and export_folder == "L":
            inpath = paths.server(e_ota, e_shape)
            outpath = paths.ktima(e_ota, e_shape, ext=True)
        elif get_folder == "L" and export_folder == "P":
            inpath = paths.ktima(e_ota, e_shape, ext=True)
            outpath = paths.ktima(e_ota, e_shape, ext=True, spatial_folder=paradosidata_o)
        else:
            print("Wrong letter combination")

        if arcpy.Exists(inpath):
            arcpy.CopyFeatures_management(inpath, outpath)
        else:
            missing_name = e_shape + "_" + e_ota
            missing_list.append(missing_name)

        return

    progress_counter = 0

    if get_pass():
        if ota_code == "" and shapes == "":
            for ota in kt.ota_list:
                progress_counter += 1
                for shape in shape_list:
                    export(shape, ota)
                progress(progress_counter, len(kt.ota_list))
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
            for ota in kt.ota_list:
                progress_counter += 1
                for shape in user_shapes:
                    export(shape, ota)
                progress(progress_counter, len(kt.ota_list))

        missing_list.sort()

        log('Export Shapefiles', log_status)

        print("\nMissing files : \n")

        if not missing_list:
            print("NONE\n\n")
        else:
            for i in missing_list:
                print(i)
    else:
        pass


def roads():
    for fullpath, filename, basename, ext in list_dir(paths.new_roads, match=['.shp', '.shx', '.dbf']):
        if basename == 'ROADS':
            outpath = os.path.join(paths.old_roads, fullpath.split('\\')[4:])
            c_copy(fullpath, outpath)
        # copy_list = ['*shp', '*shx', '*dbf']
        #
        # if get_pass():
        #     def copy_files(x):
        #         for fullpath, basename, ext in list_dir(paths.new_roads, match=['.shp', '.shx', '.dbf']):
        #             if basename == 'ROADS':
        #                 outpath = os.path.join(paths.old_roads, fullpath.split('\\')[4:])
        #                 c_copy(fullpath, outpath)
        #
        #         progress_counter = 0
        #         for i in copy_list:
        #             for rootDir, subdirs, filenames in os.walk(paths.new_roads):
        #                 for filename in fnmatch.filter(filenames, i):
        #                     if "ROADS" in filename:
        #                         progress_counter += 1
        #                         inpath = os.path.join(rootDir, filename)
        #                         outpath = os.path.join(paths.old_roads, rootDir[-x:], filename)
        #                         shutil.copyfile(inpath, outpath)
        #                         progress(progress_counter, 42)
        #
        #     if kt.mel_type == 1:
        #         copy_files(17)
        #     else:
        #         copy_files(11)

        status.update("SHAPE", "iROADS", False)
        log('New ROADS to InputRoads folder')

        print("DONE !")
    else:
        pass


def clear():
    if action_type == "1LPAA4PS5":
        clear_folder = "P"
        clear_type = "S"
    else:
        clear_folder = user_in('clear_folder')
        if clear_folder == 'L' or clear_folder == 'P' or clear_folder == 'I':
            clear_type = user_in('clear_type')
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
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*shp', '*shx', '*dbf', '*mdb', '*lock']
        log_status.append('all')
    elif clear_type == "S":
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*lock']
        log_status.append('standard')

    if get_pass():
        progress_counter = 0
        if clear_folder == 'L' or clear_folder == 'P' or clear_folder == 'I':
            for i in del_list:
                progress_counter += 1
                for rootDir, subdirs, filenames in os.walk(clearlocalpath):
                    for filename in fnmatch.filter(filenames, i):
                        if clear_type == "A" and clear_folder == "P" and os.path.splitext(filename)[0] in kt.no_del_list:
                            pass
                        else:
                            try:
                                os.remove(os.path.join(rootDir, filename))
                            except OSError:
                                print("Error while deleting file")
                progress(progress_counter, len(del_list))

            log('Clear directories', log_status)

            print("DONE !")
        else:
            for rootDir, subdirs, filenames in os.walk(clearlocalpath):
                for filename in filenames:
                    try:
                        os.remove(os.path.join(rootDir, filename))
                    except OSError:
                        print("Error while deleting file")
    else:
        pass


def metadata():
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

    if kt.mel_type == 1:
        metas = {'BLOCK_PNT_METADATA': block_pnt_cont,
                 'ROADS_METADATA': roads_cont,
                 'GEO_METADATA': geo_cont}
    else:
        metas = {'ROADS_METADATA': roads_cont,
                 'GEO_METADATA': geo_cont}

    if get_pass():
        progress_counter = 0
        for ota in kt.ota_list:
            progress_counter += 1
            for meta in metas:
                path = paths.meta(ota, meta)

                temp = metas[meta][:82] + str(ota) + metas[meta][87:]
                content = temp[:118] + date + temp[128:]

                with open(path, 'w') as meta_f:
                    meta_f.write(content)

            progress(progress_counter, len(kt.ota_list))

        log("Metadata")

        print('\nDONE !\n')
    else:
        pass


def organize():
    org_folder = user_in('org_folder')
    log_status = []

    if get_pass():
        if org_folder == 'A':
            log_status.append('Anaktiseis')
            for fullpath, filename, basename, ext in list_dir(paths.anakt_in):
                for ota in kt.ota_list:
                    if ota in basename[9:14]:
                        outpath = os.path.join(paths.anakt_out, ota, filename)
                        c_copy(fullpath, outpath)
        elif org_folder == 'S':
            log_status.append('Saromena')
            for fullpath, filename, basename, ext in list_dir(paths.saromena_in):
                for ota in kt.ota_list:
                    if basename[0] == 'D' and ota in basename[1:6]:
                        outpath = os.path.join(paths.saromena_out, ota, filename)
                        c_copy(fullpath, outpath)
                    elif ota in basename[:5]:
                        outpath = os.path.join(paths.saromena_out, ota, filename)
                        c_copy(fullpath, outpath)
        elif org_folder == 'M':
            log_status.append("MDB's")
            for fullpath, filename, basename, ext in list_dir(paths.mdb_in):
                for ota in kt.ota_list:
                    if ota in basename and 'VSTEAS_REL' in basename:
                        outpath = os.path.join(paths.mdb_vsteas, ota, 'SHAPE', 'VSTEAS_REL', filename)
                        c_copy(fullpath, outpath)
                    elif ota in basename:
                        outpath = os.path.join(paths.mdb_out, ota, filename)
                        c_copy(fullpath, outpath)

        log("Organize files", log_status)
    else:
        pass

    print("DONE !")


def counter(path_to_count=paths.paradosidata):
    shapes = Files(path_to_count)
    mdb = Files(path_to_count)
    xml = Files(path_to_count)

    shapes.list_files(match='.shp')
    mdb.list_files(match='.mdb')
    xml.list_files(match='.xml')

    cnt_shapes = Counter(shapes.filenames)
    cnt_mdb = Counter([i[6:] for i in mdb.filenames])
    cnt_xml = Counter(xml.filenames)

    ota_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}
    missing_counter = {os.path.splitext(k)[0]: [] for k in cnt_shapes.keys()}

    for i in shapes.filepaths:
        path_list = i.split('\\')
        if kt.mel_type == 1:
            ota_counter[path_list[6]].append(int(path_list[4]))
        else:
            ota_counter[path_list[5]].append(int(path_list[4]))

    otas = [int(i) for i in kt.ota_list]

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

    for i in sorted(cnt_mdb):
        name, ext = os.path.splitext(i)
        print('{:<18} - {}'.format(name, cnt_mdb[i]))

    print("\nMETADATA")
    print('------------------')

    for i in sorted(cnt_xml):
        name, ext = os.path.splitext(i)
        print('{:<18} - {}'.format(name, cnt_xml[i]))

    print('')

    print("\nMISSING")
    print("------------------")

    for i in sorted(missing_counter, key=lambda x: len(missing_counter[x])):
        if missing_counter[i]:
            print('{:<18} - {}'.format(i, missing_counter[i]))

    print('')


def get_scanned():
    drive_letter = user_in('get_scanned')

    if drive_letter == '':
        drive_letter = 'W'

    progress_counter = 0
    files = 0

    for ota in kt.ota_list:
        with open(cp([meleti, outputdata, 'Scanned_List', '{}_Scanned_Files'.format(ota)]), 'w') as f:
            progress_counter += 1
            repo = cp([ota], origin=drive_letter)
            for dirpath, dirnames, filenames in os.walk(repo):
                for filename in filenames:
                    if filename.endswith('.tif') or filename.endswith('.TIF'):
                        files += 1
                        f.write('{}\n'.format(os.path.join(dirpath, filename)))
        progress(progress_counter, len(kt.ota_list))

    pm('\n\n{} scanned documents extracted from {}:/\n\n'.format(files, drive_letter))


if get_pass():
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
        extract('Temp', ktl['temp'][user])
        update_from_server()
    elif action_type == "1LPAA4PS5":
        shapefiles()
        clear()
        metadata()
    else:
        extract('Local', ktl['temp'][user])
else:
    pass
