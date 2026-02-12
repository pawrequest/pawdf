import subprocess
from pathlib import Path

from context_menu import menus

from .array_p import array_pdfs

MENU_NAME = 'Array and Print PDF'
EXE_PATH = r"R:\paul_r\array_p.exe"


def process_file(filenames, params):
    print('process file')
    print(filenames, params)
    for filename in filenames:
        try:
            print(f'Processing {filename}')
            array_pdfs(Path(filename), print_files=True)
            print(f'Processed {filename}')
        except Exception as e:
            print('ERROR :', e)
        finally:
            input('Press Enter to continue...')


def remove_menu(name=MENU_NAME):
    try:
        menus.removeMenu(name, 'FILES')
    except Exception as e:
        print('ERRROR', e)


def add_menu(name=MENU_NAME):
    try:
        fc = menus.FastCommand(name, type='FILES', python=process_file)
        fc.compile()
    except Exception as e:
        print('ERRROR', e)
