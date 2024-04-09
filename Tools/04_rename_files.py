import subprocess


if __name__ == "__main__":

    print("Choose your prefix:")
    print("1. DJI")
    print("2. CAM")
    print("3. iPhone")
    print("4. Custome")

    choice1 = input("Enter the number of your choice: ")

    if choice1 == "1":
        prefix = "DJI_"
        suffix = ""
    elif choice1 == "2":
        prefix = "CAM_"
        suffix = ""
    elif choice1 == "3":
        prefix = "PRO_"
        suffix = ""
    elif choice1 == "4":
        prefix = input("Enter your prefix: ")
        suffix = input("Enter your suffix: ")

    print("Choose an option:")
    print("1. .jpg")
    print("2. .orf")
    print("3. .dng")
    print("4. .png")
    print("5. .mp4")
    print("6. .mov")
    print("7. Custome")

    choice2 = input("Enter the number of your choice: ")
    if choice2 == "1":
        extension = "jpg"
    elif choice2 == "2":
        extension = "orf"
    elif choice2 == "3":
        extension = "dng"
    elif choice2 == "4":
        extension = "png"
    elif choice2 == "5":
        extension = "mp4"
    elif choice2 == "6":
        extension = "mov"
    elif choice2 == "7":
        extension = input("Enter your extension: ")

    source_folder = input("Enter the path to your folder: ")

    subprocess.run(["exiftool", "-ext", f"{extension}", "-FileName<DateTimeOriginal",
                    "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", source_folder])

    # subprocess.run(["exiftool", "-ee", "-api", "QuickTimeUTC", "-ext", f"{extension}",
    #                 "-d", f"{prefix}%Y-%m-%d_%H%M%S%%-c{suffix}.%%le", "-filename<CreateDate", source_folder])

    print("\n\n----------------------DONE--------------------")
    print("Files renamed successfully.")
