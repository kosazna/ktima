# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import csv
from organize import *


# Check - Approve
def ca(*args):
    checker = 0
    for shp in args:
        if not status[kt.mode].check('SHAPE', shp):
            pm('\n{} not Merged'.format(shp))
            checker += 1

    if not checker:
        return True
    else:
        pm('\n\n\n!! Task Aborted !!\n\n\n')
        return False


def clarify(feature):
    mxd_otas = set(i[-5:] for i in org[kt.mode].mxd_fl[feature]['list'])
    user_otas = set(kt.otas)

    end_otas = list(user_otas.intersection(mxd_otas))
    end_list = [r'{}\{}_{}'.format(feature.lower(),
                                   feature,
                                   ota) for ota in end_otas]

    return end_list


class Geoprocessing:
    def __init__(self, mode, standalone=False):
        self.mode = mode
        self.gdb = gdb[mode]
        self.standalone = standalone

    @mxd
    def merge(self, shapes, force_merge=False, _roads='old'):
        log_list = []

        if not self.standalone:
            for _shape in shapes:
                if _shape == "ROADS":
                    shapefile = choose_roads(_roads)
                else:
                    shapefile = _shape

                if not status[self.mode].check('SHAPE',
                                               shapefile) or force_merge:
                    f_name = "merge_" + _shape

                    try:
                        arcpy.Merge_management(clarify(_shape),
                                               self.gdb(f_name))

                        pm("\nMerged {}\n".format(_shape))

                        status[self.mode].update('SHAPE', shapefile, True)
                        log_list.append(str(shapefile))
                    except RuntimeError:
                        pm("\n!!! {} source files missing !!!\n".format(_shape))
                else:
                    pm('\n{} already merged\n'.format(shapefile))

            if log_list:
                log("Merge Shapefiles", log_list=log_list)
        else:
            for _shape in shapes:
                if _shape == "ROADS":
                    shapefile = choose_roads(_roads)
                else:
                    shapefile = _shape

                f_name = "merge_" + _shape

                tomerge = [r'{}\{}_{}'.format(_shape.lower(),
                                              _shape,
                                              ota) for ota in kt.otas]
                try:
                    arcpy.Merge_management(tomerge, self.gdb(f_name))
                    status[self.mode].update('SHAPE', shapefile, True)
                    pm("\nMerged {}\n".format(_shape))
                except RuntimeError:
                    pm("\n!!! {} source files missing !!!\n".format(_shape))

    def union(self, shapes, precision=lut.precision,
              gaps=False):

        if gaps:
            _gaps = "GAPS"
        else:
            _gaps = "NO_GAPS"

        if not self.standalone:
            if shapes == "ALL":
                for shapefile in lut.merging_list:
                    pm("Union for {}\n".format(shapefile))

                    feature_name = "union_" + shapefile
                    arcpy.Union_analysis(
                        list(org[self.mode].mxd_fl[shapefile]['list']),
                        self.gdb(feature_name),
                        "NO_FID",
                        precision,
                        _gaps)

                log("Union Shapefiles")
            else:
                for shape in shapes:
                    feature_name = "union_" + shape
                    arcpy.Union_analysis(
                        clarify(shape),
                        self.gdb(feature_name),
                        "NO_FID",
                        precision,
                        _gaps)
        else:
            for shape in shapes:
                feature_name = "union_" + shape

                to_union = [r'{}\{}_{}'.format(shape.lower(),
                                               shape,
                                               ota) for ota in kt.otas]

                arcpy.Union_analysis(to_union,
                                     self.gdb(feature_name),
                                     "NO_FID",
                                     precision,
                                     _gaps)

    def export_to_server(self, copy_files, plus_name):
        pm('\n\n')

        _path = os.path.join(paths.checks_out,
                             time.strftime("%Y-%m-%d_%H%M") + '_' + plus_name)

        if not os.path.exists(_path):
            os.mkdir(_path)

        for shp in copy_files:
            try:
                arcpy.FeatureClassToFeatureClass_conversion(self.gdb(shp),
                                                            _path,
                                                            shp)

                pm('Exported {} from {}.gdb'.format(shp, plus_name))

            except RuntimeError:
                pm('Dataset {} does not exist'.format(shp))

        pm('\nDone !\n')


