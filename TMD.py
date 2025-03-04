import os, math, time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def extend_client_subscription(client_name, extension_days=30):
    print("در حال یافتن فیلد جستجوی کلاینت با placeholder='Search'...")
    try:
        search_input = browser.find_element(By.XPATH, "//input[@placeholder='Search']")
    except Exception as e:
        print("خطا در یافتن فیلد جستجو:", e)
        return

    search_input.clear()
    search_input.send_keys(client_name)
    search_input.send_keys(Keys.RETURN)
    print(f"کلاینت '{client_name}' ارسال شد. در حال جستجو...")
    time.sleep(3)

    try:
        wait = WebDriverWait(browser, 10)
        client_row = wait.until(
            EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{client_name}')]]"))
        )
        print("ردیف کلاینت پیدا شد.")
    except Exception as e:
        print("کلاینت یافت نشد:", e)
        # گرفتن اسکرین‌شات از نتایج جستجو جهت بررسی
        screenshot_path = os.path.join("/root/Screen/", "search_result.png")
        browser.save_screenshot(screenshot_path)
        print("اسکرین‌شات نتایج جستجو ذخیره شد:", screenshot_path)
        return

    try:
        extend_button = client_row.find_element(By.XPATH, ".//button[contains(text(), 'Extend')]")
        print("دکمه تمدید اشتراک پیدا شد. در حال کلیک روی آن...")
        extend_button.click()
    except Exception as e:
        print("خطا در یافتن یا کلیک روی دکمه تمدید اشتراک:", e)
        return

    time.sleep(2)

    try:
        days_input = browser.find_element(By.XPATH, "//input[@name='extensionDays']")
        days_input.clear()
        days_input.send_keys(str(extension_days))
        print(f"تعداد روز {extension_days} وارد شد.")

        confirm_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
        confirm_button.click()
        print("تمدید اشتراک تایید و انجام شد.")
    except Exception as e:
        print("خطا در پردازش فرم تمدید:", e)

    time.sleep(3)


# تنظیمات مرورگر و راه‌اندازی
print("در حال راه‌اندازی مرورگر...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
print("مرورگر راه‌اندازی شد.")

# ورود به پنل و کلیک روی Inbounds
login_to_panel('msi', 'msi')
click_inbounds()
time.sleep(2)

# (اختیاری) گرفتن اسکرین‌شات کامل صفحه
full_screenshot_path = os.path.join("/root/Screen/", "inbounds_page_full_stitched.png")
take_full_page_screenshot(browser, full_screenshot_path)

# فراخوانی تابع تمدید برای کلاینت "FM"
extend_client_subscription("FM", 30)

browser.quit()
