import os
from PIL import Image
from PIL.Image import Resampling
from multiprocessing.pool import Pool


def dostuff(file):
    if not file.endswith(".jpg"):
        return

    i = Image.open(f"./images/{file}")
    i = i.resize((int(i.width * 0.7), int(i.height * 0.7)), Resampling.LANCZOS)
    i.save(f"./images/{file.rstrip('.jpg')}.webp", 'webp', optimize=True, quality=30)  
    os.remove(f"./images/{file}")

    
if __name__ =='__main__':
    with Pool(20) as p:
        p.map(dostuff, os.listdir("./images")) 