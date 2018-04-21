import numpy as np
import fingerprintWorker as fw
import pickle
import os

EXPORT_PATH = 'C:\\Users\\Vlad\\Documents\\thesis\\audioExtraction\\exported_grids'
old_root        = 'C:\\Users\\Vlad\Documents\\thesis\\audioExtraction\\wavs'
exteral_root    = 'D:\\thesis-data'
db_test         = 'D:\\db_test'
mp3_test        = 'C:\\Users\\Vlad\Documents\\thesis\\audioExtraction\\mp3_test'
flac_test       = 'C:\\Users\\Vlad\Documents\\thesis\\audioExtraction\\flac_test'


##### supported audio encodings #####
VALID_EXT   = ['.wav', '.ogg', '.mp3', '.flac', '.grid', '.mpeg']
CUSTOM_EXT  = '.grid'


##### DIRECTORY STRUCTURE METHODS #####


def _get_dir_structure(dir_path):
    """Returns all stored files"""
    files = []

    for (dirpath, dirname, filenames) in os.walk(dir_path):
        files.append([dirpath, filenames])

    return files


def has_valid_extension(path_to_file):
    path, ext = os.path.splitext(path_to_file)
    if ext in VALID_EXT:
        return True
    return False


def build_dir_map(root):
    """creates a dictionary directory structure.
    It maps files to their relative path.

    file.wav -> c//dir/dir2/dir_with_wavs

    Attributes:
        root - where to start looking

    Return:
        map  - dictionary structure
    """
    dir_struct = _get_dir_structure(root)
    map = dict()

    for tup in dir_struct:
        current_directory = tup[0]
        files_in_dir      = tup[1]

        for f in files_in_dir:
            relative_path = current_directory + '\\' + f
            # add key if not already in dict and if file has a valid extension
            if f not in map and has_valid_extension(relative_path):
                map[f] = current_directory

    return map


##### IO METHODS #####


def export_file(file_name, data, dest_dir=EXPORT_PATH):
    name = file_name[:-4] + CUSTOM_EXT
    path = dest_dir + '\\' + name

    with open(path, mode='wb') as f:
        try:
            pickle.dump(data, f)
            f.close()
            print('Exported: {}'.format(name))
        except:
            print('Export failed: {}'.format(name))


def load_grid(file_name, local_dir=EXPORT_PATH):
    path = local_dir + '\\' + file_name
    filename, ext = os.path.splitext(path)

    if ext != CUSTOM_EXT:
        path = path[:-len(ext)] + CUSTOM_EXT

    with open(path, 'rb') as f:
        data = pickle.load(f)

    return data


if __name__=='__main__':
    m = build_dir_map(exteral_root)
    alread_done = build_dir_map(EXPORT_PATH)

    fw.fgp_api.set_grid_attributes(150, 150, 60, 60)

    for k in m.keys():
        grd_k = k[:-4] + '.grid'
        if grd_k not in alread_done.keys():
            _file_name = k
            _path      = m[_file_name] + '\\' + _file_name
            if has_valid_extension(_path):
                # print(_file_name, _path)
                data = fw.fingerprint_worker(_path, grid_only=True)

                export_file(_file_name, data, dest_dir=EXPORT_PATH)
        else:
            print('Skipped: {}'.format(k))