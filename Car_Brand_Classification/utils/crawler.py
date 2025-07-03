import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

# Set Chrome options for headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")

# Create folder for images
os.makedirs("car_images", exist_ok=True)

# List of websites to crawl
websites = [
]

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

MIN_WIDTH = 350
MIN_HEIGHT = 200
EXCLUDED_KEYWORDS = ["icon", "placeholder", "thumb", "logo", "favicon"]

# Download image function
def download_image(img_url, folder="car_images"):
    try:
        existing_files = os.listdir(folder)
        existing_indices = [int(f.split("_")[2].split(".")[0]) for f in existing_files if f.startswith("car_img_") and f.endswith(".jpg")]
        next_index = max(existing_indices, default=0) + 1

        img_name = f"car_img_{next_index}.jpg"
        file_path = os.path.join(folder, img_name)

        img_data = requests.get(img_url, headers=headers, timeout=10, verify=False).content

        with open(file_path, "wb") as f:
            f.write(img_data)
        print(f"[+] Lưu thành công: {file_path}")
    except Exception as e:
        print(f"[-] Lỗi khi tải {img_url}: {e}")

# Check if image is valid
def is_valid_image(img):
    try:
        width = int(img.get_attribute("naturalWidth"))
        height = int(img.get_attribute("naturalHeight"))
        if width * height >= MIN_WIDTH and height >= MIN_HEIGHT:
            return True
        else:
            print(f"[-] Bỏ qua ảnh nhỏ: {width}x{height}")
            return False
    except:
        return False

# Check for excluded keywords
def contains_excluded_keywords(img_url):
    for keyword in EXCLUDED_KEYWORDS:
        if keyword in img_url.lower():
            print(f"[-] Bỏ qua ảnh không cần thiết: {img_url}")
            return True
    return False

# Scroll to load more images
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust based on connection speed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Crawl using Selenium
def crawl_with_selenium(url):
    print(f"Đang crawl trang: {url}")
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        # Scroll to load all images
        scroll_to_bottom(driver)

        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Đã tìm thấy {len(images)} ảnh.")

        for idx, img in enumerate(images):
            img_url = img.get_attribute("src") or img.get_attribute("data-src")
            if img_url and img_url.startswith("http"):
                if not contains_excluded_keywords(img_url) and is_valid_image(img):
                    download_image(img_url)
                else:
                    print(f"[-] Ảnh bị loại bỏ: {img_url}")
    except Exception as e:
        print(f"[-] Lỗi khi crawl trang: {e}")
    finally:
        driver.quit()

# Main loop to crawl each website
for site in websites:
    try:
        crawl_with_selenium(site)
    except Exception as e:
        print(f"[-] Lỗi không xác định: {e}")
