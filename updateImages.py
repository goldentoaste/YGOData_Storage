import os, sys
from multiprocessing.pool import Pool
import requests, json
import time
from PIL import Image
from PIL.Image import Resampling
from zipfile import ZipFile
import zipfile

existingImage = set(os.listdir("./images"))
addedImages = []


def downloadImage(stuff):
    id, url = stuff
    fileName : str = url[url.rfind("/") + 1 :]
    if fileName in existingImage or (fileName.rstrip(".jpg") + ".webp") in existingImage:
        return 
    
    req = requests.get(url)

    if req.status_code != 200:
        return
    
    imageData = req.content
    with open(f"images/{fileName}", "wb") as f:
        f.write(imageData)
        addedImages.append(fileName)
            


def compress(file : str):
    if not file.endswith(".jpg") or os.path.isfile(f"./compressed/{file.rstrip('.jpg')}.webp"):
        return

    i = Image.open(f"./images/{file}")
    i = i.resize((int(i.width * 0.75), int(i.height * 0.75)), Resampling.LANCZOS)
    i.save(f"./compressed/{file.rstrip('.jpg')}.webp", 'webp', optimize=True, quality=30)  

    return f"{file.rstrip('.jpg')}.webp"

    


def getEntireDataSet(skipdownload=False):
    data = requests.get(
        "https://db.ygoprodeck.com/api/v7/cardinfo.php?tcgplayer_data", timeout=10000
    ).json()["data"]

    urls = []

    with open("multipleArtWork.txt", "w", encoding="utf-8") as f:
        for d in data:
            if len(d["card_images"]) > 1:
                f.write(f"{d['name']}  {d['id']}\n\n")
            for u in d["card_images"]:
                urls.append(u["image_url_cropped"])
    print(len(urls))

    if not skipdownload:
        # download new images
        with Pool(10) as pool:
            workerpool = pool.map(downloadImage, [(i, urls[i]) for i in range(len(urls))])


    with Pool(20) as pool:
        p = pool.map(compress, os.listdir("./images"))
    

    p = [x for x in p if x is not None]
    if not p:
        print("no new images")
        return
    
    # put the newly compressed images into a zip package for distribution
    with ZipFile(f"./packages/{str(int(time.time()))}.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip:
        for image in p:
            if not image:
                continue
          
            zip.write(f"./compressed/{image}",image)
    print("done.")



if __name__ == "__main__":
    getEntireDataSet(skipdownload=True)


'''
with open( "updateList.json", 'r', encoding='utf-8' ) as f:
    
    updates = json.load(f)
    updates[str(int(time.time()))] = os.listdir('./images')
    
    with open( "updateList.json", 'w', encoding='utf-8' ) as wp:
        json.dump(updates, wp)
'''