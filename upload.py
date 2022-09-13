# script to upload website from pc to server
import os
import pathlib
import pysftp
import yaml

# data
# TODO make config file for this data and make it safer
with open(r'config.yaml') as file:
    config = yaml.full_load(file)
host = config['host']
port = config['port']
username = config['username']
password = config['password']

# functions

def only_files(dir_path):
    '''Check if dir contains only files'''
    if os.listdir(dir_path) == []:
        return False
    for entry in os.scandir(dir_path):
        if os.path.isdir(entry):
            return False
    return True

def get_full_dir_path(old_dir, new_dir):
    '''Create full dir path from different elements'''
    if old_dir.name == "":
        full_path = new_dir.name
    else:
        full_path = old_dir.name + "/" + new_dir.name
    return full_path

def upload_files(entry, dir_path):
    for file in os.scandir(entry):
        remote = get_full_dir_path(dir_path, entry) + "/" + file.name
        conn.put(file, remote, preserve_mtime=True)
    print(f"All files in {dir_path.name} have been uploaded.")

def recursive_upload(dir_path):
    for entry in os.scandir(dir_path):
        full_dir_path = get_full_dir_path(dir_path, entry)
        if os.path.isdir(full_dir_path):
            if not conn.exists(full_dir_path):
                print(f"Creating directory {entry.name}...")
                conn.mkdir(full_dir_path)
            print(f"Recursion over dir {full_dir_path}")
            # recursion
            # base case: dir has no elements
            if os.listdir(entry) == []:
                print(f"Dir {entry.name} is empty. Skipping...")
            # basecase 2: dir has only files
            if only_files(entry) == True:
                print(f"Uploading files to directory {entry.name}")
                upload_files(entry, dir_path)
            # DIMINISHING CASE
            else:
                print(f"Folder {entry.name} contains both files and folders. Recursively walking over it.")
                recursive_upload(entry)
        else:
            if dir_path.name == "":
                print(f'Uploading file {entry.name} in root dir...')
                conn.put(entry, preserve_mtime=True)
            else:
                print(f'Uploading file {entry.name} in subdir {dir_path.name}...')
                remote_path = dir_path.name  + "/" + entry.name
                conn.put(entry, remote_path, preserve_mtime=True)

# execution

try:
    conn = pysftp.Connection(host=host, port=port, username=username, 
    password=password) #  cnopts=cnopts
    print("Connection successfully established.")
except:
    print("Failed to establish connection to server.")
# Local file path
LOCAL_PATH = 'html'
# Target path
REMOTE_PATH = 'vhosts/n.svrns.com/htdocs/'

try:
    with pysftp.cd(LOCAL_PATH):
        conn.cwd(REMOTE_PATH)
        recursive_upload(pathlib.Path('.'))
        print("Your website has successfully been uploaded.")
except IOError:
        print('Target path not found.')
except OSError:
        print('Local path not found.')
except:
        print("Cannot upload file(s).")
conn.close()