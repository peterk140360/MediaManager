###############################################################################
# Author:      Sebastian Peterka
# Company:     -
# File:        00_OnePlus_Sort-by-year.py
# created:     29.10.2023 16:17
# edited:      -
# Description: The "OnePlus Sort by year" script is just to sort a big amout
#              of photos and vids into a folder system with contains the year.
#              Furthermore the script creates subfolders e.g. "01-18" and 
#              moves all files into those subfolders.
#
# Usage:       1. Copy all files from OnePlus "Camera" Foldere to your hard-drive
#              2. Run the script using "python 00_OnePlus_Sort-by-yeear.py"
#              3. Insert the path of the just copied OnePlus photos
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
import re
import shutil

def sort_files(source_folder):
    # Define regular expressions to match date patterns in the file names
    image_date_pattern = re.compile(r'IMG_(\d{4})(\d{2})(\d{2})')
    video_date_pattern = re.compile(r'VID_(\d{4})(\d{2})(\d{2})')

    # Initialize the count of moved files
    moved_files_count = 0

    # Iterate over the files in the source directory
    for filename in os.listdir(source_folder):
        full_path = os.path.join(source_folder, filename)

        if os.path.isfile(full_path):
            # Try to match both image and video date patterns
            image_match = image_date_pattern.match(filename)
            video_match = video_date_pattern.match(filename)

            if image_match:
                year, month, day = image_match.groups()
                year = int(year)
                month = int(month)
            elif video_match:
                year, month, day = video_match.groups()
                year = int(year)
                month = int(month)
            else:
                # Skip files that don't match either pattern
                continue

            # Create the year directory if it doesn't exist
            year_dir = os.path.join(source_folder, str(year))
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)

            # Create the month-year directory if it doesn't exist
            month_year_dir = os.path.join(year_dir, f"{month:02d}-{year % 100:02d}")
            if not os.path.exists(month_year_dir):
                os.makedirs(month_year_dir)

            # Move the file to the month-year directory without renaming
            new_path = os.path.join(month_year_dir, filename)
            shutil.move(full_path, new_path)


            # Increment the count of moved files
            moved_files_count += 1

    print(f"\n{moved_files_count} Files organized into year-month folders within the source directory.")



if __name__ == "__main__":
    source_folder = input("Enter the path of the folder with photos and videos: ")

    input("\nPress Enter to sort files into year-month scheme...")
    sort_files(source_folder)

    print("\n----------------------DONE--------------------")