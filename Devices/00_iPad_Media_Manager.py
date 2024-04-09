###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        01_iPad_Media_Manager.py
# created:     19.08.2023 14:30
# edited:      15.10.2023 15:10
# Description: The "iPad Media Manager" script is a versatile and efficient
#              tool designed to simplify the organization and management of
#              photos and videos captured using an iPhone or similar devices.
#              Key features are:
#                   * File Organization (move files into different folder)
#                   * File Renaming using exiftool (day and time tag)
#                   * Cleanup and Optimization (deletes unused folder)
#
# Usage:       1. Copy all files from iPad to your hard-drive
#              2. Run the script using "python 01_iPad_Media_Manager.py"
#              3. Insert the path of the just copied iPad photos
#              4. Let the script to it's things and check the result.
#              5. Sort all pics which are not into a folder
#              6. Merge the screenshot and edit folder and delete the
#                 uncut (orginal) screenshots
#
# Comments:    * Make sure that imagemagick and exiftool is installed.
#              * some dates does not fit to the real creation date - I used the 
#                FileModifyDate - Tag instead.
#
# Todo:        * delete all unedited (uncut) duplicates!
#                e.g. 'PAD_2023-04-18_081110_edit' and 'PAD_2023-04-18_081110'
#                      the unedited one (PAD_2023-04-18_081110) should be deleted
#                      after screenshot and edit folder are marged together.
#
# Resources:   https://www.mysysadmintips.com/windows/clients/967-rename-iphone-mov-videos-to-date-and-time-taken
#              https://imagemagick.org/script/download.php
#              https://exiftool.org/examples.html
#              https://exiftool.org/
#
################################################################################

import os
import shutil
import subprocess

jpg_folder = None
edit_folder = None
vids_folder = None
aae_folder = None
screenshot_folder = None


def init_folders(source_folder):
    global jpg_folder, edit_folder, vids_folder, aae_folder, screenshot_folder

    jpg_folder = os.path.join(source_folder, 'pics')
    edit_folder = os.path.join(source_folder, 'edit')
    vids_folder = os.path.join(source_folder, 'vids')
    aae_folder = os.path.join(source_folder, 'aae')
    screenshot_folder = os.path.join(source_folder, 'screenshots')


def create_folders():
    global jpg_folder, edit_folder, vids_folder, aae_folder, screenshot_folder

    # Create destination folders if they don't exist
    for folder in [jpg_folder, edit_folder, vids_folder, aae_folder, screenshot_folder]:
        os.makedirs(folder, exist_ok=True)
    print("Folders are created sucessfully")

def organize_files(source_folder):  
    jpg_count = 0
    edit_count = 0
    vids_count = 0
    aae_count = 0
    screenshot_count = 0

    # List all files in the source folder
    files = os.listdir(source_folder)

    for file in files:
        if file.endswith('.JPG'):
            if file.startswith('IMG_E'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(edit_folder, file))
                edit_count += 1
            elif file.startswith('IMG_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
        elif file.endswith('.MOV'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(vids_folder, file))
            vids_count += 1
        elif file.endswith('.AAE'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(aae_folder, file))
            aae_count += 1
        elif file.endswith('.PNG'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(screenshot_folder, file))
            screenshot_count += 1

    print(f"\t{jpg_count} files moved to 'pics' folder")
    print(f"\t{edit_count} files moved to 'edit' folder")
    print(f"\t{vids_count} files moved to 'vids' folder")
    print(f"\t{aae_count} files moved to 'aae' folder")
    print(f"\t{screenshot_count} files moved to 'screenshots' folder")


def rename_files():
    global jpg_folder, edit_folder, vids_folder, screenshot_folder
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", "PAD_%Y-%m-%d_%H%M%S%%-c.%%le", jpg_folder])
    subprocess.run(["exiftool", "-ext", "png", "-FileName<DateCreated",
                   "-d", "PAD_%Y-%m-%d_%H%M%S%%-c.%%le", screenshot_folder])
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<FileModifyDate",
                   "-d", "PAD_%Y-%m-%d_%H%M%S%%-c_edit.%%le", edit_folder])
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "mov",
                   "-d", "PAD_%Y-%m-%d_%H%M%S%%-c.%%le", "-filename<CreateDate", vids_folder])

def delete_aae_folder():
    global aae_folder, edit_folder
    if len(os.listdir(aae_folder)) == len(os.listdir(edit_folder)):
        shutil.rmtree(aae_folder)
        print("\tAAE-Folder removed successfully")
    else:
        print("\tERROR:Number of aae-Files is not the euqal to edited-Files - Check it")


def merge_edit_folder():
    global edit_folder, screenshot_folder

    edit_files = os.listdir(edit_folder)
    for edit_file in edit_files:
        shutil.move(os.path.join(edit_folder, edit_file), os.path.join(screenshot_folder, edit_file))

    print(f"\t{len(edit_files)} files moved from 'edit' folder to 'screenshot' folder")


def delete_original_before_edit(): # delete unedited original screeenshot before edited scrrenshot
    global screenshot_folder

    screenshot_files = sorted(os.listdir(screenshot_folder))
    files_to_delete = []

    for i in range(len(screenshot_files) - 1):
        current_file = screenshot_files[i]
        next_file = screenshot_files[i + 1]
        
        if current_file.endswith('_edit.jpg'):
            continue
        
        if next_file.endswith('_edit.jpg'):
            files_to_delete.append(current_file)

    for file_to_delete in files_to_delete:
        os.remove(os.path.join(screenshot_folder, file_to_delete))
        print(f"\tDeleted: {file_to_delete}")
    print(f"\t{len(files_to_delete)} Files got deleted.")

def delete_unused_folder():
    global source_folder, aae_folder, edit_folder, jpg_folder, vids_folder
    
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"\tDeleted empty folder: {folder_path}")


if __name__ == "__main__":
    source_folder = input("Enter the path of the folder with photos and videos: ")

    init_folders(source_folder)

    input("\nPress Enter to create subfolders...")
    create_folders()

    input("\nPress Enter to organize files...")
    organize_files(source_folder)

    input("\nPress Enter to rename files...")
    rename_files()

    input("\nPress Enter to delete 'aae' folder...")
    delete_aae_folder()

    input("\nPress Enter to merge 'edit' folder...")
    merge_edit_folder()

    input("\nPress Enter to delete the uncut original items...")
    delete_original_before_edit()

    input("\nPress Enter to delete unused folders...")
    delete_unused_folder()

    print("\n\n----------------------DONE--------------------")
    print("Files organized, renamed, merged and unused files and folders are deleted successfully.")
