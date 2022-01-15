# Readme

> Simple solution for linux to iterate over wallpapers in a folder, shotwell had a not so nice transition between the images

## Requirements

- Python
- Folder with some nice wallpapers#

## Setup

Save `wallpaper.py` in an accessible location and change the path to your wallpaper folder. Save the `wallpaper.service` file into `$HOME/.config/systemd/user/` and adjust the path to `wallpaper.py`.
Enable the service for your user via `systemctl --user enable wallpaper.service`, start it manually with `systemctl --user start wallpaper.service`, the desktop background should have already changed.

## How does it work

Check the python code. All files from the folder are loaded and initially added to a list, then verified if they are actually an image. After that the script loops through the images.

## Improvements

- [ ] Wallpapers in other format than landscape are not fitted into the size of the desktop