class Queries:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]
        self.astik = self.gdb(lut.astikM)
        self.dbound_fc = self.gdb(lut.dboundM)
        self.pst_fc = self.gdb(lut.pstM)

    def kaek_in_dbound(self):
        arcpy.Intersect_analysis([self.gdb(self.pst_fc),
                                  self.gdb(self.dbound_fc)],
                                 self.gdb(lut.kaek_in_dbound),
                                 output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(lut.kaek_in_dbound))

    def kaek_in_astik(self):
        arcpy.Intersect_analysis([self.gdb(self.pst_fc), self.gdb(self.astik)],
                                 self.gdb(lut.kaek_in_astik),
                                 output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(lut.kaek_in_astik))

    def rd(self):
        org[self.mode].add_layer([self.pst_fc])
        arcpy.SelectLayerByAttribute_management(self.pst_fc,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0701' ")
        arcpy.CopyFeatures_management(self.pst_fc, self.gdb(lut.rd))
        pm('\nDONE !  -->  {}\n'.format(lut.rd))

    def pr(self):
        org[self.mode].add_layer([self.pst_fc])
        arcpy.SelectLayerByAttribute_management(self.pst_fc,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0702' ")
        arcpy.CopyFeatures_management(self.pst_fc, self.gdb(lut.pr))
        pm('\nDONE !  -->  {}\n'.format(lut.pr))

    def find_identical(self, what, in_what, export=False):
        if isinstance(what, list):
            _what = what
        else:
            _what = [what]

        to_merge = []

        pm('\n')

        for shp in _what:
            arcpy.SelectLayerByLocation_management(shp,
                                                   "ARE_IDENTICAL_TO", in_what)
            identical = get_count(shp)
            clear_selection(shp)
            all_rows = get_count(shp)
            percentage = round((identical / float(all_rows)) * 100, 1)

            if percentage:
                to_merge.append(shp)

            pm('{:<20}: {:<6}/{:<6} are identical / {:<5} %'.format(shp,
                                                                    identical,
                                                                    all_rows,
                                                                    percentage))
            pm('--------------------------------------------------------------')

        if export:
            for shp in _what:
                arcpy.SelectLayerByLocation_management(
                    shp,
                    "ARE_IDENTICAL_TO",
                    in_what,
                    selection_type="ADD_TO_SELECTION")

            arcpy.Merge_management(to_merge, self.gdb('identical'))

        pm('\nDone!\n')


class General:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def isolate(self, fc):
        if ca('ASTOTA'):
            org[self.mode].add_layer([lut.astotaM])

            arcpy.Dissolve_management(lut.astotaM, self.gdb(lut.oria_etairias))

            fc_n = "{}_{}".format(lut.company_name, fc)
            arcpy.Intersect_analysis([fc, lut.oria_etairias],
                                     self.gdb(fc_n),
                                     output_type="INPUT")

            mdf(lut.oria_etairias, importance='!!')
            mdf(fc_n)

    @mxd
    def export_per_ota(self, fc, spatial, field='KAEK',
                       export_shp=True, database=False, formal=False,
                       name=None):

        def export(_fc, _ota):
            if export_shp:
                if database:
                    mdf(_fc, importance='!!', out='ota', ota=_ota)
                    fc_name = "{}_{}".format(_fc, _ota)
                    arcpy.CopyFeatures_management(fc, paths.mdb(fc_name))
                elif formal:
                    mdf(fc, out='formal', ota=ota, _name=name)
                else:
                    mdf(_fc, importance='!!', out='ota', ota=_ota)
            else:
                fc_name = "{}_{}".format(_fc, _ota)
                arcpy.CopyFeatures_management(_fc, self.gdb(fc_name))

        if spatial:
            for lyr_astota in org[self.mode].available('ASTOTA'):
                ota = str(lyr_astota[-5:])
                if ota in kt.otas:
                    arcpy.SelectLayerByLocation_management(fc,
                                                           'WITHIN',
                                                           lyr_astota)

                    if get_count(fc) != 0:
                        export(fc, ota)
                        clear_selection(fc)
        else:
            arcpy.AddField_management(fc, "_OTA_", "TEXT", field_length=5)
            arcpy.CalculateField_management(fc,
                                            "_OTA_",
                                            '!{}![:5]'.format(field),
                                            "PYTHON_9.3")

            for ota in kt.otas:
                arcpy.SelectLayerByAttribute_management(
                    fc,
                    "NEW_SELECTION",
                    " _OTA_ = '{}' ".format(ota))

                if get_count(fc) != 0:
                    export(fc, ota)
                    clear_selection(fc)


class Check:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    @mxd
    def shapes(self, x):
        if ca('PST', 'ASTTOM', 'ASTENOT'):

            precision = float(10 ** -x)
            precision_txt = '{:.{}f} m'.format(precision, x)

            pm("\nCheck accuracy : {}\n".format(precision_txt))

            pm("\nProcessing...")

            # geoprocessing

            geoprocessing[self.mode].union(['PST', 'ASTENOT', 'ASTTOM'],
                                           precision,
                                           gaps=False)

            turn_off()
            org[self.mode].add_layer([lut.pstM, lut.astenotM, lut.asttomM])

            # ENOTHTES
            arcpy.AddField_management(lut.astenotM, "ENOT", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lut.astenotM, "ENOT",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            # TOMEIS
            arcpy.AddField_management(lut.asttomM, "TOM", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lut.asttomM, "TOM",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            arcpy.SpatialJoin_analysis(lut.pstM, lut.astenotM,
                                       self.gdb(lut.pst_astenot),
                                       match_option='WITHIN')
            arcpy.SpatialJoin_analysis(lut.astenotM, lut.asttomM,
                                       self.gdb(lut.astenot_asttom),
                                       match_option='WITHIN')

            turn_off()

            arcpy.AddField_management(lut.pst_astenot, "pstENOT", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(lut.pst_astenot, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lut.pst_astenot, "PSTenot",
                                            '!KAEK![:9]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lut.pst_astenot, "matches",
                                            'bool(!CAD_ADMIN!==!pstENOT!)',
                                            "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(
                lut.pst_astenot,
                "NEW_SELECTION",
                " matches = '0' and pstENOT not like '%ΕΚ%' ")
            arcpy.CopyFeatures_management(lut.pst_astenot,
                                          self.gdb(lut.p_pst_astenot))

            arcpy.AddField_management(lut.astenot_asttom, "enotTOM", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(lut.astenot_asttom, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lut.astenot_asttom,
                                            "enotTOM",
                                            '!ENOT![:7]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lut.astenot_asttom,
                                            "matches",
                                            'bool(!TOM!==!enotTOM!)',
                                            "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(lut.astenot_asttom,
                                                    "NEW_SELECTION",
                                                    " matches = '0' ")
            arcpy.CopyFeatures_management(lut.astenot_asttom,
                                          self.gdb(lut.p_astenot_asttom))

            # Problem count
            count_pst_u = get_count(lut.pstU)
            count_pst_m = get_count(lut.pstM)
            diff_pst = count_pst_u - count_pst_m
            count_astenot_u = get_count(lut.astenotU)
            count_astenot_m = get_count(lut.astenotM)
            diff_astenot = count_astenot_u - count_astenot_m
            count_asttom_u = get_count(lut.asttomU)
            count_asttom_m = get_count(lut.asttomM)
            diff_asttom = count_asttom_u - count_asttom_m
            count_pst_astenot = get_count(lut.p_pst_astenot)
            count_astenot_asttom = get_count(lut.p_astenot_asttom)

            if count_astenot_m != count_astenot_u:
                arcpy.SelectLayerByAttribute_management(
                    lut.astenotU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(
                        count_astenot_m))
                arcpy.CopyFeatures_management(lut.astenotU,
                                              self.gdb(lut.p_overlaps_astenot))

            if count_asttom_m != count_asttom_u:
                arcpy.SelectLayerByAttribute_management(
                    lut.asttomU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_asttom_m))
                arcpy.CopyFeatures_management(lut.asttomU,
                                              self.gdb(lut.p_overlaps_asttom))

            if count_pst_m != count_pst_u:
                arcpy.SelectLayerByAttribute_management(
                    lut.pstU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_pst_m))
                arcpy.CopyFeatures_management(lut.pstU,
                                              self.gdb(lut.p_overlaps_pst))

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
                pm('! Lathos KAEK se ENOTITA ! - [{}]'.format(
                    count_pst_astenot))

            if count_astenot_asttom == 0:
                pm('ASTENOT me ASTTOM - OK\n')
            else:
                pm('! Lathos KAEK se TOMEA ! - [{}]\n'.format(
                    count_astenot_asttom))

            time_now = timestamp()

            log("Check Shapefiles", log_shapes)
            status[self.mode].update("OVERLAPS", "DECIMALS", precision_txt)
            status[self.mode].update("OVERLAPS", "CD", time_now)
            status[self.mode].update("OVERLAPS", "ASTENOT", diff_astenot)
            status[self.mode].update("OVERLAPS", "ASTTOM", diff_asttom)
            status[self.mode].update("OVERLAPS", "PST", diff_pst)
            status[self.mode].update("WRONG_KAEK", "ASTENOT_ASTTOM",
                                     count_astenot_asttom)
            status[self.mode].update("WRONG_KAEK", "PST_ASTENOT",
                                     count_pst_astenot)

    def pst_geometry(self):
        if ca('PST'):
            org[self.mode].add_layer([lut.pstM])
            turn_off()

            arcpy.CheckGeometry_management(lut.pstM, self.gdb(lut.pst_geom))

            count_geom = get_count(lut.pst_geom)
            problematic_set = set()
            problematic = []

            # Elegxos gia to an uparxoun self_intersections kai
            # apomonosi ton provlimatikon KAEK
            if count_geom == 0:
                pm("\nGEOMETRY OK - NO SELF INTERSECTIONS.\n")
            else:
                pm("\n{} SELF INTERSECTIONS.\n".format(count_geom))
                pm("Processing...\n")
                arcpy.AddJoin_management(lut.pstM, "OBJECTID", lut.pst_geom,
                                         "FEATURE_ID", "KEEP_COMMON")
                arcpy.CopyFeatures_management(lut.pstM,
                                              self.gdb(lut.p_geometry_kaek))
                clear_selection(lut.pstM)
                arcpy.AddField_management(lut.p_geometry_kaek, "OTA", "TEXT",
                                          field_length=5)
                arcpy.CalculateField_management(lut.p_geometry_kaek, "OTA",
                                                '!merge_PST_KAEK![:5]',
                                                "PYTHON_9.3")
                arcpy.Dissolve_management(lut.p_geometry_kaek,
                                          self.gdb(lut.p_geometry_ota), "OTA")
                cursor = arcpy.UpdateCursor(lut.p_geometry_ota)

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

            status[self.mode].update("SHAPES_GEOMETRY", "PROBS",
                                     bool(count_geom))
            status[self.mode].update("SHAPES_GEOMETRY", "CD", time_now)
            status[self.mode].update("SHAPES_GEOMETRY", "OTA", problematic)

            pm("\nDONE !\n")

            log('Check PST Geometry', log_geometry)

    @mxd
    def fbound_geometry(self):
        if status[self.mode].check('EXPORTED', "FBOUND"):
            try:
                arcpy.CheckGeometry_management(clarify('FBOUND'),
                                               self.gdb(lut.fbound_geom))

                count_geom = get_count(lut.fbound_geom)
                problematic_set = set()
                problematic = []

                # Elegxos gia to an uparxoun self_intersections
                # kai apomonosi ton provlimatikon KAEK
                if count_geom == 0:
                    pm("\nGEOMETRY OK - NO SELF INTERSECTIONS IN FBOUND.\n")
                else:
                    arcpy.AddField_management(lut.fbound_geom, "OTA", "TEXT",
                                              field_length=5)
                    arcpy.CalculateField_management(lut.fbound_geom,
                                                    "OTA",
                                                    '!CLASS![-5:]',
                                                    "PYTHON_9.3")
                    pm("\n{} SELF INTERSECTIONS IN FBOUND.\n".format(
                        count_geom))

                    cursor = arcpy.UpdateCursor(lut.fbound_geom)
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

                status[self.mode].update("FBOUND_GEOMETRY", "PROBS",
                                         bool(count_geom))
                status[self.mode].update("FBOUND_GEOMETRY", "CD", time_now)
                status[self.mode].update("FBOUND_GEOMETRY", "OTA", problematic)

                log('Check FBOUND Geometry', log_fbound_geometry)
            except RuntimeError:
                pm("\n!!! {} source files missing !!!\n".format('FBOUND'))
        else:
            raise Exception(
                "\n\n\n!!! Den exeis vgalei kainouria FBOUND !!!\n\n\n")

    def roads(self, _roads='old'):
        roads = choose_roads(_roads)

        if ca('PST', 'ASTENOT', roads):
            org[self.mode].add_layer([lut.pstM, lut.roadsM, lut.astenotM])

            # Eksagwgh kai enosi eidikwn ektasewn
            arcpy.SelectLayerByAttribute_management(lut.pstM,
                                                    "NEW_SELECTION",
                                                    " PROP_TYPE = '0701' ")
            arcpy.CopyFeatures_management(lut.pstM, self.gdb(lut.ek))
            clear_selection(lut.pstM)
            arcpy.Dissolve_management(lut.ek, self.gdb(lut.temp_ek),
                                      "PROP_TYPE")

            # Elegxos gia aksones ektos EK
            arcpy.Intersect_analysis([lut.roadsM, lut.temp_ek],
                                     self.gdb(lut.intersections_roads),
                                     output_type="POINT")
            arcpy.DeleteField_management(lut.intersections_roads, "PROP_TYPE")

            # Elegxos gia aksones pou mporei na kovoun thn idia enotita
            arcpy.SpatialJoin_analysis(lut.intersections_roads, lut.pstM,
                                       self.gdb(lut.intersections_pst_rd),
                                       match_option="CLOSEST")
            arcpy.SelectLayerByAttribute_management(lut.intersections_pst_rd,
                                                    "NEW_SELECTION",
                                                    " PROP_TYPE = '0101' ")
            arcpy.SpatialJoin_analysis(lut.intersections_pst_rd,
                                       lut.astenotM,
                                       self.gdb(lut.intersections_astenot_rd))

            count_inter_all = get_count(lut.intersections_roads)
            count_inter_astenot = get_count(lut.intersections_astenot_rd)

            if count_inter_astenot > 10:
                arcpy.Dissolve_management(lut.intersections_astenot_rd,
                                          self.gdb(lut.p_roads),
                                          "CAD_ADMIN", "CAD_ADMIN COUNT")
            else:
                arcpy.SpatialJoin_analysis(lut.intersections_pst_rd,
                                           lut.astenotM,
                                           self.gdb(lut.p_roads))

            log_roads = [count_inter_all,
                         count_inter_astenot]

            if count_inter_all == 0:
                pm("\nROADS - OK\n")
            else:
                pm("\nROADS intersections - [{}]".format(count_inter_all))
                pm("ROADS intersections me ASTENOT - [{}].\n".format(
                    count_inter_astenot))

            time_now = timestamp()

            log('Check ROADS', log_roads)
            status[self.mode].update("ROADS", "ALL", count_inter_all)
            status[self.mode].update("ROADS", "PROBS", count_inter_astenot)
            status[self.mode].update("ROADS", "CD", time_now)
            status[self.mode].update("ROADS", "CPROBS", bool(count_inter_all))

    def dbound(self):
        if ca('DBOUND'):
            # Elegxos gia DBOUND pou mporei na toys leipei eite to
            # DEC_ID eite to DEC_DATE
            org[self.mode].add_layer([lut.dboundM])

            arcpy.SelectLayerByAttribute_management(lut.dboundM,
                                                    "NEW_SELECTION",
                                                    " DEC_ID = '' ")
            arcpy.SelectLayerByAttribute_management(lut.dboundM,
                                                    "ADD_TO_SELECTION",
                                                    " DEC_DATE IS NULL ")
            arcpy.CopyFeatures_management(lut.dboundM,
                                          self.gdb(lut.p_dbound))

            count_dbound = get_count(lut.p_dbound)

            if count_dbound == 0:
                pm("\nDBOUND - OK\n")
            else:
                pm("\n{} eggrafes den exoun DEC_ID / DEC_DATE.\n".format(
                    count_dbound))

            time_now = timestamp()

            log('Check DBOUND', count_dbound)
            status[self.mode].update("DBOUND", "PROBS", count_dbound)
            status[self.mode].update("DBOUND", "CD", time_now)

    def bld(self):
        if ca('BLD'):
            # Elegxos gia BLD pou mporei na exoun thn timh '0' eite
            # sto BLD_T_C eite sto BLD_NUM
            org[self.mode].add_layer([lut.bldM])

            arcpy.SelectLayerByAttribute_management(lut.bldM,
                                                    "NEW_SELECTION",
                                                    " BLD_T_C = 0 ")
            arcpy.SelectLayerByAttribute_management(lut.bldM,
                                                    "ADD_TO_SELECTION",
                                                    " BLD_NUM = 0 ")
            arcpy.CopyFeatures_management(lut.bldM, self.gdb(lut.temp_bld))
            arcpy.SpatialJoin_analysis(lut.temp_bld, self.gdb(lut.pstM),
                                       self.gdb(lut.p_bld),
                                       match_option='WITHIN')

            count_bld = get_count(lut.p_bld)

            if count_bld == 0:
                pm("\nBLD - OK\n")
            else:
                pm("\n{} eggrafes den exoun BLD_T_C / BLD_NUM.\n".format(
                    count_bld))

            time_now = timestamp()

            log('Check BLD', count_bld)
            status[self.mode].update("BLD", "PROBS", count_bld)
            status[self.mode].update("BLD", "CD", time_now)


class Fix:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def pst_geometry(self):
        if status[self.mode].check('SHAPES_GEOMETRY', "PROBS"):
            # Epilogi olon ton shapefile enos provlimatikou OTA kai
            # epidiorthosi tis geometrias tous
            _data = load_json(paths.status_path)

            repaired = []

            for row in _data["SHAPES_GEOMETRY"]["OTA"]:
                ota_folder = str(row)
                repaired.append(int(ota_folder))
                for i in lut.geometry_list:
                    lyr = paths.ktima(ota_folder, i, ext=True)

                    if arcpy.Exists(lyr):
                        pm("Repairing geometry in {}_{}".format(i, ota_folder))
                        arcpy.RepairGeometry_management(lyr, "KEEP_NULL")

            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix Geometry', repaired)

    def fbound_geometry(self):
        if status[self.mode].check('FBOUND_GEOMETRY', "PROBS"):
            # Epidiorthosi ton FBOUND
            _data = load_json(paths.status_path)

            repaired = []

            for row in _data["FBOUND_GEOMETRY"]["OTA"]:
                repair_ota = str(row)
                repaired.append(int(repair_ota))

                lyr = paths.ktima(repair_ota, "FBOUND", ext=True)

                if arcpy.Exists(lyr):
                    pm("Repairing geometry in FBOUND_{}".format(repair_ota))
                    arcpy.RepairGeometry_management(lyr, "DELETE_NULL")

            status[self.mode].update('SHAPE', 'FBOUND', False)
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix FBOUND Geometry', repaired)

    def roads(self):
        if status[self.mode].check("ROADS", "CPROBS"):
            # Kopsimo ton aksonon 10 cm prin to orio tis enotitas
            arcpy.Buffer_analysis(self.gdb(lut.temp_ek),
                                  self.gdb(lut.ek_fixed_bound),
                                  lut.ek_bound_reduction)
            arcpy.Clip_analysis(self.gdb(lut.roadsM),
                                self.gdb(lut.ek_fixed_bound),
                                self.gdb(lut.gdb_roads_all))

            status[self.mode].update("EXPORTED", "ROADS", False)

            log('Fix ROADS')
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")


class Fields:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    @mxd
    def pst(self):
        # Diorthosi ton pedion ORI_TYPE, DEC_ID kai ADDRESS stous PST
        # me vasi tis prodiagrafes
        for lyr_pst in org[self.mode].available('PST'):
            if lyr_pst[-5:] in kt.otas:
                pm("Processing {}".format(lyr_pst))
                arcpy.SelectLayerByAttribute_management(lyr_pst,
                                                        "NEW_SELECTION",
                                                        " ORI_CODE = '' ")
                arcpy.CalculateField_management(lyr_pst, "ORI_TYPE", '1',
                                                "PYTHON_9.3")
                arcpy.CalculateField_management(lyr_pst, "DEC_ID", "''",
                                                "PYTHON_9.3")
                arcpy.SelectLayerByAttribute_management(lyr_pst,
                                                        "NEW_SELECTION",
                                                        " ADDRESS = '' ")
                arcpy.CalculateField_management(lyr_pst, "ADDRESS",
                                                "'ΑΝΩΝΥΜΟΣ'",
                                                "PYTHON_9.3")

        pm("\nDONE !\n")

        log('Fields PST')

    @mxd
    def asttom(self):
        # Diagrafi ACQ_SCALE apo tous ASTTOM
        for lyr_asttom in org[self.mode].available('ASTTOM'):
            if lyr_asttom[-5:] in kt.otas:
                pm("Processing {}".format(lyr_asttom))
                arcpy.DeleteField_management(lyr_asttom, "ACQ_SCALE", )

        pm("\nDONE !\n")

        log('Fields ASTTOM')

    @mxd
    def astenot(self):
        # Prosthiki onomasias sto pedio LOCALITY ton ASTENOT me vasi txt arxeio
        available = org[self.mode].available('ASTENOT', ota_num=True)

        with open(paths.locality) as csvfile:
            localnames = csv.reader(csvfile)

            for row in localnames:
                try:
                    ota = row[0][:5]
                    if ota in available and ota in kt.otas:
                        lyr_astenot = "ASTENOT_{}".format(ota)
                        pm("Processing {}".format(lyr_astenot))
                        arcpy.SelectLayerByAttribute_management(
                            lyr_astenot,
                            "NEW_SELECTION",
                            " CAD_ADMIN LIKE '%{}%' ".format(row[0]))
                        arcpy.CalculateField_management(lyr_astenot,
                                                        "LOCALITY",
                                                        "'{}'".format(row[1]),
                                                        "PYTHON_9.3")
                        arcpy.SelectLayerByAttribute_management(
                            lyr_astenot,
                            "NEW_SELECTION",
                            " LOCALITY = '' ")
                        arcpy.CalculateField_management(lyr_astenot,
                                                        "LOCALITY",
                                                        "'{}'".format(row[2]),
                                                        "PYTHON_9.3")
                except IndexError:
                    pm("Leipei onomatologia gia {}".format(ota))

        pm("\nDONE !\n")

        log('Fields ASTENOT')


class Create:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def fbound(self):
        if ca('ASTOTA'):
            # Dhmiourgia tou sunolikou FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis([self.gdb(lut.astotaM),
                                      paths.dasinpath],
                                     self.gdb(lut.gdb_fbound_all),
                                     output_type="INPUT")
            arcpy.DeleteField_management(self.gdb(lut.gdb_fbound_all),
                                         ["FID_merge_ASTOTA", "FID_PO_PARCELS",
                                          "FIELD", "AREA", "LEN"])
            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lut.gdb_fbound_all),
                paths.fboundoutpath,
                lut.fbound_all)

            turn_off()

            # # Dhmiourgia pinaka FBOUND vasi ton prodiagrafon
            arcpy.DeleteField_management(paths.fboundinpath,
                                         ["Shape_Leng", "Shape_Area"])
            arcpy.AddField_management(paths.fboundinpath, "ORI_CODE", "SHORT",
                                      field_precision=1)
            arcpy.AddField_management(paths.fboundinpath, "DOC_ID", "TEXT",
                                      field_length=254)
            arcpy.AddField_management(paths.fboundinpath, "AREA", "DOUBLE")
            arcpy.AddField_management(paths.fboundinpath, "LEN", "DOUBLE")
            arcpy.CalculateField_management(paths.fboundinpath, "ORI_CODE", "1",
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.fboundinpath, "AREA",
                                            "float(!shape.Area@UNKNOWN!)",
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.fboundinpath, "LEN",
                                            "float(!shape.Length@UNKNOWN!)",
                                            "PYTHON_9.3")

            # Prosthiki DOC_ID sto pinaka me vasi txt arxeio
            with open(paths.fbounddoc) as csvfile:
                docs = csv.reader(csvfile)

                lyr_fbound = lut.fbound_all
                pm("Processing DOC_ID in {}".format(lyr_fbound))

                for row in docs:
                    try:
                        ota = row[0]
                        area = int(row[2]) * 2000
                        arcpy.SelectLayerByAttribute_management(
                            lyr_fbound,
                            "NEW_SELECTION",
                            " CAD_ADMIN LIKE '%{}%' AND AREA >= {} ".format(
                                ota, area))
                        arcpy.CalculateField_management(lyr_fbound,
                                                        "DOC_ID",
                                                        "'{}'".format(row[1]),
                                                        "PYTHON_9.3")
                    except IndexError:
                        pm("Leipei DOC_ID gia {} apo to .txt arxeio".format(
                            ota))

            arcpy.SelectLayerByAttribute_management(lut.fbound_all,
                                                    "NEW_SELECTION",
                                                    " DOC_ID = '' ")

            if get_count(lut.fbound_all) != 0:
                pm("\n !!! Leipoun DOC_ID apo to FBOUND_ALL \n!!!")

            clear_selection(lut.fbound_all)

            arcpy.DeleteField_management(lut.fbound_all, "CAD_ADMIN")

            pm("Exporting FBOUND / OTA")

            # Eksagogi FBOUND ana OTA
            general[self.mode].export_per_ota(lut.fbound_all,
                                              spatial=False, field='DOC_ID',
                                              formal=True,
                                              name="FBOUND")

            mdf(lut.fbound_all, importance='!')

            pm("\nDONE !\n")

            time_now = timestamp()

            status[self.mode].update("EXPORTED", "FBOUND", True)
            status[self.mode].update("SHAPE", "FBOUND", False)
            status[self.mode].update("EXPORTED", "FBOUND_ED", time_now)

            log('Create FBOUND')

    def roads(self):
        if status[self.mode].check("ROADS", "CPROBS") \
                and not status[self.mode].check("EXPORTED", "ROADS"):

            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lut.gdb_roads_all),
                paths.rdoutpath, lut.roads_all)

            # Dhmiourgia pinaka ROADS vasi ton prodiagrafon
            arcpy.DeleteField_management(paths.rdinpath,
                                         ["LEFTFROM", "LEFTTO", "RIGHTFROM",
                                          "RIGHTTO"])
            arcpy.AddField_management(paths.rdinpath, "LEFTFROM", "SHORT",
                                      field_precision=3)
            arcpy.AddField_management(paths.rdinpath, "LEFTTO", "SHORT",
                                      field_precision=3)
            arcpy.AddField_management(paths.rdinpath, "RIGHTFROM", "SHORT",
                                      field_precision=3)
            arcpy.AddField_management(paths.rdinpath, "RIGHTTO", "SHORT",
                                      field_precision=3)
            arcpy.AddField_management(paths.rdinpath, "L", "SHORT",
                                      field_precision=5)
            arcpy.AddField_management(paths.rdinpath, "R", "SHORT",
                                      field_precision=5)
            arcpy.CalculateField_management(paths.rdinpath, "L", '!LEFTTK!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "R", '!RIGHTTK!',
                                            "PYTHON_9.3")
            arcpy.DeleteField_management(paths.rdinpath, ["LEFTTK", "RIGHTTK"])
            arcpy.AddField_management(paths.rdinpath, "LEFTTK", "SHORT",
                                      field_precision=5)
            arcpy.AddField_management(paths.rdinpath, "RIGHTTK", "SHORT",
                                      field_precision=5)
            arcpy.CalculateField_management(paths.rdinpath, "LEFTTK", '!L!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "RIGHTTK", '!R!',
                                            "PYTHON_9.3")
            arcpy.DeleteField_management(paths.rdinpath, ["L", "R"])
            arcpy.AddField_management(paths.rdinpath, "L", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(paths.rdinpath, "R", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(paths.rdinpath, "S", "TEXT",
                                      field_length=254)
            arcpy.AddField_management(paths.rdinpath, "C", "DATE", )
            arcpy.CalculateField_management(paths.rdinpath, "L", '!LEFTMIN!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "R", '!RIGHTMIN!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "S", '!STREETNAME!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "C", '!COLLDATE!',
                                            "PYTHON_9.3")
            arcpy.DeleteField_management(paths.rdinpath, ["LEFTMIN", "RIGHTMIN",
                                                          "STREETNAME",
                                                          "COLLDATE",
                                                          "LEN", "Shape_Leng"])
            arcpy.AddField_management(paths.rdinpath, "LEFTMIN", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(paths.rdinpath, "RIGHTMIN", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(paths.rdinpath, "STREETNAME", "TEXT",
                                      field_length=254)
            arcpy.AddField_management(paths.rdinpath, "COLLDATE", "DATE")
            arcpy.CalculateField_management(paths.rdinpath, "LEFTMIN", '!L!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "RIGHTMIN", '!R!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "STREETNAME", '!S!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.rdinpath, "COLLDATE", '!C!',
                                            "PYTHON_9.3")
            arcpy.DeleteField_management(paths.rdinpath, ["L", "R", "S", "C"])
            arcpy.AddField_management(paths.rdinpath, "LEN", "DOUBLE")
            arcpy.CalculateField_management(paths.rdinpath, "LEN",
                                            "float(!shape.Length@UNKNOWN!)",
                                            "PYTHON_9.3")

            pm("\nExporting ROADS / OTA")

            # Eksagogi ROADS ana OTA
            general[self.mode].export_per_ota(lut.roads_all, spatial=True,
                                              formal=True,
                                              name="ROADS")

            mdf(lut.roads_all, importance='!')

            time_now = timestamp()

            status[self.mode].update("SHAPE", "ROADS", False)
            status[self.mode].update("EXPORTED", "ROADS", True)
            status[self.mode].update("EXPORTED", "ROADS_ED", time_now)

            log('Create ROADS')

            pm("\nDONE !\n")
        else:
            for fullpath, filename, basename, ext in list_dir(paths.old_roads,
                                                              match=['.shp',
                                                                     '.shx',
                                                                     '.dbf']):
                if basename == 'ROADS':
                    base = paths.new_roads.split('\\')[1:]
                    base += fullpath.split('\\')[4:]
                    outpath = cp(base)
                    c_copy(fullpath, outpath)

            status[self.mode].update("SHAPE", "ROADS", False)

            log('Copied iROADS to Local')

            pm("\nDONE !\n")

    def fboundclaim(self):
        if ca('PST', 'FBOUND'):
            # Dhmiourgia tou pinaka tis diekdikisis tou dasous
            arcpy.Intersect_analysis(
                [self.gdb(lut.pstM), self.gdb(lut.fboundM)],
                self.gdb(lut.intersection_pst_fbound),
                output_type="INPUT")
            arcpy.Dissolve_management(lut.intersection_pst_fbound,
                                      self.gdb(lut.gdb_fbound_claim),
                                      ["KAEK", "AREA"])
            arcpy.FeatureClassToFeatureClass_conversion(lut.gdb_fbound_claim,
                                                        paths.claimoutpath,
                                                        lut.fbound_claim)

            turn_off()

            # Diagrafi eggrafon vasi tupikon prodiagrafon
            arcpy.SelectLayerByAttribute_management(lut.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " Shape_Area < 100 ")
            # Svinontai oles oi eggrafes kato apo 100 m2
            arcpy.DeleteRows_management(lut.fbound_claim)
            clear_selection(lut.fbound_claim)
            arcpy.AddField_management(lut.fbound_claim, "AREA_MEAS", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(lut.fbound_claim, "AREAFOREST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(lut.fbound_claim, "AREA_REST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.CalculateField_management(lut.fbound_claim, "AREA_MEAS",
                                            '!AREA!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lut.fbound_claim, "AREAFOREST",
                                            '!Shape_Area!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lut.fbound_claim, "AREA_REST",
                                            '!AREA_MEAS! - !AREAFOREST!',
                                            "PYTHON_9.3")
            arcpy.AddField_management(lut.fbound_claim, "TYPE", "SHORT",
                                      field_precision=1)
            arcpy.SelectLayerByAttribute_management(lut.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " AREA_REST < 1 ")
            # Oles oi eggrafes me AREA_REST kato apo 1 m2  diekdikountai pliros
            arcpy.CalculateField_management(lut.fbound_claim, "AREA_REST", '0',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lut.fbound_claim, "TYPE", '1',
                                            "PYTHON_9.3")
            clear_selection(lut.fbound_claim)
            arcpy.DeleteField_management(lut.fbound_claim,
                                         ["AREA", "Shape_Area", "Shape_Length",
                                          "Shape_Leng", "DOC_ID", "ORI_CODE",
                                          "LEN"])

            count_claims = get_count(lut.fbound_claim)

            mdf(lut.fbound_claim, importance='!')
            arcpy.FeatureClassToFeatureClass_conversion(paths.claiminpath,
                                                        paths.mdb(),
                                                        lut.diekdikisi)

            pm(
                "\nDONE ! - Forest claiming {} KAEK.\n\n"
                "Don't forget to change AREAFOREST to AREA_FOREST\n".format(
                    count_claims))

            log('Create FBOUND Claims', count_claims)

            pm("\nDONE !\n")

    def pre_fbound(self):
        if ca('ASTOTA'):
            # Dhmiourgia tou sunolikoy PRE_FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis(
                [self.gdb(lut.astotaM), paths.predasinpath],
                self.gdb(lut.gdb_pre_fbound_all),
                output_type="INPUT")
            arcpy.DeleteField_management(self.gdb(lut.gdb_pre_fbound_all),
                                         ["FID_merge_ASTOTA",
                                          "FID_KYR_PO_PARCELS", "KATHGORDX",
                                          "KATHGORAL1", "AREA", "LEN",
                                          "CAD_ADMIN"])
            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lut.gdb_pre_fbound_all),
                paths.fboundoutpath,
                lut.pre_fbound_all)

            turn_off()

            # Dhmiourgia pinaka PRE_FBOUND vasi ton prodiagrafon
            arcpy.DeleteField_management(paths.prefboundinpath,
                                         ["Shape_Leng", "Shape_Area"])
            arcpy.AddField_management(paths.prefboundinpath, "AREA", "DOUBLE")
            arcpy.AddField_management(paths.prefboundinpath, "LEN", "DOUBLE")
            arcpy.AddField_management(paths.prefboundinpath, "F_CODE", "SHORT",
                                      field_precision=1)
            arcpy.CalculateField_management(paths.prefboundinpath, "F_CODE",
                                            "1",
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.prefboundinpath, "AREA",
                                            "float(!shape.Area@UNKNOWN!)",
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(paths.prefboundinpath, "LEN",
                                            "float(!shape.Length@UNKNOWN!)",
                                            "PYTHON_9.3")

            pm("Exporting PRE_FBOUND / OTA")

            # Eksagogi PRE_FBOUND ana OTA
            general[self.mode].export_per_ota(lut.pre_fbound_all,
                                              spatial=True, formal=True,
                                              name="FBOUND")

            mdf(lut.pre_fbound_all, importance='!')

            pm("\nDONE !\n")

            log('Create PRE_FBOUND')
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")


geoprocessing = {ktima_m: Geoprocessing(ktima_m),
                 standalone_m: Geoprocessing(standalone_m, standalone=True)}
find = {ktima_m: Queries(ktima_m),
        standalone_m: Queries(standalone_m)}
general = {ktima_m: General(ktima_m),
           standalone_m: General(standalone_m)}
check = {ktima_m: Check(ktima_m),
         standalone_m: Check(standalone_m)}
fix = {ktima_m: Fix(ktima_m),
       standalone_m: Fix(standalone_m)}
fields = {ktima_m: Fields(ktima_m),
          standalone_m: Fields(standalone_m)}
create = {ktima_m: Create(ktima_m),
          standalone_m: Create(standalone_m)}
