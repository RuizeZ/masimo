# importing the module
from PIL import Image
import os
path = '/home/ruizezhang/Desktop/webScraping/images/'
path2 = '/home/ruizezhang/Desktop/webScraping/images2/'
os.chdir(path)
for file in os.listdir():
    print(file)
    # importing the image
    try:
        im = Image.open(path + file)
        # converting to jpg
        rgb_im = im.convert("RGB")
        # exporting the image
        rgb_im.save(path2+file)
    except Exception as e:
        print(f"ERROR")
