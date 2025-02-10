# Sync Raw Filenames

## Description

**Sync Raw Filenames** is a Python script that renames **.ORF** raw files to match their corresponding **.JPG** filenames and updates their **DateTimeOriginal**, **CreateDate**, and **FileModifyDate** metadata based on the extracted timestamp from the filename. This ensures that raw and JPEG images remain synchronized in both naming and metadata.

## Features

- Renames **.ORF** files to match the corresponding **.JPG** filenames.
- Ensures the number of raw and JPEG files match before processing.
- Updates metadata fields (`DateTimeOriginal`, `CreateDate`, `FileModifyDate`) to reflect the new filename-based timestamp.
- Uses **ExifTool** for efficient metadata handling.

## Requirements

- **Python 3.x**
- **ExifTool** (must be installed and available in the system path)

## Installation

1. Install **ExifTool**:
   - Linux/macOS: `brew install exiftool` (for macOS with Homebrew)
   - Windows: Download from [ExifTool Official Website](https://exiftool.org/) and add it to your system path.
2. Clone or download this repository.
3. Ensure you have **Python 3.x** installed.

## Usage

1. Open a terminal or command prompt.
2. Run the script:
   ```bash
   python sync-raw-filenames.py
   ```
3. Enter the required directory paths when prompted:
   - **JPG directory**: The folder containing correctly named **.JPG** files.
   - **ORF directory**: The folder containing **.ORF** files to rename.
4. The script renames the ORF files and updates their metadata.

## Example Output

```bash
Renamed: P1010173.ORF -> CAM_2025-01-29_162055.orf
Updated metadata for: CAM_2025-01-29_162055.orf -> 2025:01:29 16:20:55

Renamed: P1010185.ORF -> CAM_2025-02-10_083045.orf
Updated metadata for: CAM_2025-02-10_083045.orf -> 2025:02:10 08:30:45

Renamed: P1010192.ORF -> CAM_2025-03-05_190010.orf
Updated metadata for: CAM_2025-03-05_190010.orf -> 2025:03:05 19:00:10
```

## Notes

- The script assumes that the **.JPG** and **.ORF** files correspond in order.
- Ensure that the filenames of **.JPG** images contain timestamps in the format `PREFIX_YYYY-MM-DD_HHMMSS.ext`.

## License

This project is licensed under the MIT License.

## Author

[Your Name]
