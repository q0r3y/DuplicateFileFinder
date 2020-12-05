'''
    Author: q0r3y
    Date: 12.05.20
    Description:
        This python script scans files in the given directory,
        and checks for duplicates by checking the md5 of each file.
        It was compiled with: pyinstaller --onefile duplicate-checker.py
'''

import hashlib
import os
import time
import sys

# Gets an md5 checksum from the input filename
def get_md5_checksum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

# Returns a dictionary of all the filepaths in the input dir
def get_dir_filenames(directory):
    file_md5_dict = {}
    filecheck_counter = 0
    exclude = set(['AppData', 'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Microsoft'])
    print(' [-] Excluding: Hidden folders, AppData, Windows, Program Files\n')
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if not d[0] == '.' and d not in exclude]
        files = [f for f in files if not f[0] == '.']
        for file in files:
            full_path = os.path.join(root, file)
            print(full_path)
            file_md5_dict[full_path] = ''
            filecheck_counter += 1
    print('\n [+] Retrieved all file names in directory..')
    print(' [+] Scanned '+str(filecheck_counter)+' files.\n')
    return file_md5_dict

# Recieves a dictionary of filepaths and computes checksums for all those files
def get_file_checksums(file_dict):
    file_md5_dict = {}
    checksum_counter = 0;
    for file_name in file_dict.keys():
        try:
            md5_checksum = get_md5_checksum(file_name)
            checksum_counter += 1
            print(md5_checksum)
            if md5_checksum not in file_md5_dict:
                file_md5_dict[md5_checksum] = [file_name]
            else:
                file_md5_dict[md5_checksum].append(file_name)
        except Exception as e:
            pass
    print('\n [+] Calculated '+str(checksum_counter)+' file checksums..\n')
    return file_md5_dict

# Checks for duplicates in the input file : md5sum dictionary
def check_for_duplicates(file_md5_dict):
    duplicate_counter = 0
    duplicate_files = []
    for file_list in file_md5_dict.values():
        if len(file_list) > 1:
            duplicate_counter += 1
            for file_name in file_list:
                duplicate_files.append(file_name)
                print(file_name)
            duplicate_files.append(' ') #Adds blank line to end of list for log
    print('\n [*] Found '+str(duplicate_counter)+' sets of duplicates.')
    return duplicate_files

# Saves a log to the users desktop listing the duplicate files
def save_file(duplicate_list):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filename = '\\duplicate_log.txt'
    try:
        with open(desktop+filename, 'a') as log_file:
            for item in duplicate_list:
                log_file.write('\n')
                log_file.write(item)
            log_file.write('\n-----------Duplicate-files-appear-in-groups-----------\n')
        print(' [+] Saved log file: '+desktop+filename+'')
    except Exception as e:
        print(e)

def main():
    directory_start = str(input("\n[+] Input a starting directory (enter to scan C: drive): ") or "C:")

    while not os.path.isdir(directory_start):
        print(' [-] The directory: '+directory_start+' - is invalid.')
        directory_start = str(input(" [+] Enter a starting directory (C:\\User\\..): "))

    if os.path.isdir(directory_start):
        file_md5_dict = get_dir_filenames(directory_start)
        time.sleep(3)
        file_md5_dict = get_file_checksums(file_md5_dict)
        duplicates = check_for_duplicates(file_md5_dict)
        save_file(duplicates)

        print("\n Press enter key to close..")
        input()

main()
