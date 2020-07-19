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
    Checks whether or not shp_list are merged so that
    operations can performed more quickly.

    :param args: str
        Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
    :return: boolean
        True if shp_list are merged, False otherwise
    """

    checker = 0
    shp_exists = []

    for shp in args:
        if not status[kt.mode].check('SHAPE', shp):
            pm('\n{} not Merged'.format(shp))
            checker += 1

    if not checker:
        for shp in args:
            if not arcpy.Exists(kt.gdb('merge_{}'.format(shp))):
                shp_exists.append(shp)

        if not shp_exists:
            return True
        else:
            pm("\nMerge shp_list don't exist in {}.gdb:\n".format(kt.mode))
            for fc in shp_exists:
                pm(fc)
            pm('\n\n\n!! Task Aborted !!\n\n\n')
    else:
        pm('\n\n\n!! Task Aborted !!\n\n\n')
        return False


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

    def __init__(self):
        pass

    @staticmethod
    @mxd
    def merge(shapes, force_merge=False, missing='raise'):
        """
        ArcGIS automation to merge shp_list

        :param missing:
        :param shapes: str
            Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
        :param force_merge: boolean, optional
            Whether or not shp_list will be merged even if they
            are already merged (default: False)
        :param missing: str, {'raise', 'ignore'}, optional
            Whether or nor missing shp_list should be ignored
            (default: 'raise')
        :return: nothing
        """

        log_list = []

        for _shape in shapes:
            shapefile = _shape

            if not status[kt.mode].check('SHAPE',
                                         shapefile) or force_merge:
                f_name = "merge_" + shapefile

                to_merge = org.fetch(shapefile, missing=missing)

                try:
                    arcpy.Merge_management(to_merge, kt.gdb(f_name))

                    pm("\nMerged {}\n".format(shapefile))

                    status[kt.mode].update('SHAPE', shapefile, True)
                    log_list.append(str(shapefile))
                except RuntimeError:
                    pm("\n!!! {} source files missing !!!\n".format(shapefile))
            else:
                pm('\n{} already merged\n'.format(shapefile))

        if log_list:
            log("Merge Shapefiles", log_list=log_list)

    @staticmethod
    def union(shapes, precision=info.precision, missing='raise',
              gaps=False):
        """
        ArcGIS automation for performing Union in shp_list


        :param shapes: str
            Spatial data categories of Greek Cadastre ('ASTOTA', 'PST', etc.)
        :param precision: float, optional
            Float number passed to "Union" in ArcGIS
            (default is defined in a json file)
        :param missing: missing: str, {'raise', 'ignore'}, optional
            Whether or nor missing shp_list should be ignored
            (default: 'raise')
        :param gaps: boolean, optional
            Whether or not "Union" will be performed with gaps
            (default is False)
        :return: Nothing
        """

        if gaps:
            _gaps = "GAPS"
        else:
            _gaps = "NO_GAPS"

        if shapes == "ALL":
            for shapefile in info.merging_list:
                pm("Union for {}\n".format(shapefile))

                feature_name = "union_" + shapefile
                arcpy.Union_analysis(
                    list(org.mxd_fl[shapefile]),
                    kt.gdb(feature_name),
                    "NO_FID",
                    precision,
                    _gaps)
        else:
            for shape in shapes:
                feature_name = "union_" + shape

                to_union = org.fetch(shape, missing=missing)

                arcpy.Union_analysis(
                    to_union,
                    kt.gdb(feature_name),
                    "NO_FID",
                    precision,
                    _gaps)


class Queries:
    def __init__(self):
        pass

    @staticmethod
    def kaek_in_dbound():
        arcpy.Intersect_analysis([kt.gdb(ns.pstM),
                                  kt.gdb(ns.dboundM)],
                                 kt.gdb(ns.kaek_in_dbound),
                                 output_type="INPUT")
        pm('\nDONE !  -->  {}\n'.format(ns.kaek_in_dbound))

    @staticmethod
    def kaek_in_astik():
        if ktima_status('PST', 'ASTIK'):
            arcpy.Intersect_analysis([kt.gdb(ns.pstM), kt.gdb(ns.astikM)],
                                     kt.gdb(ns.kaek_in_astik),
                                     output_type="INPUT")
            pm('\nDONE !  -->  {}\n'.format(ns.kaek_in_astik))

    @staticmethod
    def rd():
        org.add_layer([ns.pstM])
        arcpy.SelectLayerByAttribute_management(ns.pstM,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0701' ")
        arcpy.CopyFeatures_management(ns.pstM, kt.gdb(ns.rd))
        pm('\nDONE !  -->  {}\n'.format(ns.rd))

    @staticmethod
    def pr():
        org.add_layer([ns.pstM])
        arcpy.SelectLayerByAttribute_management(ns.pstM,
                                                "NEW_SELECTION",
                                                " PROP_TYPE = '0702' ")
        arcpy.CopyFeatures_management(ns.pstM, kt.gdb(ns.pr))
        pm('\nDONE !  -->  {}\n'.format(ns.pr))

    @staticmethod
    def advanced_query(query,
                       against,
                       user_query=False,
                       user_against=False):

        what_to_query = {
            'PST': ns.pstM,
            'ASTENOT': ns.astotaM,
            'ASTTOM': ns.astotaM,
            'ASTIK': ns.astikM,
            'DBOUND': ns.dboundM
        }

        if user_query:
            find_from = query
        else:
            find_from = what_to_query[query]

        if user_against:
            find_in = against
        else:
            find_in = what_to_query[against]

        org.add_layer([find_from, find_in])

        arcpy.SelectLayerByLocation_management(find_from, 'WITHIN', find_in)

        count = get_count(find_from)

        if count != 0:
            fc_name = "{}_within_{}".format(query, against)
            arcpy.CopyFeatures_management(find_from, kt.gdb(fc_name))
            clear_selection(find_from)
            pm('\nDONE !\n-->  {} - {} features\n'.format(fc_name, count))
        else:
            pm('\nNo selection was made. No files were exported\n')

    @staticmethod
    def find_identical(what, in_what, export=False):
        """
        Find identical parcels between two shspefiles and prints statistics

        :param what: str, list
            Shapefile or feature layer
        :param in_what: str
            Shapefile or feature layer
        :param export: boolean
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

            arcpy.Merge_management(to_merge, kt.gdb('identical'))

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

    def __init__(self):
        pass

    @staticmethod
    def isolate(fc):
        """
        Isolate Features in the area of interest

        :param fc: str
            Feature class or shapefile
        :return: Nothing
        """

        if ktima_status('ASTOTA'):
            org.add_layer([ns.astotaM])

            arcpy.Dissolve_management(ns.astotaM, kt.gdb(ns.oria_etairias))

            fc_n = "{}_{}".format(info.company_name, fc)
            arcpy.Intersect_analysis([fc, ns.oria_etairias],
                                     kt.gdb(fc_n),
                                     output_type="INPUT")

            mdf(ns.oria_etairias, importance='!!')
            mdf(fc_n)

    @staticmethod
    @mxd
    def export_per_ota(fc,
                       spatial,
                       spatial_method='location_within',
                       field='KAEK',
                       export_shp=True,
                       database=False,
                       formal=False,
                       name=None):
        """
        Given a shapefile it will export the features that intersect with
        a specific ota as a new shapefile.


        :param fc: str
            Shapefile or feature class.
        :param spatial: boolean
            If True the selection will be based on spatial location
            If False the selection will be bases on an attribute. Field
            parameter is required when set to False.
        :param spatial_method: str {'location_intersect,
                                    'location_within',
                                    'intersect'}, optional
            The way shp_list per ota will be exported
            (default: 'location_within')
        :param field: str, optional
            Field of the shapefile attribute table that the selection will
            be based on (default: 'KAEK')
        :param export_shp: boolean, optional
            If True, shp_list for each ota
             will be exported in this folder (OutputData\\Shapefile\\!!OTA).
            If False, feature classes will be exported for each ota in gdb.
            (default: True)
        :param database: boolean, optional
            If True, mdbs will be also exported in archive.mdb
            If False, no mdbs will be made.
            (default: False)
        :param formal: boolean, optional
            If True formal export will be executed based on formal mdf function
             parameter.
            If False, shp_list for each ota
             will be exported in this folder (OutputData\\Shapefile\\!!OTA).
             (default: False)
        :param name: str, optional
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
                arcpy.CopyFeatures_management(_fc, kt.gdb(fc_name))

        if spatial:
            if spatial_method in ['location_intersect', 'location_within']:
                if spatial_method == 'location_intersect':
                    how = 'INTERSECT'
                else:
                    how = 'WITHIN'

                for ota in org.fetch('ASTOTA',
                                     missing='ignore',
                                     ota_num=True):

                    lyr_astota = toc_layer('ASTOTA', ota)

                    if ota in kt.otas:
                        arcpy.SelectLayerByLocation_management(fc,
                                                               how,
                                                               lyr_astota)

                        if get_count(fc) != 0:
                            export(fc, ota)
                            clear_selection(fc)
            else:
                if ktima_status('ASTOTA'):
                    intersected = "i_{}".format(fc)

                    arcpy.Intersect_analysis([fc, kt.gdb(ns.astotaM)],
                                             kt.gdb(intersected),
                                             output_type="INPUT",
                                             join_attributes='NO_FID')

                    org.add_layer([intersected])

                    arcpy.DeleteField_management(intersected,
                                                 clean_fields(fc,
                                                              intersected))

                    for lyr_astota in org.fetch('ASTOTA', missing='ignore'):
                        ota = str(lyr_astota[-5:])
                        if ota in kt.otas:
                            arcpy.SelectLayerByLocation_management(intersected,
                                                                   'WITHIN',
                                                                   lyr_astota)
                            if get_count(intersected) != 0:
                                export(intersected, ota)
                                clear_selection(intersected)
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

    @staticmethod
    def export_to_server(copy_files, plus_name):
        """
        Export generated shp_list to company server

        :param copy_files: str
            Shapefile to export
        :param plus_name: str
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
                arcpy.FeatureClassToFeatureClass_conversion(kt.gdb(shp),
                                                            _path,
                                                            shp)

                pm('Exported {} from {}.gdb'.format(shp, plus_name))

            except RuntimeError:
                pm('Dataset {} does not exist'.format(shp))

        pm('\nDone !\n')

    @staticmethod
    def month_report():
        if ktima_status('PST', 'ASTENOT', 'ASTIK', 'DBOUND'):
            org.add_layer([ns.pstM, ns.astenotM, ns.astikM, ns.dboundM])

            dbound_area = 0.0

            ap = get_count(ns.pstM)
            aa = get_count(ns.astenotM)

            arcpy.SelectLayerByLocation_management(ns.pstM, 'WITHIN', ns.astikM)
            astik_pst = get_count(ns.pstM)
            agrot_pst = ap - astik_pst

            arcpy.SelectLayerByLocation_management(ns.astenotM, 'WITHIN',
                                                   ns.astikM)
            astik_astenot = get_count(ns.astenotM)
            agrot_astenot = aa - astik_astenot

            clear_selection(ns.pstM)
            clear_selection(ns.astenotM)

            arcpy.SelectLayerByLocation_management(ns.pstM, 'WITHIN',
                                                   ns.dboundM)
            dbound_pst = get_count(ns.pstM)

            cursor = arcpy.UpdateCursor(ns.dboundM)
            for row in cursor:
                dbound_area += float(row.getValue("AREA"))

            dbound_str = round(dbound_area / 1000, 2)

            pm("PST- ALL: {} / ASTIKO: {} / AGROTIKO: {}\n".format(ap,
                                                                   astik_pst,
                                                                   agrot_pst))

            pm("ASTENOT- ALL: {} / ASTIKO: {} / AGROTIKO: {}\n".format(
                aa,
                astik_astenot,
                agrot_astenot))

            pm("DBOUND KAEK: {} / AREΑ (m2): {} - (stremmata): {}\n\n".format(
                dbound_pst,
                dbound_area,
                dbound_str))


