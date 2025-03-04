from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# تنظیمات مرورگر و وب‌درایور
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # اجرای بدون نمایش رابط کاربری
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

def login_to_panel(username, password):
    # ورود به صفحه اصلی پنل
    browser.get('http://37.27.253.117:2095')
    time.sleep(2)
    
    try:
        # پیدا کردن فیلدهای ورود
        username_field = browser.find_element(By.NAME, 'username')
        password_field = browser.find_element(By.NAME, 'password')
        print("فیلدهای نام کاربری و رمز عبور پیدا شدند.")
        
        # ارسال اطلاعات ورود
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # بررسی آدرس فعلی پس از ورود
        current_url = browser.current_url
        print("آدرس فعلی پس از ورود:", current_url)
    except Exception as e:
        print("خطا در ورود به پنل:", e)
        # ذخیره صفحه HTML جهت بررسی
        page_source = browser.page_source
        with open("page_source.html", "w", encoding='utf-8') as file:
            file.write(page_source)
        print("کد HTML صفحه ذخیره شد.")

def click_inbounds():
    try:
        # اگر هنوز در صفحه اصلی پنل هستیم، باید روی دکمه Inbounds کلیک کنیم
        time.sleep(2)
        # پیدا کردن دکمه Inbounds با استفاده از تگ <b>
        inbound_element = browser.find_element(By.XPATH, "//b[text()='Inbounds']")
        # اگر نیاز است، ممکن است لازم باشد عنصر والد (مانند دکمه) را کلیک کنیم:
        try:
            inbound_button = inbound_element.find_element(By.XPATH, "./..")
            inbound_button.click()
        except Exception:
            inbound_element.click()
        time.sleep(5)
        
        current_url = browser.current_url
        print("آدرس فعلی پس از کلیک روی Inbounds:", current_url)
        if "panel/inbounds" in current_url:
            print("هدایت به صفحه Inbounds انجام شد.")
        else:
            print("هدایت به صفحه Inbounds انجام نشد.")
    except Exception as e:
        print("خطا در کلیک روی Inbounds:", e)
        screenshot_path = os.path.join("/root/Screen/", "inbounds_error.png")
        browser.save_screenshot(screenshot_path)
        print("اسکرین‌شات خطا در مسیر:", screenshot_path)

# اجرای توابع
login_to_panel('msi', 'msi')
click_inbounds()

browser.quit()
