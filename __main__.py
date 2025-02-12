from pathlib import Path
from platform import system as operating_system
from subprocess import run
from sys import path
from os import mkdir
from shutil import rmtree
from zipfile import ZipFile
from zipimport import zipimporter

BASE_DIR_PATH,BASE_DIR_NAME = path[0],path[0].split(".")[0]

def server():
        ...
        if operating_system().lower().startswith("linux"):
            print(f"Running : [ {operating_system()} ]\n")
            return run("supervisord",cwd=BASE_DIR_NAME)
        elif operating_system().lower().startswith("window"):
            print(f"Running : [ {operating_system()} ]\n")
            return run("python manage.py runserver",cwd=BASE_DIR_NAME)
        
if __name__ == "__main__":
    ...
    
    try:
        mkdir(BASE_DIR_NAME)
    except FileExistsError:
    
        print(f"Removing: {BASE_DIR_NAME}")
        rmtree(f'{BASE_DIR_NAME}')
        mkdir(BASE_DIR_NAME)
        print(f"Created: {BASE_DIR_NAME}")



    with ZipFile(BASE_DIR_PATH) as extract_all_zip_files:
        ...
        extract_all_zip_files.extractall(BASE_DIR_NAME)
        server()

    