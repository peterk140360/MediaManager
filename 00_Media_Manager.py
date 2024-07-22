###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        03_CAM_DJI_Media_Manager.py
# created:     01.02.2024 14:17
# edited:
#
# Description: The "iPhone Media Manager" script is a versatile and efficient
#              tool designed to simplify the organization and management of
#              photos and videos captured using an iPhone or similar devices.
#              Key features are:
#                   * File Organization (move files into different folder)
#                   * HEIC-to-JPEG Conversion using magick
#                   * File Renaming using exiftool (day and time tag)
#                   * Cleanup and Optimization (deletes unused folder)
#
# Usage:       1. Copy all files from iPhone to your hard-drive
#              2. Run the script using "python 00_iPhone_Media_Manager.py"
#              3. Insert the path of the just copied iPhone photos
#              4. Let the script to it's things and check the result.
#
# Comments:    Make sure that imagemagick and exiftool is installed.
#
# Todo:        * delete Live-Photo videos which got air-droped (videos with no length)
#              * also rename those pics that got airdroped and than got locally edited.
#                now it is only named with ending "-1" --> should be "_edited"
#              * combine the converted-jpgs into the pics folder
#              * Change filename for saved whatsapp imags to saved date and time.
#              * check converted heics if there are edit ones included and rename them
#
# Resources:   https://www.mysysadmintips.com/windows/clients/967-rename-iphone-mov-videos-to-date-and-time-taken
#              https://imagemagick.org/script/download.php
#              https://exiftool.org/examples.html
#              https://exiftool.org/
#
###############################################################################

# from curses import raw
import os
from random import choices
import shutil
import subprocess

jpg_folder = None
edit_folder = None
vids_folder = None
heic_folder = None
aae_folder = None
screenshot_folder = None
raw_folder = None
converted_jpg_folder = None
conversion_count = 0


def init_folders(source_folder):
    global jpg_folder, edit_folder, vids_folder, heic_folder, aae_folder, screenshot_folder, raw_folder

    jpg_folder = os.path.join(source_folder, 'pics')
    edit_folder = os.path.join(source_folder, 'edit')
    vids_folder = os.path.join(source_folder, 'vids')
    heic_folder = os.path.join(source_folder, 'heic-to-jpg')
    aae_folder = os.path.join(source_folder, 'aae')
    screenshot_folder = os.path.join(source_folder, 'screenshots')
    raw_folder = os.path.join(source_folder, 'raw')


def create_folders():
    global jpg_folder, edit_folder, vids_folder, heic_folder, aae_folder, screenshot_folder

    # Create destination folders if they don't exist
    for folder in [jpg_folder, edit_folder, vids_folder, heic_folder, aae_folder, screenshot_folder, raw_folder]:
        os.makedirs(folder, exist_ok=True)
    print("Folders are created sucessfully")


