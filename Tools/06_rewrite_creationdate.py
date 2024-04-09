import os
import subprocess
import shutil


def execute_exiftool_command(file_path):
    command = f'exiftool "-DateTimeOriginal<FileModifyDate" -overwrite_original "{file_path}"'
    subprocess.run(command, shell=True)

def convert_png_to_jpg(file_path):
    jpg_file = os.path.splitext(file_path)[0] + ".jpg"
    command = f'magick convert "{file_path}" "{jpg_file}"'
    subprocess.run(command, shell=True)
    os.remove(file_path)  # Remove the original PNG file after conversion

def rename_files(prefix, suffix, path):
    subprocess.run(["exiftool", "-ext", "jpg", "-FileName<DateTimeOriginal",
                   "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", path])

def process_files_in_path(path):
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            execute_exiftool_command(file_path)

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

def del_folder(source_folder):
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"\tDeleted empty folder: {folder_path}")

if __name__ == "__main__":
    path = input("Enter the path to the directory: ")

    input("\nPress Enter update date...")
    process_files_in_path(path)
    # prefix = input("Enter the prefix for the new filename: ")
    # suffix = input("Enter the suffix for the new filename: ")
    prefix = "5S_"
    suffix = "_shared"

    input("\nPress Enter rename files...")
    rename_files(prefix, suffix, path)
    
    input("\nPress Enter move files...")
    move_files_one_level_up(path)

    input("\nPress Enter delete folder...")
    del_folder(path)
