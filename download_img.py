import os
import requests
counter = 0
file = open('URL.txt', 'r')
lines = file.readlines()
for url in lines:
    if counter >= 923:
        print(counter)
        try:
            print('downloading...')
            print(url[:-1])
            image_content = requests.get(url[:-1], verify=False, timeout=5)
            print('finish')
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
        try:
            f = open(os.path.join('/home/ruizezhang/Desktop/webScraping/images/', 'jpg' +
                                  "_" + str(counter) + ".jpg"), 'wb')
            f.write(image_content.content)
            f.close()
            print(f"SUCCESS - saved {url}")
            counter += 1
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
    else:
        counter += 1
