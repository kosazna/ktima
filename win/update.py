# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.paths import *
import fnmatch


toolboxes = ["A) General",
             "B) Check",
             "C) Fix",
             "D) Create"]


def update_from_server(folder):
    src = cp([mdev, 'Diafora', 'logs', 'scripts'], origin=folder)
    dst_c = ['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima']
    dst_t = ['Program Files (x86)', 'ArcGIS', 'Desktop10.1', 'Tools', 'KT-Tools']

    for rootDir, subdirs, filenames in os.walk(src):
        for filename in fnmatch.filter(filenames, '*py'):
            basename = os.path.splitext(filename)[0]
            if basename in toolboxes:
                inpath = os.path.join(rootDir, filename)
                outpath = os.path.join(cp(dst_t), '{}.pyt'.format(basename))
                c_copy(inpath, outpath)
            else:
                inpath = os.path.join(rootDir, filename)
                out = dst_c + inpath.split('\\')[5:]
                outpath = cp(out)
                c_copy(inpath, outpath)


def main(_func, _action):
    def all_files(__action):
        src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima'])
        dst = ['Google Drive', 'Work', 'ktima', 'ktima 5']

        for rootDir, subdirs, filenames in os.walk(src):
            for filename in fnmatch.filter(filenames, '*py'):
                inpath = os.path.join(rootDir, filename)
                out = dst + inpath.split('\\')[6:]
                outpath = cp(out, origin=gd[user])

                if __action == 'push':
                    c_copy(inpath, outpath)
                else:
                    c_copy(outpath, inpath)

    def tools():
        src = cp(['Python27', 'ArcGIS10.1', 'Lib', 'site-packages', 'ktima', '!Toolboxes'])
        dst_t = ['Program Files (x86)', 'ArcGIS', 'Desktop10.1', 'Tools', 'KT-Tools']

        for rootDir, subdirs, filenames in os.walk(src):
            for filename in fnmatch.filter(filenames, '*py'):
                basename = os.path.splitext(filename)[0]
                inpath = os.path.join(rootDir, filename)
                outpath = os.path.join(cp(dst_t), '{}.pyt'.format(basename))
                c_copy(inpath, outpath)

    if _func == "all_files":
        all_files(_action)
    else:
        tools()


if __name__ == "__main__":
    func = str(sys.argv[1])
    action = str(sys.argv[2])
    main(func, action)
