###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        01_OnePlus_Media_Manager
# created:     18.08.2023 18:30
# edited:      15.10.2023 15:10
#              20.10.2023 11:30
# Description: The "OnePlus Media Manager" script is a versatile and efficient
#              tool designed to simplify the organization and management of
#              photos and videos captured using an OnePlus or similar devices.
#              Key features are:
#                   * File Organization (move files into different folder)
#                   * File Renaming using exiftool (day and time tag)
#                   * Cleanup and Optimization (deletes unused folder)
#
# Usage:       1. Copy all files from OnePlus to your hard-drive
#              2. Run the script using "python 01_OnePlus_Media_Manager"
#              3. Insert the path of the just copied OnePlus photos
#              4. Let the script to it's things and check the result.
#
# Comments:    Make sure that imagemagick and exiftool is installed.
#
# Todo:        delete Live-Photo videos which got air-droped (videos with no length) 
#        
#
#
# Resources:   https://www.mysysadmintips.com/windows/clients/967-rename-iphone-mov-videos-to-date-and-time-taken
#              https://imagemagick.org/script/download.php
#              https://exiftool.org/examples.html
#              https://exiftool.org/
#
################################################################################

import os
import re
import shutil
import subprocess

jpg_folder = None
edit_folder = None
vids_folder = None
screenshot_folder = None
converted_jpg_folder = None
conversion_count = 0


def init_folders(source_folder):
    global jpg_folder, edit_folder, vids_folder, screenshot_folder

    jpg_folder = os.path.join(source_folder, 'pics')
    edit_folder = os.path.join(source_folder, 'edit')
    vids_folder = os.path.join(source_folder, 'vids')
    screenshot_folder = os.path.join(source_folder, 'screenshots')


def create_folders():
    global jpg_folder, edit_folder, vids_folder, screenshot_folder

    # Create destination folders if they don't exist
    for folder in [jpg_folder, edit_folder, vids_folder, screenshot_folder]:
        os.makedirs(folder, exist_ok=True)
    print("Folders are created sucessfully")


def organize_files(source_folder):
    jpg_count = 0
    edit_count = 0
    vids_count = 0
    screenshot_count = 0
    file_count = 0
    
    # List all files in the source folder
    files = os.listdir(source_folder)

    for file in files:
        if file.endswith('.jpg'):
            if file.__contains__('__'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(edit_folder, file))
                edit_count += 1
            elif file.startswith('IMG_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
        elif file.endswith('.mp4'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(vids_folder, file))
            vids_count += 1
        elif file.endswith('.png'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(screenshot_folder, file))
            screenshot_count += 1
       

    file_count = jpg_count + edit_count + vids_count + screenshot_count
    
    print(f"{jpg_count} files moved to 'pics' folder")
    print(f"{edit_count} files moved to 'edit' folder")
    print(f"{vids_count} files moved to 'vids' folder")
    print(f"{screenshot_count} files moved to 'screenshots' folder")
    print(f"\n{file_count} files moved in total")


def rename_files():
    global jpg_folder, edit_folder, vids_folder, converted_jpg_folder, screenshot_folder
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", "NORD_%Y-%m-%d_%H%M%S%%-c.%%le", jpg_folder])
    subprocess.run(["exiftool", "-ext", "png", "-FileName<DateTimeOriginal",
                   "-d", "NORD_%Y-%m-%d_%H%M%S%%-c.%%le", screenshot_folder])
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", "NORD_%Y-%m-%d_%H%M%S_edit%%-c.%%le", edit_folder])
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "mp4",
                   "-d", "NORD_%Y-%m-%d_%H%M%S%%-c.%%le", "-filename<CreateDate", vids_folder])

def delete_unused_folder():
    global jpg_folder, edit_folder, vids_folder, screenshot_folder
    
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"\tDeleted empty folder: {folder_path}")


if __name__ == "__main__":
    source_folder = input("Enter the path of the folder with photos and videos: ")

    init_folders(source_folder)

    # input("\nPress Enter to create subfolders...")
    create_folders()

    # input("\nPress Enter to organize files...")
    organize_files(source_folder)

    # input("\nPress Enter to rename files...")
    rename_files()

    # input("\nPress Enter to delete unused folders...")
    delete_unused_folder()

    print("\n\n----------------------DONE--------------------")
    print("Files organized, converted, renamed and unused files and folders are deleted successfully.")
    