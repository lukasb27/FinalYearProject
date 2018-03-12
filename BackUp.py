# KeePassDB_30-January-2018-07-31-33.kdbx


# Look for file name eg 'KeePassDB_30-January-2018-07-31-33.kdbx' in folder location smb://charlie/Lukas
# (do i need creds) move that file to new folder in icloud location ../Documents/KeePass(create?)
# wipe old back ups. Write to a log.

import shutil
import datetime
import os
today = str(datetime.date.today())
folder_to_move_to = r'/Users/lukasball/Documents/keePass'
folder = r'/Volumes/Lukas/'

for file in os.listdir(folder):
    if file.endswith(".kdbx"):
        print(file, 'will be moved')
        fullpath = folder + file
        shutil.move(fullpath, folder_to_move_to)
    else:
        break



#  build in a logger 