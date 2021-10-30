"""
Fetch all files from Kortforsyningen FTP server folder.

Copyright (c) 2021 Peter Fogh

See also command line alternative in `download_dk_dem.sh`
"""
from ftplib import FTP, error_perm
import os
from pathlib import Path
import time
import operator
import functools
import shutil
# TODO: use logging to std instead of print(time.ctime())

from environs import Env


# Functions
def download_FTP_tree(ftp, remote_dir, local_dir):
    """
    Download FTP directory and all content to local directory.

    Inspired by https://stackoverflow.com/a/55127679/7796217.

    Parameters:
        ftp : ftplib.FTP
            Established FTP connection after login.
        remote_dir : pathlib.Path
            FTP directory to download.
        local_dir : pathlib.Path
            Local directory to store downloaded content.

    """
    # Set up empty local dir and FTP current work dir before tree traversal.
    shutil.rmtree(local_dir)
    ftp.cwd(remote_dir.parent.as_posix())
    local_dir.mkdir(parents=True, exist_ok=True)
    return _recursive_download_FTP_tree(ftp, remote_dir, local_dir)


def _is_ftp_dir(ftp, name):
    """
    Check if FTP entry is a directory.
    Modified from here https://www.daniweb.com/programming/software-development/threads/243712/ftplib-isdir-or-isfile
    to accommodate not necessarily being in the top-level directory.

    Parameters:
        ftp : ftplib.FTP
            Established FTP connection after login.
        name: str
            Name of FTP file system entry to check if directory or not.

    """
    try:
        current_dir = ftp.pwd()
        ftp.cwd(name)
        #print(f'File system entry "{name=}" is a directory.')
        ftp.cwd(current_dir)
        return True
    except error_perm as e:
        #print(f'File system entry "{name=}" is a file.')
        return False


def _recursive_download_FTP_tree(ftp, remote_dir, local_dir):
    """
    Download FTP directory and all content to local directory.

    Inspired by https://stackoverflow.com/a/55127679/7796217.

    Parameters:
        ftp : ftplib.FTP
            Established FTP connection after login.
        remote_dir : pathlib.Path
            FTP directory to download.
        local_dir : pathlib.Path
            Local directory to store downloaded content.

    """
    print(f'{remote_dir=}')
    print(f'{local_dir=}')
    ftp.cwd(remote_dir.name)
    local_dir.mkdir(exist_ok=True)

    print(f'{time.ctime()}: Fetching file & directory names within "{remote_dir}".')
    dir_entries = ftp.nlst()
    print(f'{time.ctime()}: Fetched file & directory names within "{remote_dir}".')
    dirs = []
    for filename in sorted(dir_entries)[-5:]:  # TODO: remove restriction on downloaded of entries 
        if _is_ftp_dir(ftp, filename):
            dirs.append(filename)
        else:
            local_file = local_dir/filename
            print(f'{time.ctime()}: Downloading "{local_file}".')
            ftp.retrbinary(
                cmd=f'RETR {filename}',
                callback=local_file.open('wb').write)
            print(f'{time.ctime()}: Downloaded "{local_file}".')
            
    print(f'Traverse dir tree to "{dirs=}"')
    map_download_FTP_tree = map(lambda dir: _recursive_download_FTP_tree(
        ftp, remote_dir/dir, local_dir/dir), dirs)
    return functools.reduce(operator.iand, map_download_FTP_tree, True)


if __name__ == '__main__':
    # Load environment variables from local `.env` file.
    env = Env()
    env.read_env()

    # Set up server and source/destination paths.
    ftp_host = 'ftp.kortforsyningen.dk'
    dem_ftp_dir = Path('dhm_danmarks_hoejdemodel/DTM')
    local_ftp_dir = env.path('LOCAL_FTP_DIR', './')
    local_dem_ftp_dir = local_ftp_dir/'kortforsyningen'/dem_ftp_dir

    # Perform FTP download.
    print(f'{time.ctime()}: Connect to {ftp_host}')
    ftp = FTP(ftp_host)
    ftp.login(env('KORTFORSYNING_USERNAME'), env('KORTFORSYNING_PASSWORD'))
    download_FTP_tree(ftp, dem_ftp_dir, local_dem_ftp_dir)
    ftp.close()
    print(f'{time.ctime()}: Finished')
