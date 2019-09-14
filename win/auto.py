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

if get_pass():
    action_type = (raw_input("(1) Export Shapefiles\n(2) Organize MDB's\n(3) Export NEW ROADS to InputData\n(4) Delete data\n(5) Create Metadata\n(6) Anaktiseis\n(7) Status\n(8) Update\n\n").upper())

    if action_type == "1LPAA4PS5":
        mod_date = (raw_input("\nDate for Metadata (xx/xx/xxxx) : \n").upper())

    meleti = str(sys.argv[1].split('\\')[1])
    data = load_json(cp([meleti, inputdata, docs_i, 'KT_Info.json']))

    kt = NamesAndLists(data)
    paths = Paths(meleti, kt.mel_type, kt.company_name)
else:
    print("\nAccess denied\n")
    action_type = "None"
    meleti = "None"

status = Status(meleti)
log = Log(meleti)


def shapefiles():
    if action_type == "1LPAA4PS5":
        get_folder = "L"
        export_folder = "P"
        shapes = ""
        ota_code = ""
    else:
        get_folder = (raw_input("\nGet from : (S)erver  or  (L)ocal \n\n").upper())
        export_folder = (raw_input("\nExport to : (L)ocal  or  (P)aradosi\n\n").upper())
        shapes = (raw_input("\nSHAPEFILE to export: (Enter for ALL)\n\n").upper())
        ota_code = (raw_input("\nOTA to export from: (Enter for ALL)\n\n").upper())

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
            print("NONE")
        else:
            for i in missing_list:
                print(i)
    else:
        pass


def mdbs():
    if get_pass():
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
        clear_folder = (raw_input("\nDelete from : (I)nputData  (L)ocal  or  (P)aradosi\n").upper())
        clear_type = (raw_input("\nDelete method : (A)ll  or  (S)tandard\n").upper())

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

    del_list = []

    if clear_type == "A":
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*shp', '*shx', '*dbf', '*mdb', '*lock']
        log_status.append('all')
    elif clear_type == "S":
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*lock']
        log_status.append('standard')

    if get_pass():
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


def anaktiseis():
    if get_pass():
        for rootDir, subdirs, filenames in os.walk(paths.anakt_in):
            for ota in kt.ota_list:
                for filename in filenames:
                    if ota in filename:
                        inpath = os.path.join(rootDir, filename)
                        outpath = os.path.join(paths.anakt_out, ota, filename)
                        copyfile(inpath, outpath)
    else:
        pass

    print("DONE !")


if get_pass():
    if action_type == "1":
        shapefiles()
    elif action_type == "2":
        mdbs()
    elif action_type == "3":
        roads()
    elif action_type == "4":
        clear()
    elif action_type == "5":
        metadata()
    elif action_type == "6":
        anaktiseis()
    elif action_type == "7":
        status.show()
    elif action_type == "8":
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