class Check:
    """
    Check class has all the basic check functions for the shp_list.

    Methods
    -------
    - shapes
    - pst_geometry
    - fbound_geometry
    - roads
    - bld
    - dbound
    """

    def __init__(self):
        pass

    @staticmethod
    @mxd
    def boundaries(inner, check_leitourgoun=False, outer=4):
        if ktima_status('ASTOTA'):
            _inner = float(10 ** -inner)

            precision_txt = '{:.{}f} m'.format(_inner, inner)

            pm("\n  Check accuracy : {}\n".format(precision_txt))

            pm("\n  Processing...\n")

            geoprocessing.union(['ASTOTA'], _inner, gaps=False)
            turn_off()

            org.add_layer([ns.astotaM])

            count_astota_m = get_count(ns.astotaM)
            count_astota_u = get_count(ns.astotaU)
            diff_astota = count_astota_u - count_astota_m

            if count_astota_m != count_astota_u:
                arcpy.SelectLayerByAttribute_management(
                    ns.astotaU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(
                        count_astota_m))
                arcpy.CopyFeatures_management(ns.astotaU,
                                              kt.gdb(ns.p_overlaps_astota))

            if check_leitourgoun:
                _outer = float(10 ** -outer)

                arcpy.Merge_management([ns.astotaM, ns.leitourgoun],
                                       kt.gdb(ns.astota_leitourgounM))

                arcpy.Union_analysis(
                    [ns.astotaM, ns.leitourgoun],
                    kt.gdb(ns.astota_leitourgounU),
                    "NO_FID",
                    _outer,
                    "NO_GAPS")

                count_leitourgoun_m = get_count(ns.astota_leitourgounM)
                count_leitourgoun_u = get_count(ns.astota_leitourgounU)
                diff_leitourgoun = count_leitourgoun_m - count_leitourgoun_u

                if count_leitourgoun_m != count_leitourgoun_u:
                    arcpy.SelectLayerByAttribute_management(
                        ns.astota_leitourgounU,
                        "NEW_SELECTION",
                        ''' "OBJECTID" > {} '''.format(
                            count_leitourgoun_m))
                    arcpy.CopyFeatures_management(
                        ns.astotaU,
                        kt.gdb(
                            ns.p_overlaps_leitourgoum))

                if count_leitourgoun_m == count_leitourgoun_u:
                    pm('\n  - LEITOURGOUN - OK\n')
                else:
                    pm('\n  - LEITOURGOUN - ! Overlaps ! - [{}]\n'.format(
                        diff_leitourgoun))

            log_shapes = [precision_txt,
                          diff_astota]

            # TO UNION PREPEI NA EINAI IDIO ME TO MERGE
            if count_astota_m == count_astota_u:
                pm('\n  - ASTOTA - OK\n')
            else:
                pm('\n  - ASTOTA - ! Overlaps ! - [{}]\n'.format(diff_astota))

            log('Check ASTOTA', log_list=log_shapes)

    @staticmethod
    @mxd
    def overlaps(accuracy):
        """
        Checks for overlaps and wrong numbering.

        :param accuracy: int
            Precision which will be used in 'union'.
        :return: Nothing
        """

        if ktima_status('PST', 'ASTTOM', 'ASTENOT'):

            precision = float(10 ** -accuracy)

            precision_txt = '{:.{}f} m'.format(precision, accuracy)

            pm("\n  Check accuracy : {}\n".format(precision_txt))

            pm("\n  Processing...\n")

            # GEOPROCESSING

            geoprocessing.union(['PST', 'ASTTOM'],
                                precision,
                                gaps=False)

            geoprocessing.union(['ASTENOT'],
                                precision,
                                gaps=True)

            turn_off()
            org.add_layer([ns.pstM, ns.astenotM, ns.asttomM])

            # Problem count
            count_pst_u = get_count(ns.pstU)
            count_pst_m = get_count(ns.pstM)
            diff_pst = count_pst_u - count_pst_m

            count_astenot_u = get_count(ns.astenotU)
            count_astenot_m = get_count(ns.astenotM)
            diff_astenot = count_astenot_u - count_astenot_m

            count_asttom_u = get_count(ns.asttomU)
            count_asttom_m = get_count(ns.asttomM)
            diff_asttom = count_asttom_u - count_asttom_m

            if count_astenot_m != count_astenot_u:
                arcpy.SelectLayerByAttribute_management(
                    ns.astenotU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(
                        count_astenot_m))
                arcpy.CopyFeatures_management(ns.astenotU,
                                              kt.gdb(ns.p_overlaps_astenot))

            if count_asttom_m != count_asttom_u:
                arcpy.SelectLayerByAttribute_management(
                    ns.asttomU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_asttom_m))
                arcpy.CopyFeatures_management(ns.asttomU,
                                              kt.gdb(ns.p_overlaps_asttom))

            if count_pst_m != count_pst_u:
                arcpy.SelectLayerByAttribute_management(
                    ns.pstU,
                    "NEW_SELECTION",
                    ''' "OBJECTID" > {} '''.format(count_pst_m))
                arcpy.CopyFeatures_management(ns.pstU,
                                              kt.gdb(ns.p_overlaps_pst))

            log_shapes = [precision_txt,
                          diff_pst,
                          diff_astenot,
                          diff_asttom]

            # TO UNION PREPEI NA EINAI IDIO ME TO MERGE
            if count_pst_m == count_pst_u:
                pm('\n  - PST - OK')
            else:
                pm('\n  - PST - ! Overlaps ! - [{}]'.format(diff_pst))

            if count_astenot_m == count_astenot_u:
                pm('  - ASTENOT - OK')
            else:
                pm('  - ASTENOT - ! Overlaps ! - [{}]'.format(diff_astenot))

            if count_asttom_m == count_asttom_u:
                pm('  - ASTTOM - OK\n')
            else:
                pm('  - ASTTOM - ! Overlaps ! - [{}]\n'.format(diff_asttom))

            time_now = timestamp()

            log("Check Overlaps", log_list=log_shapes)
            status[kt.mode].update("OVERLAPS", "DECIMALS", precision_txt)
            status[kt.mode].update("OVERLAPS", "CD", time_now)
            status[kt.mode].update("OVERLAPS", "ASTENOT", diff_astenot)
            status[kt.mode].update("OVERLAPS", "ASTTOM", diff_asttom)
            status[kt.mode].update("OVERLAPS", "PST", diff_pst)

    @staticmethod
    def numbering():
        if ktima_status('PST', 'ASTTOM', 'ASTENOT'):
            pm("\n  Processing...\n")

            org.add_layer([ns.pstM, ns.astenotM, ns.asttomM])

            # ENOTITES
            arcpy.AddField_management(ns.astenotM, "ENOT", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(ns.astenotM, "ENOT",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            # TOMEIS
            arcpy.AddField_management(ns.asttomM, "TOM", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(ns.asttomM, "TOM",
                                            '!CAD_ADMIN!',
                                            "PYTHON_9.3")

            arcpy.SpatialJoin_analysis(ns.pstM, ns.astenotM,
                                       kt.gdb(ns.pst_astenot),
                                       match_option='WITHIN')
            arcpy.SpatialJoin_analysis(ns.astenotM, ns.asttomM,
                                       kt.gdb(ns.astenot_asttom),
                                       match_option='WITHIN')

            turn_off()

            arcpy.AddField_management(ns.pst_astenot, "pstENOT", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(ns.pst_astenot, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(ns.pst_astenot, "PSTenot",
                                            '!KAEK![:9]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(ns.pst_astenot, "matches",
                                            'bool(!CAD_ADMIN!==!pstENOT!)',
                                            "PYTHON_9.3")

            count_pst_astenot_og = get_count(ns.pst_astenot)

            arcpy.SelectLayerByAttribute_management(
                ns.pst_astenot,
                "NEW_SELECTION",
                " matches = '0' and pstENOT not like '%ΕΚ%' ")

            count_pst_astenot = get_count(ns.pst_astenot)

            if count_pst_astenot == count_pst_astenot_og:
                probs_pst_astenot = 0
            else:
                probs_pst_astenot = count_pst_astenot

            if probs_pst_astenot:
                arcpy.CopyFeatures_management(ns.pst_astenot,
                                              kt.gdb(ns.p_pst_astenot))

            arcpy.AddField_management(ns.astenot_asttom, "enotTOM", "TEXT",
                                      field_length=50)
            arcpy.AddField_management(ns.astenot_asttom, "matches", "TEXT",
                                      field_length=50)
            arcpy.CalculateField_management(ns.astenot_asttom,
                                            "enotTOM",
                                            '!ENOT![:7]',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(ns.astenot_asttom,
                                            "matches",
                                            'bool(!TOM!==!enotTOM!)',
                                            "PYTHON_9.3")

            count_astenot_asttom_og = get_count(ns.astenot_asttom)

            arcpy.SelectLayerByAttribute_management(ns.astenot_asttom,
                                                    "NEW_SELECTION",
                                                    " matches = '0' ")

            count_astenot_asttom = get_count(ns.astenot_asttom)

            if count_astenot_asttom == count_astenot_asttom_og:
                probs_astenot_asttom = 0
            else:
                probs_astenot_asttom = count_astenot_asttom

            if probs_astenot_asttom:
                arcpy.CopyFeatures_management(ns.astenot_asttom,
                                              kt.gdb(ns.p_astenot_asttom))

            # PREPEI NA MIN YPARXEI KAMIA EGGRAFI STOUS PROBLIMATIKOUS PINAKES

            if probs_pst_astenot == 0:
                pm('\n  - PST me ASTENOT - OK')
            else:
                pm('\n  ! Lathos KAEK se ENOTITA ! - [{}]'.format(
                    count_pst_astenot))

            if probs_astenot_asttom == 0:
                pm('  - ASTENOT me ASTTOM - OK\n')
            else:
                pm('  ! Lathos KAEK se TOMEA ! - [{}]\n'.format(
                    count_astenot_asttom))

            log_shapes = [probs_pst_astenot,
                          probs_astenot_asttom]

            log("Check Numbering", log_list=log_shapes)
            status[kt.mode].update("WRONG_KAEK", "ASTENOT_ASTTOM",
                                   probs_pst_astenot)
            status[kt.mode].update("WRONG_KAEK", "PST_ASTENOT",
                                   probs_astenot_asttom)

    @staticmethod
    def pst_geometry():
        """
        Checks for self intersection in PST_merge.

        :return: Nothing
        """

        if ktima_status('PST'):
            org.add_layer([ns.pstM])
            turn_off()

            arcpy.CheckGeometry_management(ns.pstM, kt.gdb(ns.pst_geom))

            count_geom = get_count(ns.pst_geom)
            problematic_set = set()

            # Elegxos gia to an uparxoun self_intersections kai
            # apomonosi ton provlimatikon KAEK
            if count_geom == 0:
                pm("\n  GEOMETRY OK - NO SELF INTERSECTIONS.\n")
                problematic = []
            else:
                pm("\n  {} SELF INTERSECTIONS.\n".format(count_geom))
                pm("  Processing...\n")
                arcpy.AddJoin_management(ns.pstM, "OBJECTID", ns.pst_geom,
                                         "FEATURE_ID", "KEEP_COMMON")
                arcpy.CopyFeatures_management(ns.pstM,
                                              kt.gdb(ns.p_geometry_kaek))
                clear_selection(ns.pstM)
                arcpy.AddField_management(ns.p_geometry_kaek, "OTA", "TEXT",
                                          field_length=5)
                arcpy.CalculateField_management(ns.p_geometry_kaek, "OTA",
                                                '!merge_PST_KAEK![:5]',
                                                "PYTHON_9.3")
                arcpy.Dissolve_management(ns.p_geometry_kaek,
                                          kt.gdb(ns.p_geometry_ota), "OTA")
                cursor = arcpy.UpdateCursor(ns.p_geometry_ota)

                for row in cursor:
                    ota = str(row.getValue("OTA"))
                    problematic_set.add(ota)

                problematic = sorted(list(problematic_set))

                pm("  OTA with geometry problems:\n")
                for prob_ota in problematic:
                    pm('  - {}'.format(prob_ota))

                pm("\n")

            log_geometry = [count_geom,
                            problematic]

            time_now = timestamp()

            status[kt.mode].update("SHAPES_GEOMETRY", "PROBS",
                                   bool(count_geom))
            status[kt.mode].update("SHAPES_GEOMETRY", "CD", time_now)
            status[kt.mode].update("SHAPES_GEOMETRY", "OTA", problematic)

            pm("\nDONE !\n")

            log('Check PST Geometry', log_list=log_geometry)

    @staticmethod
    @mxd
    def fbound_geometry():
        """
        Checks for self intersections in FBOUNDS

        :return: Nothing
        """

        try:
            arcpy.CheckGeometry_management(
                org.fetch('FBOUND', missing='ignore'),
                kt.gdb(ns.fbound_geom))

            count_geom = get_count(ns.fbound_geom)
            problematic_set = set()

            # Elegxos gia to an uparxoun self_intersections
            # kai apomonosi ton provlimatikon KAEK
            if count_geom == 0:
                pm("\n  GEOMETRY OK - NO SELF INTERSECTIONS IN FBOUND.\n")
                problematic = []
            else:
                arcpy.AddField_management(ns.fbound_geom, "OTA", "TEXT",
                                          field_length=5)
                arcpy.CalculateField_management(ns.fbound_geom,
                                                "OTA",
                                                '!CLASS![-5:]',
                                                "PYTHON_9.3")
                pm("\n  {} SELF INTERSECTIONS IN FBOUND.\n".format(
                    count_geom))

                cursor = arcpy.UpdateCursor(ns.fbound_geom)
                for row in cursor:
                    ota = int(row.getValue("OTA"))
                    problematic_set.add(ota)

                problematic = sorted(list(problematic_set))

                pm("  OTA with FBOUND geometry problems :\n")
                for prob_ota in problematic:
                    pm('  - {}'.format(prob_ota))

            log_fbound_geometry = [count_geom,
                                   problematic]

            pm("\nDONE !\n")

            time_now = timestamp()

            status[kt.mode].update("FBOUND_GEOMETRY", "PROBS",
                                   bool(count_geom))
            status[kt.mode].update("FBOUND_GEOMETRY", "CD", time_now)
            status[kt.mode].update("FBOUND_GEOMETRY", "OTA", problematic)

            log('Check FBOUND Geometry', log_list=log_fbound_geometry)
        except RuntimeError:
            pm("\n!!! {} source files missing !!!\n".format('FBOUND'))

    @staticmethod
    def roads(check_with_buffer=False):
        """
        Checks intersections on ROADS shp_list.

        :param check_with_buffer: bool
            Whether or not it will check with duffered polygon
        :return:Nothing
        """

        if ktima_status('PST', 'ASTENOT', 'ROADS', 'ASTOTA'):

            org.add_layer([ns.pstM, ns.roadsM, ns.astenotM, ns.astotaM])

            pm('\n  Searching for small ROADS sections...\n')

            arcpy.FeatureToLine_management(ns.roadsM, kt.gdb(ns.roadsM_breaked))
            arcpy.SelectLayerByAttribute_management(ns.roadsM_breaked,
                                                    "NEW_SELECTION",
                                                    " Shape_Length < 0.021 ")

            small = get_count(ns.roadsM_breaked)

            if small:
                arcpy.CopyFeatures_management(ns.roadsM_breaked,
                                              kt.gdb(ns.roads_small))

            clear_selection(ns.roadsM_breaked)

            pm('  - Small ROADS sections - [{}]\n'.format(small))

            pm('\n  Searching for ROADS intersections...')

            # Eksagwgh kai enosi eidikwn ektasewn
            arcpy.SelectLayerByAttribute_management(ns.pstM,
                                                    "NEW_SELECTION",
                                                    " PROP_TYPE = '0701' ")

            arcpy.CopyFeatures_management(ns.pstM, kt.gdb(ns.ek))

            clear_selection(ns.pstM)

            arcpy.Dissolve_management(ns.ek, kt.gdb(ns.temp_ek),
                                      "PROP_TYPE")

            arcpy.Intersect_analysis([ns.temp_ek, ns.astotaM],
                                     kt.gdb(ns.ek_check),
                                     output_type="INPUT")
            if check_with_buffer:
                arcpy.Buffer_analysis(kt.gdb(ns.ek_check),
                                      kt.gdb(ns.ek_fixed_bound),
                                      ns.ek_bound_reduction)
                check_with = ns.ek_fixed_bound
            else:
                check_with = ns.ek_check

            # Elegxos gia aksones ektos EK
            arcpy.Intersect_analysis([ns.roadsM, check_with],
                                     ns.intersections_roads_multi,
                                     output_type="POINT")

            arcpy.MultipartToSinglepart_management(ns.intersections_roads_multi,
                                                   kt.gdb(
                                                       ns.intersections_roads))

            arcpy.DeleteField_management(ns.intersections_roads,
                                         ["PROP_TYPE", "CAD_ADMIN"])

            count_inter_all = get_count(ns.intersections_roads)

            if count_inter_all:
                # Elegxos gia aksones pou mporei na kovoun thn idia enotita
                arcpy.SpatialJoin_analysis(ns.intersections_roads, ns.astenotM,
                                           kt.gdb(ns.intersections_astenot_rd),
                                           match_option="CLOSEST")

            if count_inter_all > 10:
                arcpy.Dissolve_management(ns.intersections_astenot_rd,
                                          kt.gdb(ns.p_roads),
                                          "CAD_ADMIN", "CAD_ADMIN COUNT")
            elif 0 < count_inter_all <= 10:
                arcpy.SpatialJoin_analysis(ns.intersections_astenot_rd,
                                           ns.astenotM,
                                           kt.gdb(ns.p_roads))

            log_roads = [count_inter_all]

            if count_inter_all == 0:
                pm("\n  - ROADS - OK\n")
            else:
                pm("\n  - ROADS intersections - [{}]\n".format(count_inter_all))

            time_now = timestamp()

            log('Check ROADS', log_list=log_roads)
            status[kt.mode].update("ROADS", "ALL", count_inter_all)
            status[kt.mode].update("ROADS", "PROBS", 0)
            status[kt.mode].update("ROADS", "CD", time_now)
            status[kt.mode].update("ROADS", "CPROBS", bool(count_inter_all))

    @staticmethod
    def dbound():
        """
        Checks DBOUND shp_list for missing data in attribute table.

        :return:
        """

        if ktima_status('DBOUND'):
            # Elegxos gia DBOUND pou mporei na toys leipei eite to
            # DEC_ID eite to DEC_DATE
            org.add_layer([ns.dboundM])

            arcpy.SelectLayerByAttribute_management(ns.dboundM,
                                                    "NEW_SELECTION",
                                                    " DEC_ID = '' ")
            arcpy.SelectLayerByAttribute_management(ns.dboundM,
                                                    "ADD_TO_SELECTION",
                                                    " DEC_DATE IS NULL ")
            arcpy.CopyFeatures_management(ns.dboundM,
                                          kt.gdb(ns.p_dbound))

            count_dbound = get_count(ns.p_dbound)

            if count_dbound == 0:
                pm("\n  DBOUND - OK\n")
            else:
                pm("\n  - {} eggrafes den exoun DEC_ID / DEC_DATE.\n".format(
                    count_dbound))

            time_now = timestamp()

            log('Check DBOUND', log_list=count_dbound)
            status[kt.mode].update("DBOUND", "PROBS", count_dbound)
            status[kt.mode].update("DBOUND", "CD", time_now)

    @staticmethod
    def bld():
        """
        Checks BLD shp_list for missing data in attribute table.

        :return: Nothing
        """

        if ktima_status('BLD'):
            # Elegxos gia BLD pou mporei na exoun thn timh '0' eite
            # sto BLD_T_C eite sto BLD_NUM
            org.add_layer([ns.bldM])

            arcpy.SelectLayerByAttribute_management(ns.bldM,
                                                    "NEW_SELECTION",
                                                    " BLD_T_C = 0 ")
            arcpy.SelectLayerByAttribute_management(ns.bldM,
                                                    "ADD_TO_SELECTION",
                                                    " BLD_NUM = 0 ")
            arcpy.CopyFeatures_management(ns.bldM, kt.gdb(ns.temp_bld))
            arcpy.SpatialJoin_analysis(ns.temp_bld, kt.gdb(ns.pstM),
                                       kt.gdb(ns.p_bld),
                                       match_option='WITHIN')

            count_bld = get_count(ns.p_bld)

            if count_bld == 0:
                pm("\n  BLD - OK\n")
            else:
                pm("\n  - {} eggrafes den exoun BLD_T_C / BLD_NUM.\n".format(
                    count_bld))

            time_now = timestamp()

            log('Check BLD', log_list=count_bld)
            status[kt.mode].update("BLD", "PROBS", count_bld)
            status[kt.mode].update("BLD", "CD", time_now)


class Fix:
    """
    Class Fix has all the functions for fixing problems in shp_list.

    Methods
    -------
    - pst_geometry
    - fbound_geometry
    - roads
    """

    def __init__(self):
        pass

    @staticmethod
    def pst_geometry():
        """
        Fixes PST geometry.

        :return: Nothing
        """

        if status[kt.mode].check('SHAPES_GEOMETRY', "PROBS"):
            # Epilogi olon ton shapefile enos provlimatikou OTA kai
            # epidiorthosi tis geometrias tous
            _data = load_json(paths.status_path)

            repaired = []

            for row in _data["SHAPES_GEOMETRY"]["OTA"]:
                ota_folder = str(row)
                repaired.append(str(ota_folder))
                for i in info.geometry_list:
                    lyr = paths.ktima(ota_folder, i, ext=True)

                    if os.path.exists(lyr):
                        pm("Repairing geometry in {}_{}".format(i, ota_folder))
                        arcpy.RepairGeometry_management(lyr, "KEEP_NULL")

            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix Geometry', log_list=repaired)

    @staticmethod
    def fbound_geometry():
        """
        Fixes FBOUND geometry.

        :return: Nothing
        """

        if status[kt.mode].check('FBOUND_GEOMETRY', "PROBS"):
            # Epidiorthosi ton FBOUND
            _data = load_json(paths.status_path)

            repaired = []

            for row in _data[kt.mode]["FBOUND_GEOMETRY"]["OTA"]:
                repair_ota = str(row)
                repaired.append(str(repair_ota))

                lyr = paths.ktima(repair_ota, "FBOUND", ext=True)

                if os.path.exists(lyr):
                    pm("  Repairing geometry in FBOUND_{}".format(repair_ota))
                    arcpy.RepairGeometry_management(lyr, "DELETE_NULL")

            status[kt.mode].update('SHAPE', 'FBOUND', False)
            pm("\nDONE !\n")
        else:
            pm("\nNothing to fix\n")
            repaired = "None"

        log('Fix FBOUND Geometry', log_list=repaired)

    @staticmethod
    def roads(buffer_dist, ignore_status=False, ignore_intersections=False):
        """
        Fixes ROADS.


        :param buffer_dist: float
            How much the shapefile will be buffered
        :param ignore_status: bool
            Whether or not to ignore ROADS current state.
        :param ignore_intersections: bool
            Whether or not to ignore intersections found from buffered polygon
        :return: Nothing
        """

        if status[kt.mode].check("ROADS", "CPROBS") or ignore_status:
            org.add_layer([ns.roadsM, ns.astenotM, ns.pstM])
            turn_off()
            # Kopsimo ton aksonon 10 cm prin to orio tis enotitas
            arcpy.Buffer_analysis(kt.gdb(ns.ek_check),
                                  kt.gdb(ns.ek_fixed_bound), buffer_dist)

            arcpy.Intersect_analysis([ns.roadsM, ns.ek_fixed_bound],
                                     kt.gdb(ns.intersections_after_fix),
                                     output_type="POINT",
                                     join_attributes="ONLY_FID")

            probs = get_count(ns.intersections_after_fix)

            if probs and not ignore_intersections:
                arcpy.SpatialJoin_analysis(ns.intersections_after_fix,
                                           ns.astenotM,
                                           kt.gdb(ns.intersections_astenot_rd),
                                           match_option="CLOSEST")

                if probs > 10:
                    arcpy.Dissolve_management(ns.intersections_astenot_rd,
                                              kt.gdb(ns.p_roads_after_fix),
                                              "CAD_ADMIN", "CAD_ADMIN COUNT")
                elif 0 < probs <= 10:
                    arcpy.SpatialJoin_analysis(ns.intersections_astenot_rd,
                                               ns.astenotM,
                                               kt.gdb(ns.p_roads_after_fix))

                pm('\n!! Task Aborted !!\n')
                pm('- {} intersections when cliping with {} buffer\n'.format(
                    probs, buffer_dist))
                pm('- For adjustments see: {} ({}.gdb)\n\n'.format(
                    ns.p_roads_after_fix, kt.mode))
            else:
                arcpy.Clip_analysis(kt.gdb(ns.roadsM),
                                    kt.gdb(ns.ek_fixed_bound),
                                    kt.gdb(ns.gdb_roads_all))

                status[kt.mode].update("EXPORTED", "ROADS", False)

                pm('\nROADS fixed\n')

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
    - asttom
    """

    def __init__(self):
        pass

    @staticmethod
    @mxd
    def pst():
        """
        Fixing PST fields for ORI_TYPE, DEC_ID, ADDRESS.

        :return: Nothing
        """

        # Diorthosi ton pedion ORI_TYPE, DEC_ID kai ADDRESS stous PST
        # me vasi tis prodiagrafes
        for lyr_pst in org.fetch('PST', missing='ignore'):
            if lyr_pst[-5:] in kt.otas:
                pm("  Processing {}".format(lyr_pst))
                arcpy.SelectLayerByAttribute_management(
                    lyr_pst,
                    "NEW_SELECTION",
                    " ORI_CODE = '' AND ORI_TYPE NOT IN (5,6) ")
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

    @staticmethod
    @mxd
    def asttom():
        """
        Deletes ACQ_SCALE field from ASTTOM.

        :return: Nothing
        """

        # Diagrafi ACQ_SCALE apo tous ASTTOM
        for lyr_asttom in org.fetch('ASTTOM', missing='ignore'):
            if lyr_asttom[-5:] in kt.otas:
                pm("  Processing {}".format(lyr_asttom))
                arcpy.DeleteField_management(lyr_asttom, "ACQ_SCALE", )

        pm("\nDONE !\n")

        log('Fields ASTTOM')

    @staticmethod
    @mxd
    def astenot():
        """
        Supplements LOCALITY field in ASTENOT.

        :return: Nothing
        """

        # Prosthiki onomasias sto pedio LOCALITY ton ASTENOT me vasi txt arxeio
        available_otas = org.fetch('ASTENOT', missing='ignore', ota_num=True)

        with open(paths.locality) as csvfile:
            localnames = csv.reader(csvfile)

            for row in localnames:
                try:
                    ota = row[0][:5]
                    if ota in available_otas:
                        lyr_astenot = toc_layer('ASTENOT', ota)
                        pm("  Processing {}".format(lyr_astenot))
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

    @staticmethod
    @mxd
    def fbound_docs():
        """
        Supplements DOC_ID field in ASTENOT.

        :return: Nothing
        """

        with open(paths.fbounddoc) as csvfile:
            docs = csv.reader(csvfile)

            for row in docs:
                try:
                    ota = row[0]
                    lyr_fbound = toc_layer('FBOUND', ota)
                    pm("\n  Processing DOC_ID in {}...\n".format(lyr_fbound))

                    arcpy.CalculateField_management(lyr_fbound,
                                                    "DOC_ID",
                                                    "'{}'".format(row[1]),
                                                    "PYTHON_9.3")
                except IndexError:
                    pm("Leipei DOC_ID gia {} apo to .txt arxeio".format(
                        ota))

        pm("\nDONE !\n")

        log('Fields FBOUND')


class Create:
    """
    Class Create has functions for creating shp_list.

    Methods
    -------
    - fbound
    - roads
    - fboundclaim
    - pre_fbound

    """

    def __init__(self):
        pass

    @staticmethod
    def fbound(which_po):
        """
        Creates FBOUND shp_list

        :param which_po: str
            Path for the chosen forest file to use
        :return: nothing
        """
        pm('\nCreating FBOUND using:\n-->{}\n'.format(which_po))

        if ktima_status('ASTOTA'):
            # Dhmiourgia tou sunolikou FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis([kt.gdb(ns.astotaM),
                                      which_po],
                                     kt.gdb(ns.gdb_fbound_all),
                                     output_type="INPUT",
                                     join_attributes='NO_FID')

            arcpy.FeatureClassToFeatureClass_conversion(
                kt.gdb(ns.gdb_fbound_all),
                paths.fboundoutpath,
                ns.fbound_all)

            turn_off()

            # # Dhmiourgia pinaka FBOUND vasi ton prodiagrafon
            arcpy.DeleteField_management(paths.fboundinpath,
                                         delete_fields(paths.fboundinpath,
                                                       keep=['CAD_ADMIN']))
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

                lyr_fbound = ns.fbound_all
                pm("\nProcessing DOC_ID in {}...\n".format(lyr_fbound))

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

            arcpy.SelectLayerByAttribute_management(ns.fbound_all,
                                                    "NEW_SELECTION",
                                                    " DOC_ID = '' ")

            if get_count(ns.fbound_all) != 0:
                pm("\n !!! Leipoun DOC_ID apo to FBOUND_ALL \n!!!")

            clear_selection(ns.fbound_all)

            arcpy.DeleteField_management(ns.fbound_all, "CAD_ADMIN")

            pm("Exporting FBOUND / OTA...\n")

            # Eksagogi FBOUND ana OTA
            general.export_per_ota(ns.fbound_all,
                                   spatial=True,
                                   spatial_method='location_within',
                                   formal=True,
                                   name="FBOUND")

            mdf(ns.fbound_all, importance='!')

            pm("\nDONE !\n")

            time_now = timestamp()

            status[kt.mode].update("EXPORTED", "FBOUND", True)
            status[kt.mode].update("SHAPE", "FBOUND", False)
            status[kt.mode].update("EXPORTED", "FBOUND_ED", time_now)

            log('Create FBOUND')

    @staticmethod
    def roads(ignore_status=False):
        """
        Creates ROADS.

        :param ignore_status: bool
            Whether or not to ignore ROADS current state.
        :return: Nothing
        """

        if status[kt.mode].check("ROADS", "CPROBS") or ignore_status:

            arcpy.FeatureClassToFeatureClass_conversion(
                kt.gdb(ns.gdb_roads_all),
                paths.rdoutpath, ns.roads_all)

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
            general.export_per_ota(ns.roads_all,
                                   spatial=True,
                                   spatial_method='location_within',
                                   formal=True,
                                   name="ROADS")

            mdf(ns.roads_all, importance='!')

            time_now = timestamp()

            status[kt.mode].update("SHAPE", "ROADS", False)
            status[kt.mode].update("EXPORTED", "ROADS", True)
            status[kt.mode].update("EXPORTED", "ROADS_ED", time_now)

            log('Create ROADS')

            pm("\nDONE !\n")
        else:
            pm('ROADS have no problem. No creation was performed')

    @staticmethod
    def fboundclaim():
        """
        Creates FOREST CLAIMS shp_list and mdb.

        :return: Nothing
        """

        if ktima_status('PST', 'FBOUND'):
            # Dhmiourgia tou pinaka tis diekdikisis tou dasous
            arcpy.Intersect_analysis(
                [kt.gdb(ns.pstM), kt.gdb(ns.fboundM)],
                kt.gdb(ns.intersection_pst_fbound),
                output_type="INPUT")
            arcpy.Dissolve_management(ns.intersection_pst_fbound,
                                      kt.gdb(ns.gdb_fbound_claim),
                                      ["KAEK", "AREA"])
            arcpy.FeatureClassToFeatureClass_conversion(ns.gdb_fbound_claim,
                                                        paths.claimoutpath,
                                                        ns.fbound_claim)

            turn_off()

            # Diagrafi eggrafon vasi tupikon prodiagrafon
            arcpy.SelectLayerByAttribute_management(ns.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " Shape_Area < 100 ")
            # Svinontai oles oi eggrafes kato apo 100 m2
            arcpy.DeleteRows_management(ns.fbound_claim)
            clear_selection(ns.fbound_claim)
            arcpy.AddField_management(ns.fbound_claim, "AREA_MEAS", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(ns.fbound_claim, "AREAFOREST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.AddField_management(ns.fbound_claim, "AREA_REST", "DOUBLE",
                                      field_precision=15, field_scale=3)
            arcpy.CalculateField_management(ns.fbound_claim, "AREA_MEAS",
                                            '!AREA!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(ns.fbound_claim, "AREAFOREST",
                                            '!Shape_Area!',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(ns.fbound_claim, "AREA_REST",
                                            '!AREA_MEAS! - !AREAFOREST!',
                                            "PYTHON_9.3")
            arcpy.AddField_management(ns.fbound_claim, "TYPE", "SHORT",
                                      field_precision=1)
            arcpy.SelectLayerByAttribute_management(ns.fbound_claim,
                                                    "NEW_SELECTION",
                                                    " AREA_REST < 1 ")
            # Oles oi eggrafes me AREA_REST kato apo 1 m2  diekdikountai pliros
            arcpy.CalculateField_management(ns.fbound_claim, "AREA_REST", '0',
                                            "PYTHON_9.3")
            arcpy.CalculateField_management(ns.fbound_claim, "TYPE", '1',
                                            "PYTHON_9.3")
            clear_selection(ns.fbound_claim)

            arcpy.DeleteField_management(ns.fbound_claim,
                                         delete_fields(ns.fbound_claim,
                                                       keep=['KAEK',
                                                             'AREA_MEAS',
                                                             'AREAFOREST',
                                                             'AREA_REST',
                                                             'TYPE']))

            count_claims = get_count(ns.fbound_claim)

            mdf(ns.fbound_claim, importance='!')
            arcpy.FeatureClassToFeatureClass_conversion(paths.claiminpath,
                                                        paths.mdb(),
                                                        ns.diekdikisi)

            pm(
                "\nDONE ! - Forest claiming {} KAEK.\n\n"
                "Don't forget to change AREAFOREST to AREA_FOREST\n".format(
                    count_claims))

            log('Create FBOUND Claims', log_list=count_claims)

            pm("\nDONE !\n")

    @staticmethod
    def pre_fbound():
        """
        Creates PRE_FBOUND shp_list.

        :return: Nothing
        """

        if ktima_status('ASTOTA'):
            # Dhmiourgia tou sunolikoy PRE_FBOUND me vasi ta nea oria ton OTA
            arcpy.Intersect_analysis(
                [kt.gdb(ns.astotaM), paths.predasinpath],
                kt.gdb(ns.gdb_pre_fbound_all),
                output_type="INPUT")
            arcpy.DeleteField_management(kt.gdb(ns.gdb_pre_fbound_all),
                                         ["FID_merge_ASTOTA",
                                          "FID_KYR_PO_PARCELS", "KATHGORDX",
                                          "KATHGORAL1", "AREA", "LEN",
                                          "CAD_ADMIN"])
            arcpy.FeatureClassToFeatureClass_conversion(
                kt.gdb(ns.gdb_pre_fbound_all),
                paths.fboundoutpath,
                ns.pre_fbound_all)

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
            general.export_per_ota(ns.pre_fbound_all,
                                   spatial=True, formal=True,
                                   name="FBOUND")

            mdf(ns.pre_fbound_all, importance='!')

            pm("\nDONE !\n")

            log('Create PRE_FBOUND')
        else:
            raise Exception("\n\n\n!!! Den exeis kanei MERGE !!!\n\n\n")


if __name__ == 'ktima.arc.core':
    geoprocessing = Geoprocessing()
    find = Queries()
    general = General()
    check = Check()
    fix = Fix()
    fields = Fields()
    create = Create()
