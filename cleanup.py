import os


for p in os.listdir("./images"):
    
    if (os.stat(f"./images/{p}").st_size // 1024) < 10:
        
        os.remove(f"./images/{p}")