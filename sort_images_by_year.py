import shutil
import time
from collections import defaultdict
import os
from typing import Optional

import filetype
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def sort_images_by_year(folder_to_sort: Path) -> None:
    """Move the images in the given folder to sub-folders by year."""

    # Verify that the folder exists
    if not folder_to_sort.exists():
        raise RuntimeError(f"Could not locate the folder at {folder_to_sort}!")

    folder_organization_dict = defaultdict(list)

    print(f"Inspecting image files in {folder_to_sort}...")
    for folder_item in folder_to_sort.iterdir():
        # Only read from image files.
        # Attempting is_image on dirs will throw a PermissionError, so we check
        # if it's a file first.
        if folder_item.is_file() and filetype.is_image(folder_item):
            img_year = get_year_taken(folder_item)
            folder_organization_dict[img_year].append(folder_item)
        else:
            print(f"Skipping `{folder_item.name}` because it is not an image file")

    if not folder_organization_dict:
        print("Could not find any images in this folder! No images will be moved.")
        return

    # Move the images found
    print(
        f"Found images taken in the following years: "
        + f"{list(folder_organization_dict.keys())}. Sorting images into these "
        + "folders..."
    )
    for img_year, images_from_year in folder_organization_dict.items():
        year_folder = folder_to_sort.joinpath(img_year)

        # Create the new sub-folder if it doesn't already exist
        if not year_folder.exists():
            year_folder.mkdir()

        img_count = 0
        for img_path in images_from_year:
            # Do not move if an image with the same name already exists in the
            # folder
            if img_path.name in os.listdir(year_folder):
                print(
                    f"`{img_path.name}` already exists in `{year_folder}`! "
                    + "Keeping image in original folder."
                )
                continue
            shutil.move(img_path, year_folder)
            img_count += 1

        print(f"Moved {img_count} images to {year_folder}")

    print("Done!")


def get_year_taken(image_file: Path) -> str:
    """Get the year taken from the given image file.

    Returns None if no year was found.
    """
    # First try getting the DateTime from the metadata
    exif_year = get_exif_year(image_file)
    if exif_year:
        return exif_year

    # Next, use os.path; compare the created and modified times and use the
    # earliest one
    print("Substituting date taken with date created/modified...")
    time_created = os.path.getctime(image_file)
    time_modified = os.path.getmtime(image_file)
    earliest_time_str = time.ctime(min(time_created, time_modified))
    earliest_datetime = time.strptime(earliest_time_str)
    return str(earliest_datetime.tm_year)


def get_exif_year(image_file) -> Optional[str]:
    """Attempt to get the year taken from the images's exif.

    Returns None if the image has no exif or DateTime tag.
    """
    try:
        with Image.open(image_file) as image_to_sort:
            img_exif = image_to_sort.getexif()
    except UnidentifiedImageError:
        print(
            f"WARNING: Pillow could not read `{image_file.name}` -- it may be "
            + "corrupted!"
        )
        return None

    if not img_exif:
        print(f"Could not find metadata for `{image_file.name}`!")
        return None

    # 306 is the DateTime key
    date_taken_str = img_exif.get(306)
    if not date_taken_str:
        print(f"Could not find date taken for `{image_file.name}`!")
        return None

    # The year should be the first four characters
    if len(date_taken_str) < 4:
        print(
            f"DateTime for `{image_file.name}` could not be parsed: "
            + f"`{date_taken_str}`"
        )
        return None

    return date_taken_str[:4]
