import os
import math
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def take_full_page_screenshot(browser, save_path):
    print("در حال تغییر سطح zoom صفحه به 50%...")
    browser.execute_script("document.body.style.zoom='0.5'")
    time.sleep(2)
    print("در حال گرفتن اسکرین‌شات صفحه...")
    browser.save_screenshot(save_path)
    print("اسکرین‌شات صفحه ذخیره شد:", save_path)
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
    try:
        inbound_element = browser.find_element(By.XPATH, "//b[text()='Inbounds']")
        try:
            inbound_button = inbound_element.find_element(By.XPATH, "./..")
            print("دکمه Inbounds پیدا شد. در حال کلیک روی آن...")
            inbound_button.click()
        except Exception:
            print("مشکل در دریافت دکمه والد. تلاش برای کلیک مستقیم روی عنصر...")
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
            time.sleep(1)
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
    full_search_screenshot = os.path.join("/root/Screen/", "search_result_full.png")
    take_full_page_screenshot(browser, full_search_screenshot)
    print("اسکرین‌شات کامل نتایج جستجو ذخیره شد در:", full_search_screenshot)

def click_edit_client_button_and_capture():
    try:
        print("در حال یافتن دکمه 'Edit Client' با استفاده از CSS Selector...")
        wait = WebDriverWait(browser, 10)
        edit_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "i.normal-icon.anticon.anticon-edit"))
        )
        print("عنصر دکمه 'Edit Client' پیدا شد. در حال کلیک روی آن با استفاده از JavaScript...")
        browser.execute_script("arguments[0].click();", edit_elem)
        print("کلیک روی دکمه 'Edit Client' انجام شد.")
        time.sleep(5)
        result_screenshot_path = os.path.join("/root/Screen/", "edit_client_result.png")
        take_full_page_screenshot(browser, result_screenshot_path)
        print("اسکرین‌شات نتیجه 'Edit Client' در مسیر ذخیره شد:", result_screenshot_path)
    except Exception as e:
        print("خطا در عملیات کلیک روی دکمه 'Edit Client' یا در گرفتن اسکرین‌شات:", e)

# توابع برای استفاده از ارسال کلید TAB جهت دستیابی به فیلد "Total Flow"
def go_to_total_flow_field_by_tab(tab_count=6):
    print(f"در حال ارسال {tab_count} بار کلید TAB جهت رسیدن به فیلد 'Total Flow'...")
    actions = ActionChains(browser)
    for _ in range(tab_count):
        actions.send_keys(Keys.TAB)
    actions.perform()
    time.sleep(1)

def edit_total_flow_value(new_value):
    go_to_total_flow_field_by_tab(6)
    active = browser.switch_to.active_element
    active.clear()
    active.send_keys(new_value)
    print(f"مقدار فیلد 'Total Flow' به {new_value} تغییر یافت.")

def edit_client_window_and_capture():
    try:
        print("در حال انتظار برای بارگذاری کامل پنجره 'Edit Client'...")
        time.sleep(3)
        
        # گرفتن اسکرین‌شات قبل از تغییر در پنجره Edit Client
        before_path = os.path.join("/root/Screen/", "edit_client_before.png")
        take_full_page_screenshot(browser, before_path)
        print("اسکرین‌شات قبل از تغییرات ذخیره شد:", before_path)
        
        # فقط تغییر در فیلد "Total Flow"
        print("در حال تغییر مقدار 'Total Flow' با استفاده از کلید TAB...")
        edit_total_flow_value("7")
        
        # صبر برای اعمال تغییرات
        time.sleep(2)
        
        # گرفتن اسکرین‌شات بعد از تغییرات
        after_path = os.path.join("/root/Screen/", "edit_client_after.png")
        take_full_page_screenshot(browser, after_path)
        print("اسکرین‌شات بعد از تغییرات ذخیره شد:", after_path)
        
    except Exception as e:
        print("خطا در عملیات ویرایش پنجره 'Edit Client':", e)

# ------------------ Main Program ------------------
print("در حال راه‌اندازی مرورگر...")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
print("مرورگر راه‌اندازی شد.")

login_to_panel('msi', 'msi')
click_inbounds()
time.sleep(2)
expand_all_inbound_rows()
search_client_and_capture("FM")
full_screenshot_path = os.path.join("/root/Screen/", "inbounds_page_full_stitched.png")
take_full_page_screenshot(browser, full_screenshot_path)
print("تا اینجا عملیات باز کردن زیرمجموعه‌ها و جستجوی کلاینت به پایان رسید. اکنون در مرحله 'Edit Client' هستیم.")
click_edit_client_button_and_capture()
edit_client_window_and_capture()
print("تا اینجا عملیات ویرایش پنجره 'Edit Client' و گرفتن اسکرین‌شات قبل و بعد از تغییر انجام شد. منتظر دستور بعدی شما هستیم.")
browser.quit()
print("مرورگر بسته شد.")
