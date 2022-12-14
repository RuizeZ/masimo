# importing the module
from PIL import Image
import os
path = 'C:/Users/ruize.zhang/Desktop/webscraping/images/'
path2 = 'C:/Users/ruize.zhang/Desktop/webscraping/hand_sanitizing/'
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