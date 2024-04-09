# MediaManager

## Description
The **Media Manager** script is a versatile and efficient tool designed to simplify the organization and management of photos and videos captured using an iPhones, cameras or drones. It offers the following key features:

- File Organization: Move files into different folders.
- HEIC-to-JPEG Conversion using `magick`.
- File Renaming using `exiftool` (day and time tag).
- Cleanup and Optimization: Deletes unused folders.

## Usage
1. Copy all files from iPhone to your hard drive.
2. Run the script using `python 00_Media_Manager.py`.
3. Insert the path of the just copied iPhone photos.
4. Let the script do its things and check the result.

## Requirements
Make sure that `imagemagick` and `exiftool` are installed.

## Todo
- Delete Live-Photo videos which got air-dropped (videos with no length).
- Rename pictures that were air-dropped and then locally edited (currently named with ending "-1" should be "_edited").
- Combine the converted JPEGs into the pictures folder.
- Change filename for saved WhatsApp images to saved date and time.

## Resources
- [Rename iPhone MOV videos to date and time taken](https://www.mysysadmintips.com/windows/clients/967-rename-iphone-mov-videos-to-date-and-time-taken)
- [ImageMagick Download](https://imagemagick.org/script/download.php)
- [ExifTool Examples](https://exiftool.org/examples.html)
- [ExifTool](https://exiftool.org/)

