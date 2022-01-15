#/usr/bin/env python3

import imghdr
import os
import time

wpPath = '/home/user/Pictures/Wallpaper/'
allowedFiles = ['jpeg', 'png', 'webp']

def initialCheck():
    # load the path of all files
    files = [wpPath + f for f in os.listdir(wpPath) if os.path.isfile(os.path.join(wpPath, f))]

    # check if file is actual image, else remove from list
    for f in files:
        if not imghdr.what(f) in allowedFiles:
            files.remove(f)
    
    return files

if __name__ == '__main__':
    images = initialCheck()

    # define max idx and random starting image
    maxctr = len(images)-1
    idx = int(time.time() % maxctr)
    
    # let it run
    while True:
        os.system('/usr/bin/gsettings set org.gnome.desktop.background picture-uri {}'.format((images[idx])))
        idx += 1
        if idx == maxctr:
            idx = 0
        time.sleep(30)
