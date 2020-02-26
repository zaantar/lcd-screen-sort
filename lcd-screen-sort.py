import json
import os
import re
import shutil
from pathlib import Path
from datetime import time, timedelta


def get_time_from_filename(filename: str):
    """
    From a filename like "something-15-25-something", extract the numbers as hours and minutes
    and turn them into a timedelta.
    """
    matches = re.search(r"^[^-]+-(\d\d)-(\d\d).*", filename)
    if not matches:
        return None
    return timedelta(hours=int(matches.group(1)), minutes=int(matches.group(2)))


def get_time_subdir(input_time: timedelta) -> str:
    """
    Convert a timedelta into a "HHmm" string. Surprising that Python has no native way of doing this
    in a simpler way (or I am missing something).

    :param input_time:
    :return:
    """
    beginning = input_time - timedelta(minutes=5)
    hours = beginning.seconds // 3600
    minutes = (beginning.seconds - (hours * 3600)) // 60
    return str(hours).rjust(2, '0') + str(minutes).rjust(2, '0')


def copy_and_rename(source_filepath: str, source_filename: str, destination_directory: str, index: int):
    """
    Copy provided file into the destination directory and prefix its name with the two-digit index.

    :param source_filepath: Path where the source file is located, without the actual filename.
    :param source_filename: Name of the source file.
    :param destination_directory: Destination.
    :param index: Index that will be used as a prefix to the filename.
    """
    Path(destination_directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        source_filepath + '/' + source_filename,
        destination_directory + '/' + str(index).rjust(2, '0') + '_' + source_filename
    )


# Read and parse settings
with open('settings.json') as jsonFile:
    settings = json.load(jsonFile)

output_dir = settings['output_dir']

repeating_images_dir = settings['input_dir']['repeating']
screen_input_dir = settings['input_dir']['screens']

# Build the list of screens we need to process
screen_list = [str(f.name) for f in Path(screen_input_dir).glob('*') if f.is_dir()]
screen_list.sort()

repeating_images = [str(f.name) for f in Path(repeating_images_dir).glob('*.jpg') if f.is_file()]
repeating_images.sort()

# Clear the destination directory
shutil.rmtree(output_dir)
os.mkdir(output_dir)

for screen_name in screen_list:
    # Each "main file" in each screen determines a certain time, during which it will be displayed together with
    # other repeating images.
    main_files = [str(f.name) for f in Path(screen_input_dir + '/' + screen_name).glob('*.jpg') if f.is_file()]
    main_files.sort()

    for main_file in main_files:
        # Determine the output directory
        time = get_time_from_filename(main_file)
        if time is None:
            continue
        time_dir = get_time_subdir(time)

        main_filepath = screen_input_dir + '/' + screen_name
        output_subdir = output_dir + '/' + screen_name + '/' + time_dir

        # Cycle the main file and each repeating image once.
        # noinspection PyRedeclaration
        file_index = 0
        for repeating_image in repeating_images:
            copy_and_rename(main_filepath, main_file, output_subdir, file_index)
            copy_and_rename(repeating_images_dir, repeating_image, output_subdir, file_index + 1)
            file_index = file_index + 2

print('done')
