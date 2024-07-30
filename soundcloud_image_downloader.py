# python soundcloud_image_downloader.py "https://soundcloud.com/ezzye-1/sets/london-n9-1"
# pip install requests beautifulsoup4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import os
import sys
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    return webdriver.Chrome(options=chrome_options)

def get_track_urls(driver, playlist_url):
    driver.get(playlist_url)

    # Scroll to load all tracks
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait for tracks to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".trackItem__trackTitle"))
    )

    track_elements = driver.find_elements(By.CSS_SELECTOR, ".trackItem__trackTitle")
    return [elem.get_attribute('href') for elem in track_elements]

def download_image(track_url, folder):
    response = requests.get(track_url)
    if response.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find('meta', property='og:image')
        if image_tag and 'content' in image_tag.attrs:
            image_url = image_tag['content']
            image_name = soup.find('meta', property='og:title')['content'] if soup.find('meta', property='og:title') else 'unknown'

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                filename = os.path.join(folder, f"{image_name}.jpg")
                with open(filename, 'wb') as f:
                    f.write(image_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image for: {image_name}")
        else:
            print(f"No image found for: {track_url}")
    else:
        print(f"Failed to access: {track_url}")

def main(playlist_url):
    driver = setup_driver()
    try:
        track_urls = get_track_urls(driver, playlist_url)

        # Create folder for downloads
        folder_name = "soundcloud_images"
        os.makedirs(folder_name, exist_ok=True)

        for url in track_urls:
            download_image(url, folder_name)
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <playlist_url>")
        sys.exit(1)

    playlist_url = sys.argv[1]
    main(playlist_url)