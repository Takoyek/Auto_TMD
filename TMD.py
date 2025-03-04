import os
import math
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def take_full_page_screenshot(browser, save_path):
    # اسکرول به پایین صفحه جهت بارگذاری تمام محتوای lazy-loaded
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # تغییر سطح zoom به 50% برای کوچک‌تر شدن محتوا در ویوپورت
    browser.execute_script("document.body.style.zoom='0.5'")
    time.sleep(2)
    
    # گرفتن ابعاد کامل صفحه
    total_height = browser.execute_script("return document.body.parentNode.scrollHeight")
    total_width  = browser.execute_script("return document.body.parentNode.scrollWidth")
    viewport_height = browser.execute_script("return window.innerHeight")
    
    # تنظیم اندازه پنجره مرورگر به عرض کامل صفحه
    browser.set_window_size(total_width, viewport_height)
    time.sleep(2)
    
    num_sections = math.ceil(total_height / viewport_height)
    screenshot_files = []
    
    # گرفتن اسکرین‌شات از هر بخش صفحه
    for i in range(num_sections):
        scroll_y = i * viewport_height
        browser.execute_script(f"window.scrollTo(0, {scroll_y});")
        time.sleep(1)
        section_file = os.path.join("/root/Screen/", f"section_{i}.png")
        browser.save_screenshot(section_file)
        screenshot_files.append(section_file)
    
    # ادغام تصاویر اسکرین‌شات
    stitched_image = Image.new("RGB", (total_width, total_height))
    offset = 0
    for idx, file in enumerate(screenshot_files):
        im = Image.open(file)
        # در صورت نیاز کراپ کردن بخش آخر برای حذف فضای خالی (حاشیه مشکی)
        if idx == len(screenshot_files) - 1:
            crop_height = total_height - offset
            if crop_height < im.size[1]:
                im = im.crop((0, 0, im.size[0], crop_height))
        stitched_image.paste(im, (0, offset))
        offset += im.size[1]
    
    # تغییر اندازه نهایی تصویر به 1920x1080 با استفاده از Image.LANCZOS
    final_image = stitched_image.resize((1920, 1080), Image.LANCZOS)
    final_image.save(save_path)
    
    # حذف فایل‌های موقت
    for file in screenshot_files:
        os.remove(file)

def login_to_panel(username, password):
    browser.get('http://37.27.253.117:2095')
    time.sleep(2)
    username_field = browser.find_element(By.NAME, 'username')
    password_field = browser.find_element(By.NAME, 'password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

def click_inbounds():
    inbound_element = browser.find_element(By.XPATH, "//b[text()='Inbounds']")
    try:
        inbound_button = inbound_element.find_element(By.XPATH, "./..")
        inbound_button.click()
    except Exception:
        inbound_element.click()
    time.sleep(5)

# تنظیمات مرورگر
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# ورود به پنل و کلیک روی دکمه Inbounds
login_to_panel('msi', 'msi')
click_inbounds()
time.sleep(2)

# گرفتن اسکرین‌شات کامل (و تغییر اندازه آن به 1920x1080)
full_screenshot_path = os.path.join("/root/Screen/", "inbounds_page_full_stitched.png")
take_full_page_screenshot(browser, full_screenshot_path)

browser.quit()
