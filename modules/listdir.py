import os


def run(options):
    print('[*] Listdir module.')

    files = os.listdir('.')

    print('[*] Success!')

    return str(files)
