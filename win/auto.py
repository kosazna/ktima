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
    action_type = (raw_input("(1) Export Shapefiles\n(2) Organize MDB's\n(3) Export NEW ROADS to InputData\n(4) Delete data\n(5) Create Metadata\n(6) Status\n(7) Update\n\n").upper())

    if action_type == "1LPAA4PS5":
        mod_date = (raw_input("\nDate for Metadata (xx/xx/xxxx) : \n").upper())

    meleti = str(sys.argv[1].split('\\')[1])
    ktdata = load_json(cp([meleti, inputdata, docs_i, 'KT_Info.json']))
    mel_type = ktdata["mel_type"]

    ktima_paths = KtimaPaths(meleti, mel_type)
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
        shape_list = ktdata["server_list"]
        log_status.append('Server')
        log_status.append('LocalData')

        if not shapes:
            for shape in ktdata["status_list"]:
                status.update('SHAPE', shape, False)
            status.update('EXPORTED', "FBOUND", False)
        else:
            for shape in user_shapes:
                status.update('SHAPE', shape, False)
    elif get_folder == "L" and export_folder == "P":
        shape_list = ktdata["local_list"]
        log_status.append('LocalData')
        log_status.append('ParadosiData')

    print("Initializing...")

    def export(e_shape, e_ota):
        inpath = ""
        outpath = ""

        if get_folder == "S" and export_folder == "L":
            inpath = cp([e_ota, 'SHP', e_shape + '.shp'], origin='K')
            outpath = ktima_paths(e_ota, e_shape, ext=True)
        elif get_folder == "L" and export_folder == "P":
            inpath = ktima_paths(e_ota, e_shape, ext=True)
            outpath = ktima_paths(e_ota, e_shape, ext=True, spatial_folder=paradosidata_o)
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
            for ota in ktdata["ota_list"]:
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
                for ota in ktdata["ota_list"]:
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
    input_data = cp([meleti, inputdata, databases_i])
    output_data = cp([meleti, outputdata, paradosimdb_o])
    output_data_vsteas = cp([meleti, outputdata, paradosidata_o])

    if get_pass():
        for rootDir, subdirs, filenames in os.walk(input_data):
            for ota in ktdata["ota_list"]:
                for filename in filenames:
                    if ota in filename and 'VSTEAS_REL' in filename:
                        inpathv = os.path.join(rootDir, filename)
                        outpathv = os.path.join(output_data_vsteas, ota, 'SHAPE', 'VSTEAS_REL', filename)
                        copyfile(inpathv, outpathv)
                    elif ota in filename:
                        inpath = os.path.join(rootDir, filename)
                        outpath = os.path.join(output_data, ota, filename)
                        copyfile(inpath, outpath)

        log("Export MDB's")
    else:
        pass

    print("Done !")


def roads():
    copy_list = ['*shp', '*shx', '*dbf']
    old_roads = cp([meleti, inputdata, shapefiles_i, roadsold_i])
    new_roads = cp([meleti, outputdata, paradosidata_o])

    if get_pass():
        def copy_files(x):
            for i in copy_list:
                for rootDir, subdirs, filenames in os.walk(new_roads):
                    for filename in fnmatch.filter(filenames, i):
                        if "ROADS" in filename:
                            inpath = os.path.join(rootDir, filename)
                            outpath = os.path.join(old_roads, rootDir[-x:], filename)
                            copyfile(inpath, outpath)

        if mel_type == 1:
            copy_files(17)
        else:
            copy_files(11)

        status.update("SHAPE", "iROADS", False)
        log('New ROADS to InputRoads folder')

        print("Done !")
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
        clearlocalpath = cp([meleti, outputdata, localdata_o])
        log_status.append('LocalData')
    elif clear_folder == "P":
        clearlocalpath = cp([meleti, outputdata, paradosidata_o])
        log_status.append('ParadosiData')
    elif clear_folder == "I":
        clearlocalpath = cp([meleti, inputdata, shapefiles_i, roadsold_i])
        log_status.append('InputRoads')

    del_list = []

    if clear_type == "A":
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*shp', '*shx', '*dbf', '*mdb', '*lock']
        log_status.append('all')
    elif clear_type == "S":
        del_list = ['*sbn', '*sbx', '*shp.xml', '*prj', '*idx', '*cpg', '*lock']
        log_status.append('standard')

    no_del = ktdata["no_del_list"]

    if get_pass():
        for i in del_list:
            for rootDir, subdirs, filenames in os.walk(clearlocalpath):
                for filename in fnmatch.filter(filenames, i):
                    if clear_type == "A" and clear_folder == "P" and filename[:-4] in no_del:
                        pass
                    else:
                        try:
                            os.remove(os.path.join(rootDir, filename))
                        except OSError:
                            print("Error while deleting file")

        log('Clear directories', log_status)

        print("Done !")
    else:
        pass


def metadata():
    if action_type == "1LPAA4PS5":
        date = mod_date
    else:
        date = (raw_input("\nDate (xx/xx/xxxx) : \n").upper())

    block_pnt_path = cp([meleti, inputdata, xml_i, 'BLOCK_PNT_METADATA.xml'])
    geo_path = cp([meleti, inputdata, xml_i, 'GEO_METADATA.xml'])
    roads_path = cp([meleti, inputdata, xml_i, 'ROADS_METADATA.xml'])

    try:
        with open(block_pnt_path, 'r') as block_pnt_f:
            block_pnt_cont = str(block_pnt_f.read())
    except IOError:
        pass

    try:
        with open(geo_path, 'r') as geo_f:
            geo_cont = str(geo_f.read())
    except IOError:
        pass

    try:
        with open(roads_path, 'r') as roads_f:
            roads_cont = str(roads_f.read())
    except IOError:
        pass

    if mel_type == 1:
        metas = {'BLOCK_PNT_METADATA': block_pnt_cont,
                 'ROADS_METADATA': roads_cont,
                 'GEO_METADATA': geo_cont}
    else:
        metas = {'ROADS_METADATA': roads_cont,
                 'GEO_METADATA': geo_cont}

    if get_pass():
        for ota in ktdata['ota_list']:
            for meta in metas:
                if mel_type == 1:
                    path = cp([meleti, outputdata, paradosidata_o, ota, 'METADATA', meta + '.xml'])
                else:
                    path = cp([meleti, outputdata, paradosidata_o, ota, meta + '.xml'])

                temp = metas[meta][:82] + str(ota) + metas[meta][87:]
                content = temp[:118] + date + temp[128:]

                with open(path, 'w') as meta_f:
                    meta_f.write(content)

        log("Metadata")

        print('\nDONE !\n')
    else:
        pass


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
        status.show()
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