def organize_files(source_folder):
    jpg_count = 0
    edit_count = 0
    vids_count = 0
    heic_count = 0
    aae_count = 0
    screenshot_count = 0
    file_count = 0
    raw_count = 0

    # List all files in the source folder
    files = os.listdir(source_folder)

    for file in files:
        if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.JPEG'):
            if file.startswith('IMG_E'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(edit_folder, file))
                edit_count += 1
            elif file.startswith('IMG_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
            elif file.startswith('P'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
            elif file.startswith('DJI_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
            elif file.startswith('PRO_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
            elif file.startswith('CAM_'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
            elif file.startswith('2024'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(jpg_folder, file))
                jpg_count += 1
        elif file.endswith('.MOV') or file.endswith('.mov') or file.endswith('.MP4') or file.endswith('.m4v') or file.endswith('.mp4'):
            if file.startswith('IMG_E'):
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(edit_folder, file))
                edit_count += 1
            else:
                shutil.move(os.path.join(source_folder, file),
                            os.path.join(vids_folder, file))
                vids_count += 1
        elif file.endswith('.HEIC'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(heic_folder, file))
            heic_count += 1
        elif file.endswith('.AAE'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(aae_folder, file))
            aae_count += 1
        elif file.endswith('.PNG'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(screenshot_folder, file))
            screenshot_count += 1

        elif file.endswith('.ORF') or file.endswith('.DNG'):
            shutil.move(os.path.join(source_folder, file),
                        os.path.join(raw_folder, file))
            raw_count += 1

    file_count = jpg_count + edit_count + vids_count + heic_count + aae_count + screenshot_count + raw_count

    print(f"{jpg_count} files moved to 'pics' folder")
    print(f"{edit_count} files moved to 'edit' folder")
    print(f"{vids_count} files moved to 'vids' folder")
    print(f"{heic_count} files moved to 'heic-to-jpg' folder")
    print(f"{aae_count} files moved to 'aae' folder")
    print(f"{screenshot_count} files moved to 'screenshots' folder")
    print(f"{raw_count} files moved to 'raw' folder")
    print(f"\n{file_count} files moved in total")


def convert_heic_to_jpg():
    global conversion_count, heic_folder, converted_jpg_folder
    conversion_count = 0
    converted_jpg_folder = os.path.join(
        os.path.dirname(heic_folder), "converted-jpg")
    os.makedirs(converted_jpg_folder, exist_ok=True)

    heic_files = os.listdir(heic_folder)
    for heic_file in heic_files:
        output_jpg_file = os.path.splitext(heic_file)[0] + ".jpg"
        heic_file_path = os.path.join(heic_folder, heic_file)
        output_jpg_path = os.path.join(converted_jpg_folder, output_jpg_file)
        subprocess.run(["magick", "convert", heic_file_path, output_jpg_path])
        conversion_count += 1

    if conversion_count == len(os.listdir(heic_folder)):
        print(f"All {conversion_count } Files got converted.")
    else:
        print("\tERROR: Number of converted Files is not equal to number of HEIC-Files - Check it")


def rename_files(prefix, suffix):
    global jpg_folder, edit_folder, vids_folder, converted_jpg_folder, screenshot_folder, raw_folder
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", jpg_folder])
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", converted_jpg_folder])
    subprocess.run(["exiftool", "-ext", "png", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", screenshot_folder])
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c_edit{suffix}.%%le", edit_folder])
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "mov",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}_edit.%%le", "-filename<CreationDate", edit_folder])
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "mov",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", "-filename<CreateDate", vids_folder]) # CreateDate or CreationDate
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "mp4",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", "-filename<CreateDate", vids_folder]) # CreateDate (works for DJI) or CreationDate
    subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", "m4v",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", "-filename<CreateDate", vids_folder])
    subprocess.run(["exiftool", "-ext", "orf", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", raw_folder])
    subprocess.run(["exiftool", "-ext", "dng", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", raw_folder])


def delete_heic_folder():
    global conversion_count, heic_folder
    if conversion_count == len(os.listdir(heic_folder)):
        shutil.rmtree(heic_folder)
        print("\tHEIC-Folder removed successfully")

    else:
        print("\tERROR: Number of HEIC-Files is not equal to converted JPG-Files - Check it")


def delete_aae_folder():
    global aae_folder, edit_folder
    shutil.rmtree(aae_folder)
    print("\tAAE-Folder removed successfully")


def delete_unused_folder():
    global conversion_count, jpg_folder, edit_folder, vids_folder, heic_folder, aae_folder, screenshot_folder

    delete_heic_folder()
    delete_aae_folder()

    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"\tDeleted empty folder: {folder_path}")


def move_files_one_level_up(folder_path):
    parent_folder = os.path.dirname(folder_path)
    moved_files_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            destination_path = os.path.join(parent_folder, filename)
            if not os.path.exists(destination_path):
                shutil.move(file_path, destination_path)
                moved_files_count += 1
    print(f"Moved {moved_files_count} file(s) one level up.")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Custom")
    print("2. CAM")
    print("3. PRO")
    print("4. DJI")
    print("5. 3GS")
    print("6. 5S")

    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        prefix = input("Enter your prefix: ")
        suffix = input("Enter your suffix: ")
    elif choice == "2":
        prefix = "CAM_"
        suffix = ""
    elif choice == "3":
        prefix = "PRO_"
        suffix = ""
    elif choice == "4":
        prefix = "DJI_"
        suffix = ""
    elif choice == "5":
        prefix = "3GS_"
        suffix = ""
    elif choice == "6":
        prefix = "5S_"
        suffix = ""
    else:
        raise ValueError("Invalid choice. Recheck.")

    source_folder = input("Enter the path to your folder: ")

    init_folders(source_folder)

    input("\nPress Enter to create subfolders...")
    create_folders()

    input("\nPress Enter to organize files...")
    organize_files(source_folder)

    input("\nPress Enter to convert heic to jpg...")
    convert_heic_to_jpg()

    input("\nPress Enter to rename files...")
    rename_files(prefix, suffix)

#    input("\nPress Enter to move files one level up...")
#    move_files_one_level_up(jpg_folder)

    input("\nPress Enter to delete unused folders...")
    delete_unused_folder()

    print("\n\n----------------------DONE--------------------")
    print("Files organized, converted, renamed and unused files and folders are deleted successfully.")