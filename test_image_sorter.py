"""Testing module for `sort_images_by_year`.

To run via command line:
```bash
python -m pytest test_image_sorter.py
```
"""

from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from PIL import Image

import os
import pytest
import shutil

from sort_images_by_year import sort_images_by_year

TEST_IMAGE_MODE = "RGB"
TEST_IMAGE_SIZE = (300, 300)


@pytest.fixture
def test_image_folder() -> Generator[Path, None, None]:
    """Generate a folder of test images."""
    test_image_folder_path = Path(f"{__file__}/../test_img_folder").resolve()
    test_image_folder_path.mkdir()

    yield test_image_folder_path

    # Once the test is finished, delete the folder and its contents
    shutil.rmtree(test_image_folder_path)


def test_sort_images_by_year(test_image_folder: Path) -> None:
    """Test `sort_images_by_year`."""
    # Set up the test files
    assert (
        test_image_folder.exists()
    ), f"Could not locate the test folder at `{test_image_folder}`!"

    # We create a stray dir to make sure that it doesn't get moved or deleted
    stray_dir = test_image_folder.joinpath("stray_dir")
    stray_dir.mkdir()
    assert (
        stray_dir.exists()
    ), f"Could not locate the test sub-folder at `{stray_dir}`!"

    # Create some test images
    img_1 = Image.new(TEST_IMAGE_MODE, TEST_IMAGE_SIZE, color="white")
    img_1_path = test_image_folder.joinpath("img_1.jpeg")
    img_1_destination = test_image_folder.joinpath(f"2020/{img_1_path.name}")
    img_1.save(img_1_path)

    img_2 = Image.new(TEST_IMAGE_MODE, TEST_IMAGE_SIZE, color="black")
    img_2_path = test_image_folder.joinpath("img_2.png")
    img_2_destination = test_image_folder.joinpath(f"2019/{img_2_path.name}")
    img_2.save(test_image_folder.joinpath("img_2.png"))

    image_with_copy_path = test_image_folder.joinpath("img_3.JPG")
    folder_with_copy_path = test_image_folder.joinpath("2012")
    folder_with_copy_path.mkdir()
    img_3 = Image.new(TEST_IMAGE_MODE, TEST_IMAGE_SIZE, color="red")
    img_3.save(image_with_copy_path)
    shutil.copy2(image_with_copy_path, folder_with_copy_path)

    # This image is not intended to be moved; we want to make sure this file
    # isn't deleted when a new image is added.
    img_4 = Image.new(TEST_IMAGE_MODE, TEST_IMAGE_SIZE, color="blue")
    img_4_path = test_image_folder.joinpath("2019/img_4.jpg")
    img_4_path.parent.mkdir()
    img_4.save(img_4_path)

    # Set mock modification dates using os.utime.
    image_paths_to_datetimes = {
        img_1_path: "2020:04:15 15:00:03",
        img_2_path: "2019:07:25 14:23:57",
        image_with_copy_path: "2012:06:01 20:29:13",
    }
    for image_path, date_taken in image_paths_to_datetimes.items():
        assert (
            image_path.exists()
        ), f"Could not locate the test image `{image_path}`!"
        mock_modification_date = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
        mock_epoch = mock_modification_date.timestamp()
        os.utime(image_path, (mock_epoch, mock_epoch))

    # Attempt to sort a non-existent folder
    fake_image_folder = test_image_folder.joinpath("fake_subfolder")
    try:
        sort_images_by_year(fake_image_folder)
        nonexistent_folder_error = False
    except RuntimeError:
        nonexistent_folder_error = True
    assert nonexistent_folder_error, (
        "The script should have terminated because the folder "
        + f"`{fake_image_folder}` does not exist!"
    )

    sort_images_by_year(test_image_folder)

    assert stray_dir.exists(), "The test sub-folder was not supposed to be moved!"

    assert (
        img_1_destination.exists()
    ), f"The image `{img_1_path.name}` was supposed to be moved to the 2020 folder!"

    assert (
        img_2_destination.exists()
    ), f"The image `{img_2_path.name}` was supposed to be moved to the 2022 folder!"

    assert (
        image_with_copy_path.exists()
    ), f"The image `{image_with_copy_path.name}` was not supposed to be moved!"
    assert folder_with_copy_path.joinpath(image_with_copy_path.name).exists(), (
        f"A copy of the image `{image_with_copy_path.name}` should be in the "
        + "2012 folder!"
    )

    assert (
        img_4_path.exists()
    ), f"The file `{img_4_path.name}` should not have been deleted!"
