# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import csv
import fnmatch
from organize import *


class Geoprocessing:
    def __init__(self):
        pass

    @staticmethod
    @mxd
    def merge(shapes, force_merge=False, _roads='old'):
        log_list = []

        for _shape in shapes:
            if _shape == "ROADS":
                shapefile = choose_roads(_roads)
            else:
                shapefile = _shape

            if not status.check('SHAPE', shapefile) or force_merge:
                f_name = "merge_" + _shape

                try:
                    arcpy.Merge_management(mxd_fl[_shape]['list'], gdbm(f_name))
                    pm("\nMerged {}\n".format(_shape))
                    status.update('SHAPE', shapefile, True)
                    log_list.append(str(shapefile))
                except RuntimeError:
                    pm("\n!!! {} source files missing !!!\n".format(_shape))
            else:
                pm('\n{} already merged\n'.format(shapefile))

        if log_list:
            log("Merge Shapefiles", log_list=log_list)

    @staticmethod
    def union(shape, precision=0.0, gaps=False):
        if gaps:
            _gaps = "GAPS"
        else:
            _gaps = "NO_GAPS"

        if shape == "ALL":
            for shapefile in ktdata["merging_list"]:
                pm("Union for {}\n".format(shapefile))

                feature_name = "union_" + shapefile
                arcpy.Union_analysis(mxd_fl[shapefile]['list'], gdbm(feature_name), "NO_FID", precision, _gaps)

            log("Union Shapefiles")
        else:
            feature_name = "union_" + shape
            arcpy.Union_analysis(mxd_fl[shape]['list'], gdbm(feature_name), "NO_FID", precision, _gaps)


class Queries:
    def __init__(self):
        pass

    @staticmethod
    def kaek_in_dbound():
        arcpy.Intersect_analysis([gdbm(ktdata["merge"]["pst"]), gdbm(ktdata["merge"]["dbound"])], gdbm(ktdata["misc"]["kaek_in_dbound"]), output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(ktdata["misc"]["kaek_in_dbound"]))

    @staticmethod
    def kaek_in_astik():
        arcpy.Intersect_analysis([gdbm(ktdata["merge"]["pst"]), gdbm(ktdata["merge"]["astik"])], gdbm(ktdata["misc"]["kaek_in_astik"]), output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(ktdata["misc"]["kaek_in_astik"]))

    @staticmethod
    def rd():
        add_layer([ktdata["merge"]["pst"]])
        arcpy.SelectLayerByAttribute_management(ktdata["merge"]["pst"], "NEW_SELECTION", " PROP_TYPE = '0701' ")
        arcpy.CopyFeatures_management(ktdata["merge"]["pst"], gdbm(ktdata["misc"]["rd"]))
        pm('\nDONE !  -->  {}\n'.format(ktdata["misc"]["rd"]))

    @staticmethod
    def pr():
        add_layer([ktdata["merge"]["pst"]])
        arcpy.SelectLayerByAttribute_management(ktdata["merge"]["pst"], "NEW_SELECTION", " PROP_TYPE = '0702' ")
        arcpy.CopyFeatures_management(ktdata["merge"]["pst"], gdbm(ktdata["misc"]["pr"]))
        pm('\nDONE !  -->  {}\n'.format(ktdata["misc"]["pr"]))


class General:
    def __init__(self):
        pass

    @staticmethod
    def isolate(fc):
        if status.check('SHAPE', 'ASTOTA'):
            add_layer([ktdata["merge"]["astota"]])

            astota_n = "__{}_{}_ORIA_{}".format(meleti[:3], meleti[4:], ktdata["company_name"])
            arcpy.Dissolve_management(ktdata["merge"]["astota"], gdbm(astota_n))

            fc_n = "{}_{}".format(ktdata["company_name"], fc)
            arcpy.Intersect_analysis([fc, astota_n], gdbm(fc_n), output_type="INPUT")

            mdf(astota_n, importance='!!')
            mdf(fc_n)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    @mxd
    def export_per_ota(fc, spatial=True, field='KAEK', export_shp=True, database=False, formal=False, name=None):

        def export(_fc, _ota):
            if export_shp:
                if database:
                    mdf(_fc, importance='!!', out='ota', ota=_ota)
                    fc_name = "{}_{}".format(_fc, _ota)
                    arcpy.CopyFeatures_management(fc, mdb(fc_name))
                elif formal:
                    mdf(fc, out='formal', ota=ota, _name=name)
                else:
                    mdf(_fc, importance='!!', out='ota', ota=_ota)
            else:
                fc_name = "{}_{}".format(_fc, _ota)
                arcpy.CopyFeatures_management(_fc, gdbm(fc_name))

        if spatial:
            for lyr_astota in mxdASTOTA:
                ota = str(lyr_astota[7:])
                arcpy.SelectLayerByLocation_management(fc, 'WITHIN', lyr_astota)

                if get_count(fc) != 0:
                    export(fc, ota)
                    clear_selection(fc)
        else:
            arcpy.AddField_management(fc, "_OTA_", "TEXT", field_length=5)
            arcpy.CalculateField_management(fc, "_OTA_", '!{}![:5]'.format(field), "PYTHON_9.3")

            for ota in ktdata["ota_list"]:
                arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", " _OTA_ = '{}' ".format(ota))

                if get_count(fc) != 0:
                    export(fc, ota)
                    clear_selection(fc)


