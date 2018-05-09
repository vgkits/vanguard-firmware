import os
import command


def upload_imports():
    script_dir_path = os.path.dirname(os.path.realpath(__file__))
    modules_dir_path = os.path.realpath(script_dir_path + os.path.sep + '../../modules')
    command.rsync(modules_dir_path, '')


def run():
    upload_imports()


if __name__ == "__main__":
    run()
