import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    try:
        inbound_element = browser.find_element(By.XPATH, "//b[text()='Inbounds']")
        try:
            inbound_button = inbound_element.find_element(By.XPATH, "./..")
            print("دکمه Inbounds پیدا شد. کلیک روی آن...")
            inbound_button.click()
        except Exception:
            print("مشکل در دریافت دکمه والد دکمه Inbounds. تلاش برای کلیک مستقیم روی عنصر...")
            inbound_element.click()
    except Exception as e:
        print("خطا در یافتن دکمه Inbounds:", e)
    time.sleep(5)
    print("پس از کلیک، آدرس فعلی:", browser.current_url)

def expand_all_inbound_rows():
    print("در حال باز کردن زیرمجموعه‌های اینباند (Expand row)...")
    try:
        expand_buttons = browser.find_elements(
            By.XPATH, "//div[@role='button' and @aria-label='Expand row' and contains(@class, 'ant-table-row-collapsed')]"
        )
        print(f"{len(expand_buttons)} دکمه برای باز کردن زیرمجموعه‌ها پیدا شدند.")
        for btn in expand_buttons:
            btn.click()
            time.sleep(1)  # صبر برای باز شدن هر ردیف
        print("تمامی زیرمجموعه‌های اینباند باز شدند.")
    except Exception as e:
        print("خطا در باز کردن زیرمجموعه‌های اینباند:", e)

def search_client_and_capture(client_name):
    print("در حال یافتن فیلد جستجوی کلاینت با placeholder='Search'...")
    try:
        search_input = browser.find_element(By.XPATH, "//input[@placeholder='Search']")
    except Exception as e:
        print("خطا در یافتن فیلد جستجو:", e)
        return

    search_input.clear()
    search_input.send_keys(client_name)
    search_input.send_keys(Keys.RETURN)
    print(f"نام کلاینت '{client_name}' ارسال شد. در حال جستجو...")
    time.sleep(3)

    # گزینه ۱: گرفتن اسکرین‌شات کامل با تابع take_full_page_screenshot
    full_search_screenshot = os.path.join("/root/Screen/", "search_result_full.png")
    take_full_page_screenshot(browser, full_search_screenshot)
    print("اسکرین‌شات کامل نتایج جستجو ذخیره شد در:", full_search_screenshot)


def take_full_page_screenshot(browser, save_path):
    # تغییر سطح zoom به 50% برای کوچک‌تر شدن کل محتوا در ویوپورت
    print("در حال تغییر سطح zoom صفحه به 50%...")
    browser.execute_script("document.body.style.zoom='0.5'")
    time.sleep(2)
    
    # گرفتن اسکرین‌شات کامل صفحه
    print("در حال گرفتن اسکرین‌شات صفحه...")
    browser.save_screenshot(save_path)
    print("اسکرین‌شات صفحه ذخیره شد:", save_path)
    
    # تغییر اندازه تصویر نهایی به 1080x720
    print("در حال تغییر اندازه تصویر نهایی به 1080x720...")
    final_image = Image.open(save_path)
    final_image = final_image.resize((1080, 720), Image.LANCZOS)
    final_image.save(save_path)
    print("تصویر نهایی با ابعاد 1080x720 ذخیره شد.")

# تنظیمات مرورگر و راه‌اندازی آن
print("در حال راه‌اندازی مرورگر...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')             # اجرای برنامه به صورت headless
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
print("مرورگر راه‌اندازی شد.")

# اجرای مراحل اصلی:
login_to_panel('msi', 'msi')
click_inbounds()
time.sleep(2)

# باز کردن زیرمجموعه‌های اینباند برای نمایش کلاینت‌ها
expand_all_inbound_rows()

# جستجو برای کلاینت "FM" و گرفتن اسکرین‌شات از نتایج جستجو
search_client_and_capture("FM")

# (اختیاری) گرفتن اسکرین‌شات از صفحه Inbounds پس از انجام عملیات
full_screenshot_path = os.path.join("/root/Screen/", "inbounds_page_full_stitched.png")
take_full_page_screenshot(browser, full_screenshot_path)

print("تا اینجا عملیات باز کردن زیرمجموعه‌ها و جستجوی کلاینت به پایان رسید. منتظر دستور بعدی شما هستیم.")
browser.quit()
print("مرورگر بسته شد.")
