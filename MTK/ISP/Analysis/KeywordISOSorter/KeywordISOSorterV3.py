import os
import shutil
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox


# Move Photos to Numbered Folders
def move_photos_to_folders(image_directory):
    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            if filename.lower().endswith(".jpg"):
                filename_parts = filename.split("_")
                image_number = filename_parts[0]
                image_name = filename_parts[1].split(".")[0]

                folder_path = os.path.join(root, image_number)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                source_path = os.path.join(root, filename)
                destination_path = os.path.join(folder_path, filename)
                shutil.move(source_path, destination_path)

# Rename JPG Files Based on ISO Value
def rename_jpg_files(image_directory, keyword):
    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
                if keyword in filename:
                    try:
                        image = Image.open(file_path)
                        exif_data = image._getexif()
                        image.close()

                        if exif_data is not None and 34855 in exif_data:
                            iso_value = exif_data[34855]

                            for same_filename in files:
                                other_file_path = os.path.join(root, same_filename)
                                new_filename = f"ISO{iso_value}_{same_filename}"
                                new_file_path = os.path.join(root, new_filename)

                                os.rename(other_file_path, new_file_path)
                    except (IOError, OSError):
                        print("Unable to read image:", filename)

# Move JPG Files Out of Numbered Folders
def move_jpg_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(os.path.dirname(root), file)
                shutil.move(source_path, destination_path)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            folder = os.path.join(root, dir)
            if not os.listdir(folder):
                os.rmdir(folder)

# Create ISO Folders
def create_iso_folders(image_directory, folder_names):
    for root, dirs, files in os.walk(image_directory):
        if not dirs:
            for folder_name in folder_names:
                folder_path = os.path.join(root, folder_name)
                os.makedirs(folder_path, exist_ok=True)

# Categorize JPG Files by ISO
def categorize_jpg_files(image_directory, target_folders):
    for root, dirs, files in os.walk(image_directory):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                source_file_path = os.path.join(root, file)
                iso_value = int(file.split("_")[0][3:])

                target_subfolder = None
                for folder, start_iso, end_iso in target_folders:
                    if start_iso <= iso_value <= end_iso:
                        target_subfolder = folder
                        break

                if target_subfolder is not None:
                    target_subfolder_path = os.path.join(root, target_subfolder)

                    if os.path.exists(target_subfolder_path):
                        target_file_path = os.path.join(target_subfolder_path, file)
                        shutil.move(source_file_path, target_file_path)

# Print JPG Count
def print_jpg_count(image_directory):
    for root, dirs, files in os.walk(image_directory):
        if not dirs:
            folder_name = os.path.basename(root)
            parent_folder_name = os.path.basename(os.path.dirname(root))
            pparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(root)))
            jpg_count = sum(1 for file in files if file.lower().endswith(".jpg"))
            print(f"{pparent_folder_name}/ {parent_folder_name}/ {folder_name}: {jpg_count} JPG")

def confirmation_clicked(image_directory, keyword):
    if not image_directory or not keyword:
        print("\nInput Error!")
        print("Please fill in all fields.")
        # QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
        # ##################
        return

    # Call the main functionality methods
    move_photos_to_folders(image_directory)
    rename_jpg_files(image_directory, keyword)
    move_jpg_files(image_directory)
    folder_names = ["ISO100-199", "ISO200-399", "ISO400-799", "ISO800-1599", "ISO1600-3199", "ISO3200-6400"]
    create_iso_folders(image_directory, folder_names)
    target_folders = [
        ("ISO100-199", 100, 199),
        ("ISO200-399", 200, 399),
        ("ISO400-799", 400, 799),
        ("ISO800-1599", 800, 1599),
        ("ISO1600-3199", 1600, 3199),
        ("ISO3200-6400", 3200, 6400)
    ]
    categorize_jpg_files(image_directory, target_folders)
    print_jpg_count(image_directory)

    # QMessageBox.information(self, "Done", "Renamed and Organized!")
    print("\n------Done------")
    print("Renamed and Organized.")
    print("------------------")


def main(image_directory, keyword):
    confirmation_clicked(image_directory, keyword)
    