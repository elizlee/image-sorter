# Image Sorter
This is a simple image file sorter that organizes image files into sub-directories
by year.

## Why this exists
* I like sorting my photos by date, and I wanted a way to automate this.
* I wanted something public on my GitHub profile that shows I know Python.

## Installation
The script requires Python 3.10+ along with the following packages:
* `filetype` (v1.2.0)
* `Pillow` (v10.4.0)

### Testing requirements
If you want to run the tests, you will also need to install `pytest` (v8.3.2).

## Testing
This code has been tested with Python 3.10 on Windows 11.

If you want to check that script will likely run as expected, run `test_image_sorter.py`
and confirm that there are no errors. You can run this by `cd`-ing into
`image-sorter` and entering this in the terminal:
```bash
python -m pytest test_image_sorter.py
```

## Running
In a terminal:
```bash
cd path/to/image-sorter
python main.py path/to/folder/of/images/to/sort
```

### Example
I have a folder of images called "Smartphone Pics" in my "Pictures"
directory. There are over 500 images, and 24 of them I've already copied into
a sub-folder called "2023 Highlights" (`Pictures/Smartphone Pics/2023 Highlights`).

To run my sorter on "Smartphone Pics", I execute the following commands:
```bash
cd "/Users/eliz/Documents/code/Python projects/image-sorter"

# Activating my conda environment
conda activate image-sorter

python main.py "/Users/eliz/Pictures/Smartphone Pics"
```
As a result, all photos from the top level are moved into sub-folders by year.
If I go into `Pictures/Smartphone Pics/2023`, I will see all the photos that I
uploaded from my smartphone that were taken in 2023. The sub-folder "2023
Highlights" is not removed or modified.
