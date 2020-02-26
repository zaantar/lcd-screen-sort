# lcd-screen-sort

Utility written for sorting images into subdirectories for the purpose of rendering loops for LCD screens for 
[WordCamp Prague 2020](https://2020.prague.wordcamp.org/).

It's just a little Python exercise and for me and I don't intend to do further develop this script in the future, 
unless it's needed again.

## Assignment

- Input: Directory structure as follows:
    - `repeating`: Contains JPG images that are supposed to be displayed in each loop, always alternating with the main image.
    - `screens`: Contains subdirectories, where each name corresponds to one room.
        - `$room`: Contains main images formatted as `something-HH-MM-whatever.jpg`, where `HH` and `MM` correspond to the
          time when the image becomes relevant.
- Output:
    - One subdirectory for each room
        - In it, one subdirectory for each time, formatted as `HHMM`
            - In it, a set of images named in the order in which they should be displayed (with a numeric prefix)
            - These images should be always: the main image, one of the repeating images, again the main image, another repeating image...
