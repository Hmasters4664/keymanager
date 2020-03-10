from pykeepass import PyKeePass

import shutil


def createfile(filename):
    shutil.copy2('/media/original.kdbx', filename)
