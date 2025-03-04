import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def take_full_page_screenshot(browser, save_path):
    # تغییر سطح zoom صفحه به 50% برای کوچک‌تر شدن کل محتوا در ویوپورت
    print("در حال تغییر سطح zoom صفحه به 50%...")
    browser.execute_script("document.body.style.zoom='0.5'")
    time.sleep(2)
    
    # گرفتن اسکرین‌شات کامل صفحه بدون نیاز به اسکرول کردن
    print("در حال گرفتن اسکرین‌شات کامل صفحه...")
    browser.save_screenshot(save_path)
    print("اسکرین‌شات صفحه ذخیره شد:", save_path)
    
    # تغییر اندازه تصویر نهایی به 1080x720
    print("در حال تغییر اندازه تصویر نهایی به 1080x720...")
    final_image = Image.open(save_path)
    final_image = final_image.resize((1080, 720), Image.LANCZOS)
    final_image.save(save_path)
    print("تصویر نهایی با ابعاد 1080x720 ذخیره شد.")

def login_to_panel(username, password):
    print("در حال ورود به پنل...")
    browser.get('http://37.27.253.117:2095')
    time.sleep(2)
    print("در حال یافتن فیلدهای نام کاربری و رمز عبور...")
    username_field = browser.find_element(By.NAME, 'username')
    password_field = browser.find_element(By.NAME, 'password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    print("ورود به پنل انجام شد. آدرس فعلی:", browser.current_url)

def click_inbounds():
    print("در حال جستجوی دکمه 'Inbounds'...")
    inbound_element = browser.find_element(By.XPATH, "//b[text()='Inbounds']")
    try:
        inbound_button = inbound_element.find_element(By.XPATH, "./..")
        print("دکمه Inbounds پیدا شد. کلیک روی آن...")
        inbound_button.click()
    except Exception:
        print("مشکل در کلیک روی دکمه Inbounds. تلاش برای کلیک مستقیم روی عنصر...")
        inbound_element.click()
    time.sleep(5)
    print("پس از کلیک روی Inbounds، آدرس فعلی پنل:", browser.current_url)

# تنظیمات مرورگر و راه‌اندازی آن
print("در حال راه‌اندازی مرورگر...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
print("مرورگر راه‌اندازی شد.")

# ورود به پنل و کلیک روی دکمه Inbounds
login_to_panel('msi', 'msi')
click_inbounds()
time.sleep(2)

# گرفتن اسکرین‌شات کامل (تغییر اندازه به 1080x720)
full_screenshot_path = os.path.join("/root/Screen/", "inbounds_page_full_stitched.png")
print("در حال گرفتن اسکرین‌شات کامل صفحه Inbounds...")
take_full_page_screenshot(browser, full_screenshot_path)

browser.quit()
print("مرورگر بسته شد. عملیات تکمیل شد.")
