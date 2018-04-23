import sys, os
from string import Template
from ampy import pyboard, cli

import command


def upload_server_files():
    script_dir_path = os.path.dirname(os.path.realpath(__file__))

    bootPath = 'boot.py'
    zippedPath = 'webrepl-inlined.html.gz'

    command.putFile(script_dir_path + os.path.sep + bootPath, bootPath)
    command.putFile(script_dir_path + os.path.sep + zippedPath, zippedPath)


def run():
    upload_server_files()


if __name__ == "__main__":
    run()
