import argparse
from pathlib import Path

from sort_images_by_year import sort_images_by_year


def main(folder_to_sort: Path) -> None:
    """Sort the images in the given folder by year."""
    sort_images_by_year(folder_to_sort)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "folder_to_sort",
        type=Path,
        help="The path to the folder of images to sort",
    )
    args = arg_parser.parse_args()

    sort_images_by_year(args.folder_to_sort)
