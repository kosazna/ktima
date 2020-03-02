# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module contains all the core functionality of ktima project.

import csv
from organize import *


def ktima_status(*args):
    """
    Checks whether or not shapefiles are merged so that
    operations can performed more quickly.

    :param args: **str**
        Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
    :return: **boolean**
        True if shapefiles are merged, False otherwise
    """

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


def available(feature):
    """
    Determines which for which otas shapefiles can be merged
    based on their availability and USER command

    :param feature: **str**
        Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
    :return: **list**
        List of otas
    """

    mxd_otas = set(i[-5:] for i in org[kt.mode].mxd_fl[feature]['list'])
    user_otas = set(kt.otas)

    end_otas = list(user_otas.intersection(mxd_otas))
    end_list = [r'{}\{}_{}'.format(feature.lower(),
                                   feature,
                                   ota) for ota in end_otas]

    return end_list


class Geoprocessing:
    """
    Geoprecessing class has all the functions for preprocessing large datasets
    in order to be ready for further testing

    Attributes
    ----------
    - mode: mode for the session (ktima or standalone)
    - gdb: geotabase function given from dictionary
    - standalone: boolean for whether or not it's a standalone session

    Methods
    -------
    - merge
    - union
    """

    def __init__(self, mode, standalone=False):
        self.mode = mode
        self.gdb = gdb[mode]
        self.standalone = standalone

    @mxd
    def merge(self, shapes, force_merge=False, _roads='old'):
        """
        ArcGIS automation to merge shapefiles

        :param shapes: **str**
            Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
        :param force_merge: **boolean**, optional
            Whether or not shapefiles will be merged even if they
            are already merged (default: False)
        :param _roads: **str**, optional
            Which roads will be used for merging. Parameter is passed
            to choose_roads function (default: 'old')
        :return: nothing
        """

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
                        arcpy.Merge_management(available(_shape),
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

    def union(self, shapes, precision=lui.precision,
              gaps=False):
        """
        ArcGIS automation for performing Union in shapefiles

        :param shapes: **str**
            Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
        :param precision: **float**, optional
            Float number passed to "Union" in ArcGIS
            (default is defined in a json file)
        :param gaps: **boolean**, optional
            Whether or not "Union" will be performed with gaps
            (default is False)
        :return: Nothing
        """

        if gaps:
            _gaps = "GAPS"
        else:
            _gaps = "NO_GAPS"

        if not self.standalone:
            if shapes == "ALL":
                for shapefile in lui.merging_list:
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
                        available(shape),
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


class Queries:
    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def kaek_in_dbound(self):
        arcpy.Intersect_analysis([self.gdb(lui.pstM),
                                  self.gdb(lui.dboundM)],
                                 self.gdb(lui.kaek_in_dbound),
                                 output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(lui.kaek_in_dbound))

    def kaek_in_astik(self):
        arcpy.Intersect_analysis([self.gdb(lui.pstM), self.gdb(lui.astikM)],
                                 self.gdb(lui.kaek_in_astik),
                                 output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(lui.kaek_in_astik))

    def rd(self):
        org[self.mode].add_layer([lui.pstM])
        arcpy.SelectLayerByAttribute_management(lui.pstM,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0701' ")
        arcpy.CopyFeatures_management(lui.pstM, self.gdb(lui.rd))
        pm('\nDONE !  -->  {}\n'.format(lui.rd))

    def pr(self):
        org[self.mode].add_layer([lui.pstM])
        arcpy.SelectLayerByAttribute_management(lui.pstM,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0702' ")
        arcpy.CopyFeatures_management(lui.pstM, self.gdb(lui.pr))
        pm('\nDONE !  -->  {}\n'.format(lui.pr))

    def advanced_query(self, q_type='KAEK', q_content='ASTIK'):
        pass

    def find_identical(self, what, in_what, export=False):
        """
        Find identical parcels between two shspefiles and prints statistics

        :param what: **str**, **list**
            Shapefile or feature layer
        :param in_what: **str**
            Shapefile or feature layer
        :param export: **boolean**
            Whether or not a shapefile with the common parcels will be exported
            (default: False)
        :return: Nothing
        """

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
    """
    General Tasks

    Methods
    -------
    - isolate
    - export_per_ota
    - export_to_server
    """

    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def isolate(self, fc):
        """
        Isolate Features in the area of interest

        :param fc: **str**
            Feature class or shapefile
        :return: Nothing
        """

        if ktima_status('ASTOTA'):
            org[self.mode].add_layer([lui.astotaM])

            arcpy.Dissolve_management(lui.astotaM, self.gdb(lui.oria_etairias))

            fc_n = "{}_{}".format(lui.company_name, fc)
            arcpy.Intersect_analysis([fc, lui.oria_etairias],
                                     self.gdb(fc_n),
                                     output_type="INPUT")

            mdf(lui.oria_etairias, importance='!!')
            mdf(fc_n)

    @mxd
    def export_per_ota(self, fc, spatial, field='KAEK',
                       export_shp=True, database=False, formal=False,
                       name=None):
        """
        Given a shapefile it will export the features that intersect with
        a specific ota as a new shapefile.

        :param fc: **str**
            Shapefile or feature class.
        :param spatial: **bollean**
            If True the selection will be based on spatial location
            If False the selection will be bases on an attribute. Field
            parameter is required when set to False.
        :param field: **str**, optional
            Field of the shapefile attribute table that the selection will
            be based on (default: 'KAEK')
        :param export_shp: **bollean**, optional
            If True, shapefiles for each ota
             will be exported in this folder (OutputData\\Shapefile\\!!OTA).
            If False, feature classes will be exported for each ota in gdb.
            (default: True)
        :param database: **bollean**, optional
            If True, mdbs will be also exported in archive.mdb
            If False, no mdbs will be made.
            (default: False)
        :param formal: **bollean**, optional
            If True formal export will be executed based on formal mdf function
             parameter.
            If False, shapefiles for each ota
             will be exported in this folder (OutputData\\Shapefile\\!!OTA).
             (default: False)
        :param name: **str**, optional
            Name for the shapefile that will be exported. (default: None)
        :return: Nothing
        """

        def export(_fc, _ota):
            if export_shp:
                if database:
                    mdf(_fc, importance='!!', out='ota', ota=_ota)
                    fc_name = "{}_{}".format(_fc, _ota)
                    arcpy.CopyFeatures_management(fc, paths.mdb(fc_name))
                elif formal:
                    mdf(fc, out='formal', ota=ota, name=name)
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

    def export_to_server(self, copy_files, plus_name):
        """
        Export generated shapefiles to company server

        :param copy_files: **str**
            Shapefile to export
        :param plus_name: **str**
            suffix added to folder. Usually it is the kt.mode
        :return: Nothing
        """

        _path = os.path.join(paths.checks_out,
                             time.strftime("%Y-%m-%d_%H%M") + '_' + plus_name)

        if not os.path.exists(_path):
            os.mkdir(_path)

        pm('\n\n')

        for shp in copy_files:
            try:
                arcpy.FeatureClassToFeatureClass_conversion(self.gdb(shp),
                                                            _path,
                                                            shp)

                pm('Exported {} from {}.gdb'.format(shp, plus_name))

            except RuntimeError:
                pm('Dataset {} does not exist'.format(shp))

        pm('\nDone !\n')


class Check:
    """
    Check class has all the basic check functions for the shapefiles.

    Methods
    -------
    - shapes
    - pst_geometry
    - fbound_geometry
    - roads
    - bld
    - dbound
    """

    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    @mxd
    def shapes(self, accuracy):
        """
        Checks for overlaps and wrong numbering.

        :param accuracy: **int**
            Precision which will be used in 'union'.
        :return: Nothing
        """

        if ktima_status('PST', 'ASTTOM', 'ASTENOT'):

            precision = float(10 ** -accuracy)
            precision_txt = '{:.{}f} m'.format(precision, accuracy)

            pm("\nCheck accuracy : {}\n".format(precision_txt))

            pm("\nProcessing...")

            # GEOPROCESSING

            geoprocessing[self.mode].union(['PST', 'ASTENOT', 'ASTTOM'],
                                           precision,
                                           gaps=False)

            turn_off()
            org[self.mode].add_layer([lui.pstM, lui.astenotM, lui.asttomM])

            # ENOTITES
            arcpy.AddField_management(lui.astenotM, "ENOT", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lui.astenotM, "ENOT",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            # TOMEIS
            arcpy.AddField_management(lui.asttomM, "TOM", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lui.asttomM, "TOM",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            arcpy.SpatialJoin_analysis(lui.pstM, lui.astenotM,
                                       self.gdb(lui.pst_astenot),
                                       match_option='WITHIN')
            arcpy.SpatialJoin_analysis(lui.astenotM, lui.asttomM,
                                       self.gdb(lui.astenot_asttom),
                                       match_option='WITHIN')

            turn_off()

            arcpy.AddField_management(lui.pst_astenot, "pstENOT", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(lui.pst_astenot, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lui.pst_astenot, "PSTenot",
                                            '!KAEK![:9]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lui.pst_astenot, "matches",
                                            'bool(!CAD_ADMIN!==!pstENOT!)',
                                            "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(
                lui.pst_astenot,
                "NEW_SELECTION",
                " matches = '0' and pstENOT not like '%ΕΚ%' ")
            arcpy.CopyFeatures_management(lui.pst_astenot,
                                          self.gdb(lui.p_pst_astenot))

            arcpy.AddField_management(lui.astenot_asttom, "enotTOM", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(lui.astenot_asttom, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(lui.astenot_asttom,
                                            "enotTOM",
                                            '!ENOT![:7]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lui.astenot_asttom,
                                            "matches",
                                            'bool(!TOM!==!enotTOM!)',
                                            "PYTHON_9.3")
            arcpy.SelectLayerByAttribute_management(lui.astenot_asttom,
                                                    "NEW_SELECTION",
                                                    " matches = '0' ")
            arcpy.CopyFeatures_management(lui.astenot_asttom,
                                          self.gdb(lui.p_astenot_asttom))

            # Problem count
            count_pst_u = get_count(lui.pstU)
            count_pst_m = get_count(lui.pstM)
            diff_pst = count_pst_u - count_pst_m
            count_astenot_u = get_count(lui.astenotU)
            count_astenot_m = get_count(lui.astenotM)
            diff_astenot = count_astenot_u - count_astenot_m
            count_asttom_u = get_count(lui.asttomU)
            count_asttom_m = get_count(lui.asttomM)
            diff_asttom = count_asttom_u - count_asttom_m
            count_pst_astenot = get_count(lui.p_pst_astenot)
            count_astenot_asttom = get_count(lui.p_astenot_asttom)

            if count_astenot_m != count_astenot_u:
                arcpy.SelectLayerByAttribute_management(
                    lui.astenotU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(
                        count_astenot_m))
                arcpy.CopyFeatures_management(lui.astenotU,
                                              self.gdb(lui.p_overlaps_astenot))

            if count_asttom_m != count_asttom_u:
                arcpy.SelectLayerByAttribute_management(
                    lui.asttomU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_asttom_m))
                arcpy.CopyFeatures_management(lui.asttomU,
                                              self.gdb(lui.p_overlaps_asttom))

            if count_pst_m != count_pst_u:
                arcpy.SelectLayerByAttribute_management(
                    lui.pstU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_pst_m))
                arcpy.CopyFeatures_management(lui.pstU,
                                              self.gdb(lui.p_overlaps_pst))

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
        """
        Checks for self intersection in PST_merge.

        :return: Nothing
        """

        if ktima_status('PST'):
            org[self.mode].add_layer([lui.pstM])
            turn_off()

            arcpy.CheckGeometry_management(lui.pstM, self.gdb(lui.pst_geom))

            count_geom = get_count(lui.pst_geom)
            problematic_set = set()
            problematic = []

            # Elegxos gia to an uparxoun self_intersections kai
            # apomonosi ton provlimatikon KAEK
            if count_geom == 0:
                pm("\nGEOMETRY OK - NO SELF INTERSECTIONS.\n")
            else:
                pm("\n{} SELF INTERSECTIONS.\n".format(count_geom))
                pm("Processing...\n")
                arcpy.AddJoin_management(lui.pstM, "OBJECTID", lui.pst_geom,
                                         "FEATURE_ID", "KEEP_COMMON")
                arcpy.CopyFeatures_management(lui.pstM,
                                              self.gdb(lui.p_geometry_kaek))
                clear_selection(lui.pstM)
                arcpy.AddField_management(lui.p_geometry_kaek, "OTA", "TEXT",
                                          field_length=5)
                arcpy.CalculateField_management(lui.p_geometry_kaek, "OTA",
                                                '!merge_PST_KAEK![:5]',
                                                "PYTHON_9.3")
                arcpy.Dissolve_management(lui.p_geometry_kaek,
                                          self.gdb(lui.p_geometry_ota), "OTA")
                cursor = arcpy.UpdateCursor(lui.p_geometry_ota)

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
        """
        Checks for self intersections in FBOUNDS

        :return: Nothing
        """

        if status[self.mode].check('EXPORTED', "FBOUND"):
            try:
                arcpy.CheckGeometry_management(available('FBOUND'),
                                               self.gdb(lui.fbound_geom))

                count_geom = get_count(lui.fbound_geom)
                problematic_set = set()
                problematic = []

                # Elegxos gia to an uparxoun self_intersections
                # kai apomonosi ton provlimatikon KAEK
                if count_geom == 0:
                    pm("\nGEOMETRY OK - NO SELF INTERSECTIONS IN FBOUND.\n")
                else:
                    arcpy.AddField_management(lui.fbound_geom, "OTA", "TEXT",
                                              field_length=5)
                    arcpy.CalculateField_management(lui.fbound_geom,
                                                    "OTA",
                                                    '!CLASS![-5:]',
                                                    "PYTHON_9.3")
                    pm("\n{} SELF INTERSECTIONS IN FBOUND.\n".format(
                        count_geom))

                    cursor = arcpy.UpdateCursor(lui.fbound_geom)
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
        """
        Checks intersections on ROADS shapefiles.

        :param _roads: **str**, optional
            Type of roads. If 'old' InputData roads will be used. If 'new'
            localdata roads will be used.
        :return: Nothing
        """

        roads = choose_roads(_roads)

        if ktima_status('PST', 'ASTENOT', roads):
            org[self.mode].add_layer([lui.pstM, lui.roadsM, lui.astenotM])

            # Eksagwgh kai enosi eidikwn ektasewn
            arcpy.SelectLayerByAttribute_management(lui.pstM,
                                                    "NEW_SELECTION",
                                                    " PROP_TYPE = '0701' ")
            arcpy.CopyFeatures_management(lui.pstM, self.gdb(lui.ek))
            clear_selection(lui.pstM)
            arcpy.Dissolve_management(lui.ek, self.gdb(lui.temp_ek),
                                      "PROP_TYPE")

            # Elegxos gia aksones ektos EK
            arcpy.Intersect_analysis([lui.roadsM, lui.temp_ek],
                                     self.gdb(lui.intersections_roads),
                                     output_type="POINT")
            arcpy.DeleteField_management(lui.intersections_roads, "PROP_TYPE")

            # Elegxos gia aksones pou mporei na kovoun thn idia enotita
            arcpy.SpatialJoin_analysis(lui.intersections_roads, lui.pstM,
                                       self.gdb(lui.intersections_pst_rd),
                                       match_option="CLOSEST")
            arcpy.SelectLayerByAttribute_management(lui.intersections_pst_rd,
                                                    "NEW_SELECTION",
                                                    " PROP_TYPE = '0101' ")
            arcpy.SpatialJoin_analysis(lui.intersections_pst_rd,
                                       lui.astenotM,
                                       self.gdb(lui.intersections_astenot_rd))

            count_inter_all = get_count(lui.intersections_roads)
            count_inter_astenot = get_count(lui.intersections_astenot_rd)

            if count_inter_astenot > 10:
                arcpy.Dissolve_management(lui.intersections_astenot_rd,
                                          self.gdb(lui.p_roads),
                                          "CAD_ADMIN", "CAD_ADMIN COUNT")
            else:
                arcpy.SpatialJoin_analysis(lui.intersections_pst_rd,
                                           lui.astenotM,
                                           self.gdb(lui.p_roads))

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
        """
        Checks DBOUND shapefiles for missing data in attribute table.

        :return:
        """

        if ktima_status('DBOUND'):
            # Elegxos gia DBOUND pou mporei na toys leipei eite to
            # DEC_ID eite to DEC_DATE
            org[self.mode].add_layer([lui.dboundM])

            arcpy.SelectLayerByAttribute_management(lui.dboundM,
                                                    "NEW_SELECTION",
                                                    " DEC_ID = '' ")
            arcpy.SelectLayerByAttribute_management(lui.dboundM,
                                                    "ADD_TO_SELECTION",
                                                    " DEC_DATE IS NULL ")
            arcpy.CopyFeatures_management(lui.dboundM,
                                          self.gdb(lui.p_dbound))

            count_dbound = get_count(lui.p_dbound)

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
        """
        Checks BLD shapefiles for missing data in attribute table.

        :return: Nothing
        """

        if ktima_status('BLD'):
            # Elegxos gia BLD pou mporei na exoun thn timh '0' eite
            # sto BLD_T_C eite sto BLD_NUM
            org[self.mode].add_layer([lui.bldM])

            arcpy.SelectLayerByAttribute_management(lui.bldM,
                                                    "NEW_SELECTION",
                                                    " BLD_T_C = 0 ")
            arcpy.SelectLayerByAttribute_management(lui.bldM,
                                                    "ADD_TO_SELECTION",
                                                    " BLD_NUM = 0 ")
            arcpy.CopyFeatures_management(lui.bldM, self.gdb(lui.temp_bld))
            arcpy.SpatialJoin_analysis(lui.temp_bld, self.gdb(lui.pstM),
                                       self.gdb(lui.p_bld),
                                       match_option='WITHIN')

            count_bld = get_count(lui.p_bld)

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
    """
    Class Fix has all the functions for fixing problems in shapefiles.

    Methods
    -------
    - pst_geometry
    - fbound_geometry
    - roads
    """

    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def pst_geometry(self):
        """
        Fixes PST geometry.

        :return: Nothing
        """

        if status[self.mode].check('SHAPES_GEOMETRY', "PROBS"):
            # Epilogi olon ton shapefile enos provlimatikou OTA kai
            # epidiorthosi tis geometrias tous
            _data = load_json(paths.status_path)

            repaired = []

            for row in _data["SHAPES_GEOMETRY"]["OTA"]:
                ota_folder = str(row)
                repaired.append(int(ota_folder))
                for i in lui.geometry_list:
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
        """
        Fixes FBOUND geometry.

        :return: Nothing
        """

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
        """
        Fixes ROADS.

        :return: Nothing
        """

        if status[self.mode].check("ROADS", "CPROBS"):
            # Kopsimo ton aksonon 10 cm prin to orio tis enotitas
            arcpy.Buffer_analysis(self.gdb(lui.temp_ek),
                                  self.gdb(lui.ek_fixed_bound),
                                  lui.ek_bound_reduction)
            arcpy.Clip_analysis(self.gdb(lui.roadsM),
                                self.gdb(lui.ek_fixed_bound),
                                self.gdb(lui.gdb_roads_all))

            status[self.mode].update("EXPORTED", "ROADS", False)

            log('Fix ROADS')
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")


class Fields:
    """
    Class Fields has functions for filling and fixing attributes tables.

    Methods
    -------
    - pst
    - astenot
    -asttom
    """

    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    @mxd
    def pst(self):
        """
        Fixing PST fields for ORI_TYPE, DEC_ID, ADDRESS.

        :return: Nothing
        """

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
        """
        Deletes ACQ_SCALE field from ASTTOM.

        :return: Nothing
        """

        # Diagrafi ACQ_SCALE apo tous ASTTOM
        for lyr_asttom in org[self.mode].available('ASTTOM'):
            if lyr_asttom[-5:] in kt.otas:
                pm("Processing {}".format(lyr_asttom))
                arcpy.DeleteField_management(lyr_asttom, "ACQ_SCALE", )

        pm("\nDONE !\n")

        log('Fields ASTTOM')

    @mxd
    def astenot(self):
        """
        Supplements LOCALITY fiels in ASTENOT.

        :return: Nothing
        """

        # Prosthiki onomasias sto pedio LOCALITY ton ASTENOT me vasi txt arxeio
        available_otas = org[self.mode].available('ASTENOT', ota_num=True)

        with open(paths.locality) as csvfile:
            localnames = csv.reader(csvfile)

            for row in localnames:
                try:
                    ota = row[0][:5]
                    if ota in available_otas and ota in kt.otas:
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
    """
    Class Create has functions for creating shapefiles.

    Methods
    -------
    - fbound
    - roads
    - fboundclaim
    - pre_fbound

    """

    def __init__(self, mode):
        self.mode = mode
        self.gdb = gdb[mode]

    def fbound(self):
        """
        Creates FBOUND shapefiles

        :return: Nothing
        """

        if ktima_status('ASTOTA'):
            # Dhmiourgia tou sunolikou FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis([self.gdb(lui.astotaM),
                                      paths.dasinpath],
                                     self.gdb(lui.gdb_fbound_all),
                                     output_type="INPUT")
            arcpy.DeleteField_management(self.gdb(lui.gdb_fbound_all),
                                         ["FID_merge_ASTOTA", "FID_PO_PARCELS",
                                          "FIELD", "AREA", "LEN"])
            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lui.gdb_fbound_all),
                paths.fboundoutpath,
                lui.fbound_all)

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

                lyr_fbound = lui.fbound_all
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

            arcpy.SelectLayerByAttribute_management(lui.fbound_all,
                                                    "NEW_SELECTION",
                                                    " DOC_ID = '' ")

            if get_count(lui.fbound_all) != 0:
                pm("\n !!! Leipoun DOC_ID apo to FBOUND_ALL \n!!!")

            clear_selection(lui.fbound_all)

            arcpy.DeleteField_management(lui.fbound_all, "CAD_ADMIN")

            pm("Exporting FBOUND / OTA")

            # Eksagogi FBOUND ana OTA
            general[self.mode].export_per_ota(lui.fbound_all,
                                              spatial=False, field='DOC_ID',
                                              formal=True,
                                              name="FBOUND")

            mdf(lui.fbound_all, importance='!')

            pm("\nDONE !\n")

            time_now = timestamp()

            status[self.mode].update("EXPORTED", "FBOUND", True)
            status[self.mode].update("SHAPE", "FBOUND", False)
            status[self.mode].update("EXPORTED", "FBOUND_ED", time_now)

            log('Create FBOUND')

    def roads(self):
        """
        Creates ROADS shapefiles.

        :return: Nothing
        """

        if status[self.mode].check("ROADS", "CPROBS") \
                and not status[self.mode].check("EXPORTED", "ROADS"):

            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lui.gdb_roads_all),
                paths.rdoutpath, lui.roads_all)

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
            general[self.mode].export_per_ota(lui.roads_all, spatial=True,
                                              formal=True,
                                              name="ROADS")

            mdf(lui.roads_all, importance='!')

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
        """
        Creates FOREST CLAIMS shapefiles and mdb.

        :return: Nothing
        """

        if ktima_status('PST', 'FBOUND'):
            # Dhmiourgia tou pinaka tis diekdikisis tou dasous
            arcpy.Intersect_analysis(
                [self.gdb(lui.pstM), self.gdb(lui.fboundM)],
                self.gdb(lui.intersection_pst_fbound),
                output_type="INPUT")
            arcpy.Dissolve_management(lui.intersection_pst_fbound,
                                      self.gdb(lui.gdb_fbound_claim),
                                      ["KAEK", "AREA"])
            arcpy.FeatureClassToFeatureClass_conversion(lui.gdb_fbound_claim,
                                                        paths.claimoutpath,
                                                        lui.fbound_claim)

            turn_off()

            # Diagrafi eggrafon vasi tupikon prodiagrafon
            arcpy.SelectLayerByAttribute_management(lui.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " Shape_Area < 100 ")
            # Svinontai oles oi eggrafes kato apo 100 m2
            arcpy.DeleteRows_management(lui.fbound_claim)
            clear_selection(lui.fbound_claim)
            arcpy.AddField_management(lui.fbound_claim, "AREA_MEAS", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(lui.fbound_claim, "AREAFOREST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(lui.fbound_claim, "AREA_REST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.CalculateField_management(lui.fbound_claim, "AREA_MEAS",
                                            '!AREA!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lui.fbound_claim, "AREAFOREST",
                                            '!Shape_Area!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lui.fbound_claim, "AREA_REST",
                                            '!AREA_MEAS! - !AREAFOREST!',
                                            "PYTHON_9.3")
            arcpy.AddField_management(lui.fbound_claim, "TYPE", "SHORT",
                                      field_precision=1)
            arcpy.SelectLayerByAttribute_management(lui.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " AREA_REST < 1 ")
            # Oles oi eggrafes me AREA_REST kato apo 1 m2  diekdikountai pliros
            arcpy.CalculateField_management(lui.fbound_claim, "AREA_REST", '0',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(lui.fbound_claim, "TYPE", '1',
                                            "PYTHON_9.3")
            clear_selection(lui.fbound_claim)
            arcpy.DeleteField_management(lui.fbound_claim,
                                         ["AREA", "Shape_Area", "Shape_Length",
                                          "Shape_Leng", "DOC_ID", "ORI_CODE",
                                          "LEN"])

            count_claims = get_count(lui.fbound_claim)

            mdf(lui.fbound_claim, importance='!')
            arcpy.FeatureClassToFeatureClass_conversion(paths.claiminpath,
                                                        paths.mdb(),
                                                        lui.diekdikisi)

            pm(
                "\nDONE ! - Forest claiming {} KAEK.\n\n"
                "Don't forget to change AREAFOREST to AREA_FOREST\n".format(
                    count_claims))

            log('Create FBOUND Claims', count_claims)

            pm("\nDONE !\n")

    def pre_fbound(self):
        """
        Creates PRE_FBOUND shapefiles.

        :return: Nothing
        """

        if ktima_status('ASTOTA'):
            # Dhmiourgia tou sunolikoy PRE_FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis(
                [self.gdb(lui.astotaM), paths.predasinpath],
                self.gdb(lui.gdb_pre_fbound_all),
                output_type="INPUT")
            arcpy.DeleteField_management(self.gdb(lui.gdb_pre_fbound_all),
                                         ["FID_merge_ASTOTA",
                                          "FID_KYR_PO_PARCELS", "KATHGORDX",
                                          "KATHGORAL1", "AREA", "LEN",
                                          "CAD_ADMIN"])
            arcpy.FeatureClassToFeatureClass_conversion(
                self.gdb(lui.gdb_pre_fbound_all),
                paths.fboundoutpath,
                lui.pre_fbound_all)

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
            general[self.mode].export_per_ota(lui.pre_fbound_all,
                                              spatial=True, formal=True,
                                              name="FBOUND")

            mdf(lui.pre_fbound_all, importance='!')

            pm("\nDONE !\n")

            log('Create PRE_FBOUND')
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")


geoprocessing = {KTIMA_MODE: Geoprocessing(KTIMA_MODE),
                 STANDALONE_MODE: Geoprocessing(STANDALONE_MODE,
                                                standalone=True)}
find = {KTIMA_MODE: Queries(KTIMA_MODE),
        STANDALONE_MODE: Queries(STANDALONE_MODE)}
general = {KTIMA_MODE: General(KTIMA_MODE),
           STANDALONE_MODE: General(STANDALONE_MODE)}
check = {KTIMA_MODE: Check(KTIMA_MODE),
         STANDALONE_MODE: Check(STANDALONE_MODE)}
fix = {KTIMA_MODE: Fix(KTIMA_MODE),
       STANDALONE_MODE: Fix(STANDALONE_MODE)}
fields = {KTIMA_MODE: Fields(KTIMA_MODE),
          STANDALONE_MODE: Fields(STANDALONE_MODE)}
create = {KTIMA_MODE: Create(KTIMA_MODE),
          STANDALONE_MODE: Create(STANDALONE_MODE)}
