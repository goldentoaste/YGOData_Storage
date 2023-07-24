import os, sys
from multiprocessing.pool import Pool
import requests, json
import time
from PIL import Image

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
            


def getEntireDataSet():
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

    with Pool(10) as pool:
        workerpool = pool.map(downloadImage, [(i, urls[i]) for i in range(len(urls))])

    with open( "updateList.json", 'r', encoding='utf-8' ) as f:
        
        updates = json.load(f)
        updates[str(int(time.time()))] = addedImages
        
        with open( "updateList.json", 'w', encoding='utf-8' ) as wp:
            json.dump(updates, wp)


if __name__ == "__main__":
    getEntireDataSet()


'''
with open( "updateList.json", 'r', encoding='utf-8' ) as f:
    
    updates = json.load(f)
    updates[str(int(time.time()))] = os.listdir('./images')
    
    with open( "updateList.json", 'w', encoding='utf-8' ) as wp:
        json.dump(updates, wp)
'''