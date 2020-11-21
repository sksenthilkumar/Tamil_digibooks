import subprocess
import pathlib
import glob
from tqdm import tqdm

from subprocess import Popen, PIPE


def get_sub_folders(path):
    fo = f"{path}/*"
    return glob.glob(fo)


def get_zip_files(path):
    fo = f"{path}/*.zip"
    return glob.glob(fo)


def unzip_file(zip_file, target, verbose=False):
    cmd = f'unzip {zip_file} -d {target}'
    if verbose:
        print(f"Executing Command {cmd}")
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if verbose:
        print(f"Command Execution Outputs{output}")


def unzip_files_in_a_dir(dir, verbose=False):
    unzip_files = []
    print(f"Unzipping folders in {dir}")
    for file in tqdm(get_zip_files(dir)):
        book_name = pathlib.Path(file).stem.split('-')[0]
        target = f'{dir}/{book_name}'
        unzip_file(file, target=target, verbose=verbose)
        unzip_files.append(target)

    return unzip_files


if __name__ == '__main__':
    fol = "/home/senthil/tamil_digital_books_library/downloads_20200927"
    unzip_files_in_a_dir(fol)



