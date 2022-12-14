
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
image_urls = set()


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 0.5):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_count = 0
    results_start = 0
    while True:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(
            f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        if results_start == number_results:
            print('next term')
            return
        for img in thumbnail_results[results_start:number_results]:
            # image_count += 1
            # if (image_count >= 10):
            #     return
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements(By.CSS_SELECTOR, "img.KAlRDb")
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

        else:
            print("Found:", len(image_urls),
                  "image links, looking for more ...")
            load_more_button = wd.find_elements(By.CSS_SELECTOR, ".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)


def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' +
                 "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term, driver_path: str, target_path='./images', number_images=2):
    target_folder = os.path.join(
        target_path)
    f = open("URL.txt", "w")
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for term in search_term:
        print("current term: " + term)
        with webdriver.Chrome(executable_path=driver_path) as wd:
            fetch_image_urls(term, number_images,
                             wd=wd, sleep_between_interactions=0.5)
    for url in image_urls:
        f.write(url+'\n')
    f.close()
    print('set size: ' + str(len(image_urls)))


DRIVER_PATH = './chromedriver'
search_term = ['hand sanitizing', 'people hand sanitizing', 'patient hand sanitizing']
search_and_download(search_term=search_term, driver_path=DRIVER_PATH)
