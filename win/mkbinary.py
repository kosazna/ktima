# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# Module is being used to compile python code to pyc files
# so that it can be delivered to the production

import py_compile
from ktima.handler import *
from update import toolboxes


def compile_ktima():
    """
    Compiles the entire codebase except from some files.

    :return: Nothing
    """

    # FILES TO NOT BE COMPILED
    no_compile = ['testing', 'pass', 'mkbinary']

    # SOURCE CODE PATH
    src = cp([users, USER, 'Desktop', 'compiled code'])

    for fullpath, filename, basename, ext in list_dir(src, match='.py'):
        if basename not in toolboxes and basename not in no_compile:
            py_compile.compile(fullpath, doraise=True)
            os.remove(fullpath)
        elif basename in toolboxes:
            relative = os.path.split(fullpath)[0]
            new_path = os.path.join(relative, '{}.pyt'.format(basename))
            os.rename(fullpath, new_path)
        else:
            os.remove(fullpath)


if __name__ == "__main__":
    compile_ktima()
