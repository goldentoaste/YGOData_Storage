# pip install pillow
import os
from typing import List
from PIL import Image
import sys
import glob

quality = int(input("Compression quality? (0 - 100, 100 is best quality)"))
deleteOriginal = input("delete originalFile? (T/N)").lower() == "t"

queue: List[str] = []
nameToSize = dict()
print("Process the following files:")

for file in glob.glob("./**/*.png", recursive=True) + glob.glob("./**/*.jpg", recursive=True):
    queue.append(file)
    nameToSize[file] = os.path.getsize(file) // 1024
    print(file, f"({nameToSize[file]}kb)")


abort = input("\n Continue? (T/N)").lower() != "t"

if abort:
    sys.exit()

for file in queue:
    img: Image.Image = Image.open(file)
    newPath = file.rstrip(".jpg").rstrip(".png") + ".webp"
    img.save(newPath, "webp", optimize=True, quality=quality)
    print(f"Processed file {file}, {nameToSize[file]}kb -> {os.path.getsize(newPath) // 1024}kb")
    if deleteOriginal:
        os.remove(file)

'''
    192.168.1.211:11710
http://192.30.89.67:11710
4Mr59LdMJ2xG
'''