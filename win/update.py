# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module has all the functions for updating the project on google
# drive and update the users scripts from the server

from ktima.handler import *


toolboxes = ["A) General",
             "B) Check",
             "C) Fix",
             "D) Create"]


def update_from_server(drive=ktl['temp'][USER]):
    """
    Updates all the USER scripts from the company server.

    :param drive: **str**, optional
        Drive letter of the server.
        (default: is defined on the paths.json file for each USER)
    :return: Nothing
    """

    if ktl.get('company_name', 'NOT_FOUND') == c_NA:
        src = cp(temp_NA, origin=drive)
    elif ktl.get('company_name', 'NOT_FOUND') == c_2P:
        src = cp(temp_2P, origin=drive)
    else:
        print('"company_name" not defined in paths.json')
        return

    dst_c = ktima_local
    dst_t = toolboxes_local

    pointer = len(src.split('\\'))

    for fullpath, filename, basename, ext in list_dir(src, match=['.py',
                                                                  '.pyt']):
        if ext == '.py':
            out = dst_c + fullpath.split('\\')[pointer:]
            outpath = cp(out)
            c_copy(fullpath, outpath)
        elif ext == '.pyt':
            outpath = os.path.join(cp(dst_t), filename)
            c_copy(fullpath, outpath)


def main(command, gd_action):
    """
    Main function of update module.
    It either pushes or pulls scripts for the google drive.
    It also updates python toolboxes in ArcGIS

    :param command: **str**,
        - 'all_files': update files from or to google drive.
        - 'tools': update python toolboxes
    :param gd_action: **str**
        - 'push': updates scripts on google drive from the cwd.
        - 'pull': fetches update from the google drive into the cwd.
    :return: Nothing
    """

    def all_files(_action):
        src = cp(ktima_local)
        dst = ktima_gd

        pointer = len(src.split('\\'))

        for fullpath, filename, basename, ext in list_dir(src, match='.py'):
            out = dst + fullpath.split('\\')[pointer:]
            outpath = cp(out, origin=gd[USER])

            if _action == 'push':
                c_copy(fullpath, outpath)
            else:
                c_copy(outpath, fullpath)

    def tools():
        src = cp(toolboxes_ktima)
        dst_t = toolboxes_local

        for fullpath, filename, basename, ext in list_dir(src, match='.py'):
            outpath = os.path.join(cp(dst_t), '{}.pyt'.format(basename))

            c_copy(fullpath, outpath)

    if command == "all_files":
        all_files(gd_action)
    else:
        tools()


if __name__ == "__main__":
    func = str(sys.argv[1])
    action = str(sys.argv[2])
    main(func, action)
