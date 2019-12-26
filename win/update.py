# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.handler import *


toolboxes = ["A) General",
             "B) Check",
             "C) Fix",
             "D) Create"]


def update_from_server(folder=ktl['temp'][user]):
    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        src = cp([mdev, 'Diafora', 'ktima', 'scripts'], origin=folder)
    else:
        src = cp([temp_2kp, mdev, 'Diafora', 'ktima', 'scripts'], origin=folder)

    dst_c = ['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']
    dst_t = ['Program Files (x86)', 'ArcGIS', 'Desktop10.1', 'Tools', 'KT-Tools']

    def d_copy(x):
        for fullpath, filename, basename, ext in list_dir(src, match=['.pyc', '.pyt']):
            if ext == '.pyc':
                out = dst_c + fullpath.split('\\')[x:]
                outpath = cp(out)
                c_copy(fullpath, outpath)
            elif ext == '.pyt':
                outpath = os.path.join(cp(dst_t), filename)
                c_copy(fullpath, outpath)

    if ktl.get('company_name', 'NOT_FOUND') == 'NAMA':
        d_copy(5)
    elif ktl.get('company_name', 'NOT_FOUND') == '2KP':
        d_copy(6)
    else:
        print('"company_name" not defined in paths.json')


def main(_func, _action):
    def all_files(__action):
        src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
        dst = ['Google Drive', 'Work', 'ktima', 'ktima_6']

        for fullpath, filename, basename, ext in list_dir(src, match='.py'):
            out = dst + fullpath.split('\\')[6:]
            outpath = cp(out, origin=gd[user])

            if __action == 'push':
                c_copy(fullpath, outpath)
            else:
                c_copy(outpath, fullpath)

    def tools():
        src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima', '!Toolboxes'])
        dst_t = ['Program Files (x86)', 'ArcGIS', 'Desktop10.1', 'Tools', 'KT-Tools']

        for fullpath, filename, basename, ext in list_dir(src):
            outpath = os.path.join(cp(dst_t), '{}.pyt'.format(basename))
            c_copy(fullpath, outpath)

    if _func == "all_files":
        all_files(_action)
    else:
        tools()


if __name__ == "__main__":
    func = str(sys.argv[1])
    action = str(sys.argv[2])
    main(func, action)