class Check:
    def __init__(self):
        pass

    @staticmethod
    @mxd
    def shapes(x):
        if status.check('SHAPE', "PST") and status.check('SHAPE', "ASTTOM") and status.check('SHAPE', "ASTENOT"):
            precision = float(10 ** -x)
            precision_txt = '{:.{}f} m'.format(precision, x)

            pm("\nCheck accuracy : {}\n".format(precision_txt))

            # geoprocessing
            geoprocessing.union("PST", precision, gaps=False)
            geoprocessing.union("ASTENOT", precision, gaps=True)
            geoprocessing.union("ASTTOM", precision, gaps=False)

            turn_off()
            add_layer([ktdata["merge"]["pst"], ktdata["merge"]["astenot"], ktdata["merge"]["asttom"]])

            # ENOTHTES
            arcpy.AddField_management(ktdata["merge"]["astenot"], "ENOT", "TEXT", field_length=50)
            arcpy.CalculateField_management(ktdata["merge"]["astenot"], "ENOT", '!CAD_ADMIN!', "PYTHON_9.3")

            # TOMEIS
            arcpy.AddField_management(ktdata["merge"]["asttom"], "TOM", "TEXT", field_length=50)
            arcpy.CalculateField_management(ktdata["merge"]["asttom"], "TOM", '!CAD_ADMIN!', "PYTHON_9.3")

            arcpy.SpatialJoin_analysis(ktdata["merge"]["pst"], ktdata["merge"]["astenot"], gdbm(ktdata["misc"]["pst_astenot"]), match_option='WITHIN')
            arcpy.SpatialJoin_analysis(ktdata["merge"]["astenot"], ktdata["merge"]["asttom"], gdbm(ktdata["misc"]["astenot_asttom"]), match_option='WITHIN')

            turn_off()

            arcpy.AddField_management(ktdata["misc"]["pst_astenot"], "pstENOT", "TEXT", field_length=50)
            arcpy.AddField_management(ktdata["misc"]["pst_astenot"], "matches", "TEXT", field_length=50)
            arcpy.CalculateField_management(ktdata["misc"]["pst_astenot"], "PSTenot", '!KAEK![:9]', "PYTHON_9.3")
            arcpy.CalculateField_management(ktdata["misc"]["pst_astenot"], "matches", 'bool(!CAD_ADMIN!==!pstENOT!)', "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["pst_astenot"], "NEW_SELECTION", " matches = '0' and pstENOT not like '%ΕΚ%' ")
            arcpy.CopyFeatures_management(ktdata["misc"]["pst_astenot"], gdbc(ktdata["probs"]["pst_astenot"]))

            arcpy.AddField_management(ktdata["misc"]["astenot_asttom"], "enotTOM", "TEXT", field_length=50)
            arcpy.AddField_management(ktdata["misc"]["astenot_asttom"], "matches", "TEXT", field_length=50)
            arcpy.CalculateField_management(ktdata["misc"]["astenot_asttom"], "enotTOM", '!ENOT![:7]', "PYTHON_9.3")
            arcpy.CalculateField_management(ktdata["misc"]["astenot_asttom"], "matches", 'bool(!TOM!==!enotTOM!)', "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["astenot_asttom"], "NEW_SELECTION", " matches = '0' ")
            arcpy.CopyFeatures_management(ktdata["misc"]["astenot_asttom"], gdbc(ktdata["probs"]["astenot_asttom"]))

            # Problem count
            count_pst_u = get_count(ktdata["union"]["pst"])
            count_pst_m = get_count(ktdata["merge"]["pst"])
            diff_pst = count_pst_u - count_pst_m
            count_astenot_u = get_count(ktdata["union"]["astenot"])
            count_astenot_m = get_count(ktdata["merge"]["astenot"])
            diff_astenot = count_astenot_u - count_astenot_m
            count_asttom_u = get_count(ktdata["union"]["asttom"])
            count_asttom_m = get_count(ktdata["merge"]["asttom"])
            diff_asttom = count_asttom_u - count_asttom_m
            count_pst_astenot = get_count(ktdata["probs"]["pst_astenot"])
            count_astenot_asttom = get_count(ktdata["probs"]["astenot_asttom"])

            if count_astenot_m != count_astenot_u:
                arcpy.Erase_analysis(ktdata["union"]["astenot"], ktdata["merge"]["astenot"], gdbc(ktdata["probs"]["overlaps_astenot"]))
            if count_asttom_m != count_asttom_u:
                arcpy.Erase_analysis(ktdata["union"]["asttom"], ktdata["merge"]["asttom"], gdbc(ktdata["probs"]["overlaps_asttom"]))
            if count_pst_m != count_pst_u:
                arcpy.Erase_analysis(ktdata["union"]["pst"], ktdata["merge"]["pst"], gdbc(ktdata["probs"]["overlaps_pst"]))

            log_shapes = [precision_txt,
                          diff_pst,
                          diff_astenot,
                          diff_asttom,
                          count_pst_astenot,
                          count_astenot_asttom]

            # TO UNION PREPEI NA EINAI IDIO ME TO MERGE
            if count_pst_m == count_pst_u:
                pm('PST - OK')
            else:
                pm('PST - ! Overlaps ! - [{}]'.format(diff_pst))

            if count_astenot_m == count_astenot_u:
                pm('ASTENOT - OK')
            else:
                pm('ASTENOT - ! Overlaps ! - [{}]'.format(diff_astenot))

            if count_asttom_m == count_asttom_u:
                pm('ASTTOM - OK\n')
            else:
                pm('ASTTOM - ! Overlaps ! - [{}]\n'.format(diff_asttom))

            # PREPEI NA MIN YPARXEI KAMIA EGGRAFI STOUS PROBLIMATIKOUS PINAKES

            if count_pst_astenot == 0:
                pm('PST me ASTENOT - OK')
            else:
                pm('! Lathos KAEK se ENOTITA ! - [{}]'.format(count_pst_astenot))

            if count_astenot_asttom == 0:
                pm('ASTENOT me ASTTOM - OK\n')
            else:
                pm('! Lathos KAEK se TOMEA ! - [{}]\n'.format(count_astenot_asttom))

            time_now = timestamp()

            log("Check Shapefiles", log_shapes)
            status.update("OVERLAPS", "DECIMALS", precision_txt)
            status.update("OVERLAPS", "CD", time_now)
            status.update("OVERLAPS", "ASTENOT", diff_astenot)
            status.update("OVERLAPS", "ASTTOM", diff_asttom)
            status.update("OVERLAPS", "PST", diff_pst)
            status.update("WRONG_KAEK", "ASTENOT_ASTTOM", count_astenot_asttom)
            status.update("WRONG_KAEK", "PST_ASTENOT", count_pst_astenot)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    def pst_geometry():
        if status.check('SHAPE', "PST"):
            arcpy.CheckGeometry_management(gdbm(ktdata["merge"]["pst"]), gdbc(ktdata["geometry"]["pst"]))

            count_geom = get_count(ktdata["geometry"]["pst"])
            problematic_set = set()
            problematic = []

            # Elegxos gia to an uparxoun self_intersections kai apomonosi ton provlimatikon KAEK
            if count_geom == 0:
                pm("\nGEOMETRY OK - NO SELF INTERSECTIONS.\n")
            else:
                pm("\n{} SELF INTERSECTIONS.\n".format(count_geom))
                pm("Processing...\n")
                arcpy.AddJoin_management(ktdata["merge"]["pst"], "OBJECTID", ktdata["geometry"]["pst"], "FEATURE_ID", "KEEP_COMMON")
                arcpy.CopyFeatures_management(ktdata["merge"]["pst"], gdbc(ktdata["probs"]["geometry_kaek"]))
                clear_selection(ktdata["merge"]["pst"])
                arcpy.AddField_management(ktdata["probs"]["geometry_kaek"], "OTA", "TEXT", field_length=5)
                arcpy.CalculateField_management(ktdata["probs"]["geometry_kaek"], "OTA", '!merge_PST_KAEK![:5]', "PYTHON_9.3")
                arcpy.Dissolve_management(ktdata["probs"]["geometry_kaek"], gdbc(ktdata["probs"]["geometry_ota"]), "OTA")
                cursor = arcpy.UpdateCursor(ktdata["probs"]["geometry_ota"])

                for row in cursor:
                    ota = int(row.getValue("OTA"))
                    problematic_set.add(ota)

                for item in problematic_set:
                    problematic.append(item)

                problematic.sort()

                pm("OTA with geometry problems:\n")
                for prob_ota in problematic:
                    pm(prob_ota)

                pm("\n")

            log_geometry = [count_geom,
                            problematic]

            time_now = timestamp()

            status.update("SHAPES_GEOMETRY", "PROBS", bool(count_geom))
            status.update("SHAPES_GEOMETRY", "CD", time_now)
            status.update("SHAPES_GEOMETRY", "OTA", problematic)

            pm("\nDONE !\n")

            log('Check PST Geometry', log_geometry)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    @mxd
    def fbound_geometry():
        if status.check('EXPORTED', "FBOUND"):
            try:
                arcpy.CheckGeometry_management(mxdFBOUND, gdbc(ktdata["geometry"]["fbound"]))

                count_geom = get_count(ktdata["geometry"]["fbound"])
                problematic_set = set()
                problematic = []

                # Elegxos gia to an uparxoun self_intersections kai apomonosi ton provlimatikon KAEK
                if count_geom == 0:
                    pm("\nGEOMETRY OK - NO SELF INTERSECTIONS IN FBOUND.\n")
                else:
                    arcpy.AddField_management(ktdata["geometry"]["fbound"], "OTA", "TEXT", field_length=5)
                    arcpy.CalculateField_management(ktdata["geometry"]["fbound"], "OTA", '!CLASS![-5:]', "PYTHON_9.3")
                    pm("\n{} SELF INTERSECTIONS IN FBOUND.\n".format(count_geom))

                    cursor = arcpy.UpdateCursor(ktdata["geometry"]["fbound"])
                    for row in cursor:
                        ota = int(row.getValue("OTA"))
                        problematic_set.add(ota)

                    for item in problematic_set:
                        problematic.append(item)

                    problematic.sort()

                    pm("OTA with FBOUND geometry problems :\n")
                    for prob_ota in problematic:
                        pm(prob_ota)

                log_fbound_geometry = [count_geom,
                                       problematic]

                pm("\nDONE !\n")

                time_now = timestamp()

                status.update("FBOUND_GEOMETRY", "PROBS", bool(count_geom))
                status.update("FBOUND_GEOMETRY", "CD", time_now)
                status.update("FBOUND_GEOMETRY", "OTA", problematic)

                log('Check FBOUND Geometry', log_fbound_geometry)
            except RuntimeError:
                pm("\n!!! {} source files missing !!!\n".format('FBOUND'))
        else:
            raise Exception("\n\n\n!!! Den exeis vgalei kainouria FBOUND !!!\n\n\n")

    @staticmethod
    def roads(_roads='old'):
        roads = choose_roads(_roads)
        if status.check('SHAPE', "PST") and status.check('SHAPE', roads) and status.check('SHAPE', "ASTENOT"):
            add_layer([ktdata["merge"]["pst"], ktdata["merge"]["roads"], ktdata["merge"]["astenot"]])

            # Eksagwgh kai enosi eidikwn ektasewn
            arcpy.SelectLayerByAttribute_management(ktdata["merge"]["pst"], "NEW_SELECTION", " PROP_TYPE = '0701' ")
            arcpy.CopyFeatures_management(ktdata["merge"]["pst"], gdbm(ktdata["misc"]["ek"]))
            clear_selection(ktdata["merge"]["pst"])
            arcpy.Dissolve_management(ktdata["misc"]["ek"], gdbm(ktdata["misc"]["temp_ek"]), "PROP_TYPE")

            # Elegxos gia aksones ektos EK
            arcpy.Intersect_analysis([ktdata["merge"]["roads"], ktdata["misc"]["temp_ek"]], gdbc(ktdata["misc"]["intersections_roads"]), output_type="POINT")
            arcpy.DeleteField_management(ktdata["misc"]["intersections_roads"], "PROP_TYPE")

            # Elegxos gia aksones pou mporei na kovoun thn idia enotita
            arcpy.SpatialJoin_analysis(ktdata["misc"]["intersections_roads"], ktdata["merge"]["pst"], gdbm(ktdata["misc"]["intersections_pst_rd"]), match_option="CLOSEST")
            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["intersections_pst_rd"], "NEW_SELECTION", " PROP_TYPE = '0101' ")
            arcpy.SpatialJoin_analysis(ktdata["misc"]["intersections_pst_rd"], ktdata["merge"]["astenot"], gdbm(ktdata["misc"]["intersections_astenot_rd"]))

            count_inter_all = get_count(ktdata["misc"]["intersections_roads"])
            count_inter_astenot = get_count(ktdata["misc"]["intersections_astenot_rd"])

            if count_inter_astenot > 10:
                arcpy.Dissolve_management(ktdata["misc"]["intersections_astenot_rd"], gdbc(ktdata["probs"]["roads"]), "CAD_ADMIN", "CAD_ADMIN COUNT")
            else:
                arcpy.SpatialJoin_analysis(ktdata["misc"]["intersections_pst_rd"], ktdata["merge"]["astenot"], gdbc(ktdata["probs"]["roads"]))

            log_roads = [count_inter_all,
                         count_inter_astenot]

            if count_inter_all == 0:
                pm("\nROADS - OK\n")
            else:
                pm("\nROADS intersections - [{}]".format(count_inter_all))
                pm("ROADS intersections me ASTENOT - [{}].\n".format(count_inter_astenot))

            time_now = timestamp()

            log('Check ROADS', log_roads)
            status.update("ROADS", "ALL", count_inter_all)
            status.update("ROADS", "PROBS", count_inter_astenot)
            status.update("ROADS", "CD", time_now)
            status.update("ROADS", "CPROBS", bool(count_inter_all))
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    def dbound():
        if status.check('SHAPE', "DBOUND"):
            # Elegxos gia DBOUND pou mporei na toys leipei eite to DEC_ID eite to DEC_DATE
            add_layer([ktdata["merge"]["dbound"]])

            arcpy.SelectLayerByAttribute_management(ktdata["merge"]["dbound"], "NEW_SELECTION", " DEC_ID = '' ")
            arcpy.SelectLayerByAttribute_management(ktdata["merge"]["dbound"], "ADD_TO_SELECTION", " DEC_DATE IS NULL ")
            arcpy.CopyFeatures_management(ktdata["merge"]["dbound"], gdbc(ktdata["probs"]["dbound"]))

            count_dbound = get_count(ktdata["probs"]["dbound"])

            if count_dbound == 0:
                pm("\nDBOUND - OK\n")
            else:
                pm("\n{} eggrafes den exoun DEC_ID / DEC_DATE.\n".format(count_dbound))

            time_now = timestamp()

            log('Check DBOUND', count_dbound)
            status.update("DBOUND", "PROBS", count_dbound)
            status.update("DBOUND", "CD", time_now)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    def bld():
        if status.check('SHAPE', "BLD"):
            # Elegxos gia BLD pou mporei na exoun thn timh '0' eite sto BLD_T_C eite sto BLD_NUM
            add_layer([ktdata["merge"]["bld"]])

            arcpy.SelectLayerByAttribute_management(ktdata["merge"]["bld"], "NEW_SELECTION", " BLD_T_C = 0 ")
            arcpy.SelectLayerByAttribute_management(ktdata["merge"]["bld"], "ADD_TO_SELECTION", " BLD_NUM = 0 ")
            arcpy.CopyFeatures_management(ktdata["merge"]["bld"], gdbm(ktdata["misc"]["temp_bld"]))
            arcpy.SpatialJoin_analysis(ktdata["misc"]["temp_bld"], gdbm(ktdata["merge"]["pst"]), gdbc(ktdata["probs"]["bld"]), match_option='WITHIN')

            count_bld = get_count(ktdata["probs"]["bld"])

            if count_bld == 0:
                pm("\nBLD - OK\n")
            else:
                pm("\n{} eggrafes den exoun BLD_T_C / BLD_NUM.\n".format(count_bld))

            time_now = timestamp()

            log('Check BLD', count_bld)
            status.update("BLD", "PROBS", count_bld)
            status.update("BLD", "CD", time_now)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")


class Fix:
    def __init__(self):
        pass

    @staticmethod
    def pst_geometry():
        if status.check('SHAPES_GEOMETRY', "PROBS"):
            # Epilogi olon ton shapefile enos provlimatikou OTA kai epidiorthosi tis geometrias tous
            data = load_json(status_path)

            repaired = []

            for row in data["SHAPES_GEOMETRY"]["OTA"]:
                ota_folder = str(row)
                repaired.append(int(ota_folder))
                for i in ktdata["geometry_list"]:
                    lyr = ktima_paths(ota_folder, i, ext=True)

                    if arcpy.Exists(lyr):
                        pm("Repairing geometry in {}_{}".format(i, ota_folder))
                        arcpy.RepairGeometry_management(lyr, "KEEP_NULL")

            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix Geometry', repaired)

    @staticmethod
    def fbound_geometry():
        if status.check('FBOUND_GEOMETRY', "PROBS"):
            # Epidiorthosi ton FBOUND
            data = load_json(status_path)

            repaired = []

            for row in data["FBOUND_GEOMETRY"]["OTA"]:
                repair_ota = str(row)
                repaired.append(int(repair_ota))

                lyr = ktima_paths(repair_ota, "FBOUND", ext=True)

                if arcpy.Exists(lyr):
                    pm("Repairing geometry in FBOUND_{}".format(repair_ota))
                    arcpy.RepairGeometry_management(lyr, "DELETE_NULL")

            status.update('SHAPE', 'FBOUND', False)
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix FBOUND Geometry', repaired)

    @staticmethod
    def roads():
        if status.check("ROADS", "CPROBS"):
            # Kopsimo ton aksonon 10 cm prin to orio tis enotitas
            arcpy.Buffer_analysis(gdbm(ktdata["misc"]["temp_ek"]), gdbm(ktdata["misc"]["ek_fixed_bound"]), ktdata["misc"]["ek_bound_reduction"])
            arcpy.Clip_analysis(gdbm(ktdata["merge"]["roads"]), gdbm(ktdata["misc"]["ek_fixed_bound"]), gdbm(ktdata["misc"]["gdb_roads_all"]))

            status.update("EXPORTED", "ROADS", False)

            log('Fix ROADS')
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")


class Fields:
    def __init__(self):
        pass

    @staticmethod
    @mxd
    def pst():
        # Diorthosi ton pedion ORI_TYPE, DEC_ID kai ADDRESS stous PST me vasi tis prodiagrafes
        for lyr_pst in mxdPST:
            pm("Processing {}".format(lyr_pst))
            arcpy.SelectLayerByAttribute_management(lyr_pst, "NEW_SELECTION", " ORI_CODE = '' ")
            arcpy.CalculateField_management(lyr_pst, "ORI_TYPE", '1', "PYTHON_9.3")
            arcpy.CalculateField_management(lyr_pst, "DEC_ID", "''", "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(lyr_pst, "NEW_SELECTION", " ADDRESS = '' ")
            arcpy.CalculateField_management(lyr_pst, "ADDRESS", "'ΑΝΩΝΥΜΟΣ'", "PYTHON_9.3")

        pm("\nDONE !\n")

        log('Fields PST')

    @staticmethod
    @mxd
    def asttom():
        # Diagrafi ACQ_SCALE apo tous ASTTOM
        for lyr_asttom in mxdASTTOM:
            pm("Processing {}".format(lyr_asttom))
            arcpy.DeleteField_management(lyr_asttom, "ACQ_SCALE", )

        pm("\nDONE !\n")

        log('Fields ASTTOM')

    @staticmethod
    @mxd
    def astenot():
        # Prosthiki onomasias sto pedio LOCALITY ton ASTENOT me vasi txt arxeio
        with open(locality) as csvfile:
            localnames = csv.reader(csvfile)

            for row in localnames:
                try:
                    ota = row[0][:5]
                    lyr_astenot = "ASTENOT_{}".format(ota)
                    pm("Processing {}".format(lyr_astenot))
                    arcpy.SelectLayerByAttribute_management(lyr_astenot, "NEW_SELECTION", " CAD_ADMIN LIKE '%{}%' ".format(row[0]))
                    arcpy.CalculateField_management(lyr_astenot, "LOCALITY", "'{}'".format(row[1]), "PYTHON_9.3")
                    arcpy.SelectLayerByAttribute_management(lyr_astenot, "NEW_SELECTION", " LOCALITY = '' ")
                    arcpy.CalculateField_management(lyr_astenot, "LOCALITY", "'{}'".format(row[2]), "PYTHON_9.3")
                except IndexError:
                    pm("Leipei onomatologia gia {}".format(ota))

        pm("\nDONE !\n")

        log('Fields ASTENOT')


class Create:
    def __init__(self):
        pass

    @staticmethod
    def fbound():
        if status.check('SHAPE', "ASTOTA"):
            # Dhmiourgia tou sunolikou FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis([gdbm(ktdata["merge"]["astota"]), dasinpath], gdbm(ktdata["misc"]["gdb_fbound_all"]), output_type="INPUT")
            arcpy.DeleteField_management(gdbm(ktdata["misc"]["gdb_fbound_all"]), ["FID_merge_ASTOTA", "FID_PO_PARCELS", "FIELD", "AREA", "LEN"])
            arcpy.FeatureClassToFeatureClass_conversion(gdbm(ktdata["misc"]["gdb_fbound_all"]), fboundoutpath, ktdata["misc"]["fbound_all"])

            turn_off()

            # # Dhmiourgia pinaka FBOUND vasi ton prodiagrafon
            arcpy.DeleteField_management(fboundinpath, ["Shape_Leng", "Shape_Area"])
            arcpy.AddField_management(fboundinpath, "ORI_CODE", "SHORT", field_precision=1)
            arcpy.AddField_management(fboundinpath, "DOC_ID", "TEXT", field_length=254)
            arcpy.AddField_management(fboundinpath, "AREA", "DOUBLE")
            arcpy.AddField_management(fboundinpath, "LEN", "DOUBLE")
            arcpy.CalculateField_management(fboundinpath, "ORI_CODE", "1", "PYTHON_9.3")
            arcpy.CalculateField_management(fboundinpath, "AREA", "float(!shape.Area@UNKNOWN!)", "PYTHON_9.3")
            arcpy.CalculateField_management(fboundinpath, "LEN", "float(!shape.Length@UNKNOWN!)", "PYTHON_9.3")

            # Prosthiki DOC_ID sto pinaka me vasi txt arxeio
            with open(fbounddoc) as csvfile:
                docs = csv.reader(csvfile)

                lyr_fbound = ktdata["misc"]["fbound_all"]
                pm("Processing DOC_ID in {}".format(lyr_fbound))

                for row in docs:
                    try:
                        ota = row[0]
                        area = int(row[2]) * 2000
                        arcpy.SelectLayerByAttribute_management(lyr_fbound, "NEW_SELECTION", " CAD_ADMIN LIKE '%{}%' AND AREA >= {} ".format(ota, area))
                        arcpy.CalculateField_management(lyr_fbound, "DOC_ID", "'{}'".format(row[1]), "PYTHON_9.3")
                    except IndexError:
                        pm("Leipei DOC_ID gia {} apo to .txt arxeio".format(ota))

            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["fbound_all"], "NEW_SELECTION", " DOC_ID = '' ")

            if get_count(ktdata["misc"]["fbound_all"]) != 0:
                pm("\n !!! Leipoun DOC_ID apo to FBOUND_ALL \n!!!")

            clear_selection(ktdata["misc"]["fbound_all"])

            arcpy.DeleteField_management(ktdata["misc"]["fbound_all"], "CAD_ADMIN")

            pm("Exporting FBOUND / OTA")

            # Eksagogi FBOUND ana OTA
            general.export_per_ota(ktdata["misc"]["fbound_all"], formal=True, name="FBOUND")

            mdf(ktdata["misc"]["fbound_all"], importance='!')

            pm("\nDONE !\n")

            time_now = timestamp()

            status.update("EXPORTED", "FBOUND", True)
            status.update("SHAPE", "FBOUND", False)
            status.update("EXPORTED", "FBOUND_ED", time_now)

            log('Create FBOUND')
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    def roads():
        if status.check("ROADS", "CPROBS") and not status.check("EXPORTED", "ROADS"):
            arcpy.FeatureClassToFeatureClass_conversion(gdbm(ktdata["misc"]["gdb_roads_all"]), rdoutpath, ktdata["misc"]["roads_all"])

            # Dhmiourgia pinaka ROADS vasi ton prodiagrafon
            arcpy.DeleteField_management(rdinpath, ["LEFTFROM", "LEFTTO", "RIGHTFROM", "RIGHTTO"])
            arcpy.AddField_management(rdinpath, "LEFTFROM", "SHORT", field_precision=3)
            arcpy.AddField_management(rdinpath, "LEFTTO", "SHORT", field_precision=3)
            arcpy.AddField_management(rdinpath, "RIGHTFROM", "SHORT", field_precision=3)
            arcpy.AddField_management(rdinpath, "RIGHTTO", "SHORT", field_precision=3)
            arcpy.AddField_management(rdinpath, "L", "SHORT", field_precision=5)
            arcpy.AddField_management(rdinpath, "R", "SHORT", field_precision=5)
            arcpy.CalculateField_management(rdinpath, "L", '!LEFTTK!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "R", '!RIGHTTK!', "PYTHON_9.3")
            arcpy.DeleteField_management(rdinpath, ["LEFTTK", "RIGHTTK"])
            arcpy.AddField_management(rdinpath, "LEFTTK", "SHORT", field_precision=5)
            arcpy.AddField_management(rdinpath, "RIGHTTK", "SHORT", field_precision=5)
            arcpy.CalculateField_management(rdinpath, "LEFTTK", '!L!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "RIGHTTK", '!R!', "PYTHON_9.3")
            arcpy.DeleteField_management(rdinpath, ["L", "R"])
            arcpy.AddField_management(rdinpath, "L", "TEXT", field_length=50)
            arcpy.AddField_management(rdinpath, "R", "TEXT", field_length=50)
            arcpy.AddField_management(rdinpath, "S", "TEXT", field_length=254)
            arcpy.AddField_management(rdinpath, "C", "DATE", )
            arcpy.CalculateField_management(rdinpath, "L", '!LEFTMIN!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "R", '!RIGHTMIN!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "S", '!STREETNAME!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "C", '!COLLDATE!', "PYTHON_9.3")
            arcpy.DeleteField_management(rdinpath, ["LEFTMIN", "RIGHTMIN", "STREETNAME", "COLLDATE", "LEN", "Shape_Leng"])
            arcpy.AddField_management(rdinpath, "LEFTMIN", "TEXT", field_length=50)
            arcpy.AddField_management(rdinpath, "RIGHTMIN", "TEXT", field_length=50)
            arcpy.AddField_management(rdinpath, "STREETNAME", "TEXT", field_length=254)
            arcpy.AddField_management(rdinpath, "COLLDATE", "DATE")
            arcpy.CalculateField_management(rdinpath, "LEFTMIN", '!L!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "RIGHTMIN", '!R!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "STREETNAME", '!S!', "PYTHON_9.3")
            arcpy.CalculateField_management(rdinpath, "COLLDATE", '!C!', "PYTHON_9.3")
            arcpy.DeleteField_management(rdinpath, ["L", "R", "S", "C"])
            arcpy.AddField_management(rdinpath, "LEN", "DOUBLE")
            arcpy.CalculateField_management(rdinpath, "LEN", "float(!shape.Length@UNKNOWN!)", "PYTHON_9.3")

            pm("\nExporting ROADS / OTA")

            # Eksagogi ROADS ana OTA
            general.export_per_ota(ktdata["misc"]["roads_all"], formal=True, name="ROADS")

            mdf(ktdata["misc"]["roads_all"], importance='!')

            time_now = timestamp()

            status.update("SHAPE", "ROADS", False)
            status.update("EXPORTED", "ROADS", True)
            status.update("EXPORTED", "ROADS_ED", time_now)

            log('Create ROADS')

            pm("\nDONE !\n")
        else:
            copy_list = ['*shp', '*shx', '*dbf']
            old_roads = cp([meleti, inputdata, shapefiles_i, roadsold_i])
            new_roads = cp([meleti, outputdata, localdata_o])

            def copy_files(x):
                for _i in copy_list:
                    for rootDir, subdirs, filenames in os.walk(old_roads):
                        for filename in fnmatch.filter(filenames, _i):
                            if "ROADS" in filename:
                                _inpath = os.path.join(rootDir, filename)
                                _outpath = os.path.join(new_roads, rootDir[-x:], filename)
                                copyfile(_inpath, _outpath)

            if mel_type == 1:
                copy_files(17)
            else:
                copy_files(11)

            status.update("SHAPE", "ROADS", False)

            log('Copied old Roads to LocalData')

            pm("\nDONE !\n")

    @staticmethod
    def fboundclaim():
        if status.check('SHAPE', "PST") and status.check('SHAPE', "FBOUND"):
            # Dhmiourgia tou pinaka tis diekdikisis tou dasous
            arcpy.Intersect_analysis([gdbm(ktdata["merge"]["pst"]), gdbm(ktdata["merge"]["fbound"])], gdbm(ktdata["misc"]["intersection_pst_fbound"]), output_type="INPUT")
            arcpy.Dissolve_management(ktdata["misc"]["intersection_pst_fbound"], gdbm(ktdata["misc"]["gdb_fbound_claim"]), ["KAEK", "AREA"])
            arcpy.FeatureClassToFeatureClass_conversion(ktdata["misc"]["gdb_fbound_claim"], claimoutpath, ktdata["misc"]["fbound_claim"])

            turn_off()

            # Diagrafi eggrafon vasi tupikon prodiagrafon
            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["fbound_claim"], "NEW_SELECTION", " Shape_Area < 100 ")  # Svinontai oles oi eggrafes kato apo 100 m2
            arcpy.DeleteRows_management(ktdata["misc"]["fbound_claim"])
            clear_selection(ktdata["misc"]["fbound_claim"])
            arcpy.AddField_management(ktdata["misc"]["fbound_claim"], "AREA_MEAS", "DOUBLE", field_precision=15, field_scale=3)
            arcpy.AddField_management(ktdata["misc"]["fbound_claim"], "AREAFOREST", "DOUBLE", field_precision=15, field_scale=3)
            arcpy.AddField_management(ktdata["misc"]["fbound_claim"], "AREA_REST", "DOUBLE", field_precision=15, field_scale=3)
            arcpy.CalculateField_management(ktdata["misc"]["fbound_claim"], "AREA_MEAS", '!AREA!', "PYTHON_9.3")
            arcpy.CalculateField_management(ktdata["misc"]["fbound_claim"], "AREAFOREST", '!Shape_Area!', "PYTHON_9.3")
            arcpy.CalculateField_management(ktdata["misc"]["fbound_claim"], "AREA_REST", '!AREA_MEAS! - !AREAFOREST!', "PYTHON_9.3")
            arcpy.AddField_management(ktdata["misc"]["fbound_claim"], "TYPE", "SHORT", field_precision=1)
            arcpy.SelectLayerByAttribute_management(ktdata["misc"]["fbound_claim"], "NEW_SELECTION", " AREA_REST < 1 ")  # Oles oi eggrafes me AREA_REST kato apo 1 m2  diekdikountai pliros
            arcpy.CalculateField_management(ktdata["misc"]["fbound_claim"], "AREA_REST", '0', "PYTHON_9.3")
            arcpy.CalculateField_management(ktdata["misc"]["fbound_claim"], "TYPE", '1', "PYTHON_9.3")
            clear_selection(ktdata["misc"]["fbound_claim"])
            arcpy.DeleteField_management(ktdata["misc"]["fbound_claim"], ["AREA", "Shape_Area", "Shape_Length", "Shape_Leng", "DOC_ID", "ORI_CODE", "LEN"])

            count_claims = get_count(ktdata["misc"]["fbound_claim"])

            mdf(ktdata["misc"]["fbound_claim"], importance='!')
            arcpy.FeatureClassToFeatureClass_conversion(claiminpath, mdb(), ktdata["misc"]["diekdikisi"])

            pm("\nDONE ! - Forest claiming {} KAEK. Don't forget to change AREAFOREST to AREA_FOREST\n".format(count_claims))

            log('Create FBOUND Claims', count_claims)
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")

    @staticmethod
    def pre_fbound():
        if status.check('SHAPE', "ASTOTA"):
            # Dhmiourgia tou sunolikoy PRE_FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis([gdbm(ktdata["merge"]["astota"]), predasinpath], gdbm(ktdata["misc"]["gdb_pre_fbound_all"]), output_type="INPUT")
            arcpy.DeleteField_management(gdbm(ktdata["misc"]["gdb_pre_fbound_all"]), ["FID_merge_ASTOTA", "FID_KYR_PO_PARCELS", "KATHGORDX", "KATHGORAL1", "AREA", "LEN", "CAD_ADMIN"])
            arcpy.FeatureClassToFeatureClass_conversion(gdbm(ktdata["misc"]["gdb_pre_fbound_all"]), fboundoutpath, ktdata["misc"]["pre_fbound_all"])

            turn_off()

            # Dhmiourgia pinaka PRE_FBOUND vasi ton prodiagrafon
            arcpy.DeleteField_management(prefboundinpath, ["Shape_Leng", "Shape_Area"])
            arcpy.AddField_management(prefboundinpath, "AREA", "DOUBLE")
            arcpy.AddField_management(prefboundinpath, "LEN", "DOUBLE")
            arcpy.AddField_management(prefboundinpath, "F_CODE", "SHORT", field_precision=1)
            arcpy.CalculateField_management(prefboundinpath, "F_CODE", "1", "PYTHON_9.3")
            arcpy.CalculateField_management(prefboundinpath, "AREA", "float(!shape.Area@UNKNOWN!)", "PYTHON_9.3")
            arcpy.CalculateField_management(prefboundinpath, "LEN", "float(!shape.Length@UNKNOWN!)", "PYTHON_9.3")

            pm("Exporting PRE_FBOUND / OTA")

            # Eksagogi PRE_FBOUND ana OTA
            general.export_per_ota(ktdata["misc"]["pre_fbound_all"], formal=True, name="FBOUND")

            mdf(ktdata["misc"]["pre_fbound_all"], importance='!')

            pm("\nDONE !\n")

            log('Create PRE_FBOUND')
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")


if get_pass():
    geoprocessing = Geoprocessing()
    find = Queries()
    general = General()
    check = Check()
    fix = Fix()
    fields = Fields()
    create = Create()
else:
    pass
