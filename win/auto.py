# -*- coding: utf-8-sig -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import fnmatch
from ktima.status import *
from update import *

arcpy.env.overwriteOutput = True

meleti = str(sys.argv[1].split('\\')[1])
data = load_json(cp([meleti, inputdata, docs_i, 'KT_Info.json']))

kt = NamesAndLists(data)
paths = Paths(meleti, kt.mel_type, kt.company_name)
status = Status(meleti)
log = Log(meleti)


def user_in(func):
    console = {'action_type': "(1) Export Shapefiles\n"
                              "(2) Organize Files\n"
                              "(3) Create Metadata\n"
                              "(4) Export NEW ROADS to InputData\n"
                              "(5) Status\n"
                              "(6) Delete Data\n"
                              "(7) Update\n\n",
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
               'clear_type': "\nDelete method : (A)ll  or  (S)tandard\n",
               'org_folder': "\nFiles : (A)naktiseis  or  (S)aromena  or  (M)DB's\n"}

    sl = ['']
    ol = ['']
    [sl.append(i) for i in kt.local_list]
    [ol.append(i) for i in kt.ota_list]

    approved = {'action_type': ['', '1', '2', '3', '4', '5', '6', '7', '1LPAA4PS5'],
                'get_folder': ['S', 'L'],
                'export_folder': ['L', 'P'],
                'shapes': sl,
                'ota_code': ol,
                'clear_folder': ['I', 'L', 'P', 'A', 'S', 'M'],
                'clear_type': ['A', 'S'],
                'org_folder': ['A', 'S', 'M']}

    if func == 'shapes' or func == 'ota_code':
        action = raw_input(console[func]).upper()
        _action = action.split('-')
        count = 0

        if len(_action) != 1:
            for i in _action:
                if i in approved[func]:
                    count += 1

            while count != len(_action):
                print('\n\n!! Action Not Recognised. Try Again !!\n\n')
                count = 0
                action = raw_input(console[func]).upper()
                _action = action.split('-')
                for i in _action:
                    if i in approved[func]:
                        count += 1
        else:
            while action not in approved[func]:
                print('\n\n!! Action Not Recognised. Try Again !!\n\n')
                action = raw_input(console[func]).upper()
    else:
        action = raw_input(console[func]).upper()
        while action not in approved[func]:
            print('\n\n!! Action Not Recognised. Try Again !!\n\n')
            action = raw_input(console[func]).upper()

    return action


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

    print("Initializing...")

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
            print("--> {}".format(outpath))
            arcpy.CopyFeatures_management(inpath, outpath)
        else:
            missing_name = e_shape + "_" + e_ota
            missing_list.append(missing_name)

        return

    if get_pass():
        if ota_code == "" and shapes == "":
            for ota in kt.ota_list:
                for shape in shape_list:
                    export(shape, ota)
        elif ota_code != "" and shapes != "":
            for ota in user_ota_list:
                for shape in user_shapes:
                    export(shape, ota)
        elif ota_code != "":
            for ota in user_ota_list:
                for shape in shape_list:
                    export(shape, ota)
        elif shapes != "":
            for shape in user_shapes:
                for ota in kt.ota_list:
                    export(shape, ota)

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
    copy_list = ['*shp', '*shx', '*dbf']

    if get_pass():
        def copy_files(x):
            for i in copy_list:
                for rootDir, subdirs, filenames in os.walk(paths.new_roads):
                    for filename in fnmatch.filter(filenames, i):
                        if "ROADS" in filename:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(paths.old_roads, rootDir[-x:], filename)
                            copyfile(inpath, outpath)

        if kt.mel_type == 1:
            copy_files(17)
        else:
            copy_files(11)

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
        if clear_folder == 'L' or clear_folder == 'P' or clear_folder == 'I':
            for i in del_list:
                for rootDir, subdirs, filenames in os.walk(clearlocalpath):
                    for filename in fnmatch.filter(filenames, i):
                        if clear_type == "A" and clear_folder == "P" and filename[:-4] in kt.no_del_list:
                            pass
                        else:
                            try:
                                os.remove(os.path.join(rootDir, filename))
                            except OSError:
                                print("Error while deleting file")

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
        for ota in kt.ota_list:
            for meta in metas:
                path = paths.meta(ota, meta)

                temp = metas[meta][:82] + str(ota) + metas[meta][87:]
                content = temp[:118] + date + temp[128:]

                with open(path, 'w') as meta_f:
                    meta_f.write(content)

        log("Metadata")

        print('\nDONE !\n')
    else:
        pass


def organize():
    org_folder = user_in('org_folder')

    if get_pass():
        if org_folder == 'A':
            for rootDir, subdirs, filenames in os.walk(paths.anakt_in):
                for ota in kt.ota_list:
                    for filename in filenames:
                        if ota in filename[:5]:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(paths.anakt_out, ota, filename)
                            copyfile(inpath, outpath)
        elif org_folder == 'S':
            for rootDir, subdirs, filenames in os.walk(paths.saromena_in):
                for ota in kt.ota_list:
                    for filename in filenames:
                        if filename[0] == 'D' and ota in filename[1:6]:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(paths.saromena_out, ota, filename)
                            copyfile(inpath, outpath)
                        elif ota in filename[:5]:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(paths.saromena_out, ota, filename)
                            copyfile(inpath, outpath)
        elif org_folder == 'M':
            for rootDir, subdirs, filenames in os.walk(paths.mdb_in):
                for ota in kt.ota_list:
                    for filename in filenames:
                        if ota in filename and 'VSTEAS_REL' in filename:
                            inpathv = os.path.join(rootDir, filename)
                            outpathv = os.path.join(paths.mdb_vsteas, ota, 'SHAPE', 'VSTEAS_REL', filename)
                            copyfile(inpathv, outpathv)
                        elif ota in filename:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(paths.mdb_out, ota, filename)
                            copyfile(inpath, outpath)

            log("Export MDB's")
    else:
        pass

    print("DONE !")


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
        extract('Temp', ktl[user])
        update_from_server(ktl[user])
    elif action_type == "1LPAA4PS5":
        shapefiles()
        clear()
        metadata()
    else:
        extract('Local', ktl[user])
else:
    pass
