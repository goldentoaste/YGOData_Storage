from typing import List
import requests, json
from multiprocessing.pool import Pool
from PIL import Image
import os, sys
import cloudinary
import cloudinary.uploader as uploader
from cloudinary.utils import cloudinary_url

existingImage = set(os.listdir("./downloads"))


def downloadImage(stuff):
    id, url = stuff
    fileName : str = url[url.rfind("/") + 1 :]
    if fileName in existingImage or (fileName.rstrip(".jpg") + ".webp") in existingImage:
        return 
    
    req = requests.get(url)

    if req.status_code != 200:
        return None
    
    imageData = req.content
    with open(f"downloads/{fileName}", "wb") as f:
        f.write(imageData)
        return fileName


def envFile():
    with open(".env", "r", encoding="utf8") as f:
        out = dict()

        for line in f.readlines():
            items = line.split("=")
            if len(items) != 2:
                continue

            out[items[0]] = items[1]

        return out

envVars = envFile()
cloudinary.config(secure=True, **envVars)

def uploadToCDN(path:str):
    uploader.upload_image(path, public_id=os.path.basename(path), asset_folder="ygo")



def getEntireDataSet():
    data = requests.get(
        "https://db.ygoprodeck.com/api/v7/cardinfo.php?tcgplayer_data", timeout=10000
    ).json()["data"]


    urls = []

    for d in data:
        for i in d["card_images"]:
            urls.append(i["image_url"])

    newImages : List[str]
    with Pool(20) as pool:
        newImages = pool.map(downloadImage, [(i, urls[i]) for i in range(len(urls))])

    # ignore downloaded files, remove Nones
    newImages = [i for i in newImages if i]

    
    with Pool(20) as pool:
        pool.map(uploadToCDN, newImages[:40])
    



if __name__ == "__main__":
    getEntireDataSet()