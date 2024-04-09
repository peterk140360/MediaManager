###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        02_OnePlus_merge-folder.py
# created:     31.10.2023 12:17
# edited:      -
# Description: The "OnePlus merge folder" script just comibines renamed pictures and videos
#              together, so that in the "09-18" folder are files together instead of seperated
#              into the "pics" and "vids" folder. The edit folder stays as it is.
#
# Usage:       1. simply run the 01_OnePlus Media Manager 
#              2. Run the script using "python 02_OnePlus_merge-folder.py"
#              3. Insert the path of the renamed and sorted OnePlus photos
#              4. Let the script to it's things and check the result.
#
# Comments:    -
#
# Todo:        - 
#        
#
#
# Resources:   -
#
################################################################################

import os
from re import S
import shutil

def merge_folders(source_folder):
    merged_files_count = 0
    for root, _, files in os.walk(source_folder):
        if root != source_folder and "edit" not in root:
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(source_folder, file)
                shutil.move(source_path, destination_path)
                merged_files_count += 1
            #shutil.rmtree(root)
    print(f"\n{merged_files_count} files got merged.\n")


def delete_unused_folder(source_folder):
      for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"\tDeleted empty folder: {folder_path}")

def extract_edit_files(source_folder):
    extract_files_count = 0
    edit_folder = os.path.join(source_folder, "edit")
    os.makedirs(edit_folder, exist_ok=True)

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.__contains__("_edit"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(edit_folder, file)
                shutil.move(source_path, destination_path)
                extract_files_count += 1

    print(f"\n{extract_files_count} files got extracted.\n")
    

if __name__ == "__main__":
    source_folder = input("Enter the path of the folder with photos and videos: ")

    input("\nPress Enter to merge files and delete folders...")
    merge_folders(source_folder)  
    
    input("\nPress Enter to extract edit files...")
    extract_edit_files(source_folder)

    input("\nPress Enter delete folders...")
    delete_unused_folder(source_folder)
    
    print("\n----------------------DONE--------------------")