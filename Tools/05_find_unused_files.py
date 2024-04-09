import os
import shutil

def list_filenames_in_folders_and_root(path):
    root_filenames_list = []
    subfolder_filenames_list = []

    # List files in the root directory
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            root_filenames_list.append(file)

    # List files in subdirectories
    for root, dirs, files in os.walk(path):
        # Ignore files in the root folder
        if root == path:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            # Extract only the filename without the path
            subfolder_filenames_list.append(os.path.relpath(file_path, path))

    return root_filenames_list, subfolder_filenames_list


def rename_filenames(original_path):
    # Extract the filename using os.path.basename
    return os.path.basename(original_path)

def cut_extension(strings_set):
    cut_strings = set()
    for string in strings_set:
        cut_string = string.split('.')[0]
        cut_strings.add(cut_string)
    return cut_strings

def cut_strings_after_dot(strings_set):
    modified_strings = set()
    for string in strings_set:
        index = string.rfind('.')
        if index != -1:
            modified_string = string[:index]
            modified_strings.add(modified_string)
    return modified_strings

def merge_extension(strings_set, extension):
    merged_strings = set()
    for string in strings_set:
        cut_string = string.split('.')[0]
        merged_string = cut_string + extension
        merged_strings.add(merged_string)
    return merged_strings


if __name__ == "__main__":
    print("Choose an option:")
    print("1. .jpg")
    print("2. .orf")
    print("3. .dng")
    print("4. Custome")
    choice = input("Choose the extension for the root-folder files: ")
    
    if choice == "1":
        extension = ".jpg"
    elif choice == "2":
        extension = ".orf"
    elif choice == "3":
        extension = ".dng"
    elif choice == "4":
        extension = input("Enter your extension: ")

    # Provide the path as input
    folder_path = input("Enter the folder path: ")
    
    
    subfolder_files = []
    rootfolder_files = []

    # Check if the path exists
    if os.path.exists(folder_path):
        root_filenames, subfolder_filenames = list_filenames_in_folders_and_root(folder_path)
        for file in subfolder_filenames:
            print(file)

        
        # Print filenames in the root directory
        print("Filenames in the root directory:")
        for filename in root_filenames:
            rootfolder_files.append(filename)

        # Print filenames in subdirectories
        print("\nFilenames in subdirectories:")
        for filename in subfolder_filenames:
            subfolder_files.append(rename_filenames(filename))
    else:
        print("Invalid folder path. Please provide a valid path.")

    subfolder_files = set(subfolder_files)
    rootfolder_files = set(rootfolder_files)

    cut_strings_subfolder = cut_extension(subfolder_files)
    cut_strings_rootfolder = cut_extension(rootfolder_files)

    for file in cut_strings_subfolder:
        print(file)
    print(f"Length cut_strings_subfolder: {len(cut_strings_subfolder)}")

    print()

    for file in cut_strings_rootfolder:
        print(file)
    print(f"Length cut_strings_rootfolder: {len(cut_strings_rootfolder)}")


    # Calculate the set of filenames that are not yet used
    not_yet_used = cut_strings_rootfolder.difference(cut_strings_subfolder)

    for file in not_yet_used:
        print(file)

    print(f"Length not_yet_used: {len(not_yet_used)}")

    merged_strings_set = merge_extension(not_yet_used, extension)

    # Create a new folder called "not_yet_used" if it doesn't exist
    not_yet_used_folder = os.path.join(folder_path, "not_yet_used_cut")
    os.makedirs(not_yet_used_folder, exist_ok=True)

    # Copy files to the "not_yet_used" folder
    for filename in merged_strings_set:
        source_path = os.path.join(folder_path, filename)
        destination_path = os.path.join(not_yet_used_folder, filename)
        shutil.move(source_path, destination_path)

    print(f"Files not yet used have been copied to the '{not_yet_used_folder}' folder.")
