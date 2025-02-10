###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        sync-raw-filenames.py
# created:     10.02.2025 12:45
# edited:      -
# Description: This Python script renames .ORF (RAW) files based on the 
#              filenames of corresponding .JPG files in a given directory. 
#              It also updates the DateTimeOriginal, CreateDate, and 
#              FileModifyDate metadata of the .ORF files to match their 
#              filenames using ExifTool.
#
# Usage:       1. Run the script - Execute the Python script in a terminal.
#              2. Provide inputs - Enter the paths for the .JPG and .ORF directories.
#              3. Check results - The .ORF files will be renamed and metadata updated.
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
import subprocess
import re

def rename_and_update_raw_files(jpg_directory, raw_directory):
    # Get sorted lists of JPG and ORF files
    jpg_files = sorted([f for f in os.listdir(jpg_directory) if f.lower().endswith(".jpg")])
    orf_files = sorted([f for f in os.listdir(raw_directory) if f.lower().endswith(".orf")])
    
    # Check if the number of files match
    if len(jpg_files) != len(orf_files):
        print("Error: The number of JPG and ORF files do not match!")
        return
    
    # Rename ORF files based on JPG filenames and update metadata
    for jpg_name, orf_name in zip(jpg_files, orf_files):
        new_name = os.path.splitext(jpg_name)[0] + ".orf"
        old_path = os.path.join(raw_directory, orf_name)
        new_path = os.path.join(raw_directory, new_name)
        
        # ExifTool command to rename the ORF file
        rename_command = ["exiftool", "-overwrite_original", f"-FileName={new_name}", old_path]
        
        try:
            subprocess.run(rename_command, check=True)
            print(f"Renamed: {orf_name} -> {new_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error renaming {orf_name}: {e}")
            continue
        
        # Extract date from filename (expecting format: PREFIX_YYYY-MM-DD_HHMMSS.ext)
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})(\d{2})(\d{2})", new_name)
        if match:
            formatted_datetime = f"{match.group(1)}:{match.group(2)}:{match.group(3)} {match.group(4)}:{match.group(5)}:{match.group(6)}"
        else:
            print(f"Error extracting date from filename: {new_name}")
            continue
        
        # ExifTool command to update metadata
        metadata_command = [
            "exiftool",
            f"-DateTimeOriginal={formatted_datetime}",
            f"-CreateDate={formatted_datetime}",
            f"-FileModifyDate={formatted_datetime}",
            "-overwrite_original",
            new_path
        ]
        
        try:
            subprocess.run(metadata_command, check=True)
            print(f"Updated metadata for: {new_name} -> {formatted_datetime}")
        except subprocess.CalledProcessError as e:
            print(f"Error updating metadata for {new_name}: {e}")

if __name__ == "__main__":
    jpg_directory = input("Enter the path to the JPG directory: ")
    raw_directory = input("Enter the path to the ORF directory: ")
    
    rename_and_update_raw_files(jpg_directory, raw_directory)
