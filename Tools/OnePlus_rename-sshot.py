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


# DateTimeOriginal
import os
import re
import shutil
import subprocess

def rename_files(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                current_file_path = os.path.join(root, file)
                subprocess.run(["exiftool", "-ext", "jpg", "-FileName<filemodifydate",
                                "-d", "NORD_%Y-%m-%d_%H%M%S_sshot%%-c.%%le", current_file_path])

def rename_files_dji(source_folder):
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<filemodifydate",
                    "-d", "NORD_%Y-%m-%d_%H%M%S_dji-pano%%-c.%%le", source_folder])

def rename_files_edit(source_folder):
    subprocess.run(["exiftool", "-ext", "jpeg", "-FileName<filemodifydate",
                    "-d", "NORD_%Y-%m-%d_%H%M%S_edit%%-c.%%le", source_folder])



if __name__ == "__main__":
    source_folder = input("Enter the path of the folder with photos and videos: ")

    input("\nPress Enter to rename files...")
        
    # rename_files(source_folder)
    # rename_files_dji(source_folder)
    rename_files_edit(source_folder)
    
    print("\n\n----------------------DONE--------------------")
    