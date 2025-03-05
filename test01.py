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
    try:
        print("در حال یافتن فیلد 'Total Flow' با استفاده از CSS Selector...")
        total_flow_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#client-modal > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > form > div:nth-child(5) > div.ant-col.ant-col-md-14.ant-form-item-control-wrapper > div > span > div > div.ant-input-number-input-wrap > input"
            ))
        )
        # پاکسازی اولیه با استفاده از clear()
        total_flow_input.clear()
        time.sleep(0.5)
        # استفاده از JavaScript برای پاکسازی قطعی مقدار و به‌روز کردن وضعیت داخلی (dispatch event)
        browser.execute_script(
            "arguments[0].value=''; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
            total_flow_input
        )
        time.sleep(0.5)
        # ارسال مقدار جدید به صورت تنها یکبار
        total_flow_input.send_keys(new_value)
        print(f"مقدار فیلد 'Total Flow' به {new_value} تغییر یافت.")
    except Exception as e:
        print("خطا در تغییر مقدار 'Total Flow':", e)




def toggle_start_after_first_use_and_capture():
    try:
        # ارسال یک بار کلید TAB برای رفتن به دکمه "Start After First Use"
        print("در حال ارسال 1 بار کلید TAB جهت رسیدن به دکمه 'Start After First Use'...")
        actions = ActionChains(browser)
        actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)  # صبر برای انتقال فوکوس
        
        # حالا کلید SPACE را ارسال می‌کنیم تا دکمه تغییر حالت دهد.
        print("در حال فشار دادن کلید SPACE برای فعال‌سازی 'Start After First Use'...")
        actions = ActionChains(browser)
        actions.send_keys(Keys.SPACE)
        actions.perform()
        time.sleep(2)  # صبر برای اعمال تغییر حالت
        
        # گرفتن اسکرین‌شات جدید از وضعیت
        start_after_screenshot_path = os.path.join("/root/Screen/", "start_after_result.png")
        take_full_page_screenshot(browser, start_after_screenshot_path)
        print("اسکرین‌شات جدید از وضعیت 'Start After First Use' در مسیر ذخیره شد:", start_after_screenshot_path)
        
    except Exception as e:
        print("خطا در عملیات تغییر وضعیت 'Start After First Use' یا گرفتن اسکرین‌شات:", e)


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


def update_duration_field_and_capture(new_value="21"):
    try:
        print("در حال ارسال یک بار کلید TAB جهت انتقال به فیلد 'Duration'...")
        actions = ActionChains(browser)
        actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)  # صبر برای انتقال فوکوس
        
        # دریافت عنصری که در حال حاضر فوکوس دارد (که باید فیلد Duration باشد)
        active_elem = browser.switch_to.active_element
        print("عنصر فعال، که باید مربوط به فیلد 'Duration' باشد، یافته شد.")
        
        # پاک‌سازی مقدار فعلی فیلد 'Duration'
        print("در حال پاک کردن مقدار فعلی در فیلد 'Duration'...")
        browser.execute_script("arguments[0].value='';", active_elem)
        time.sleep(0.5)
        
        # وارد کردن مقدار جدید
        print("در حال وارد کردن مقدار جدید برای فیلد 'Duration'...")
        active_elem.send_keys(new_value)
        print(f"مقدار فیلد 'Duration' به {new_value} تغییر یافت.")
        
        # گرفتن اسکرین‌شات از وضعیت جدید
        duration_screenshot_path = os.path.join("/root/Screen/", "duration_updated.png")
        take_full_page_screenshot(browser, duration_screenshot_path)
        print("اسکرین‌شات وضعیت به‌روز شده فیلد 'Duration' در مسیر ذخیره شد:", duration_screenshot_path)
        
    except Exception as e:
        print("خطا در به‌روزرسانی فیلد 'Duration':", e)


def save_changes_and_capture():
    try:
        print("در حال ارسال 3 بار کلید TAB جهت انتقال به دکمه 'Save Changes'...")
        actions = ActionChains(browser)
        for _ in range(3):
            actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)  # صبر برای انتقال فوکوس به دکمه 'Save Changes'
        
        # دریافت عنصر فعال پس از ارسال TAB
        active_elem = browser.switch_to.active_element
        print("عنصر فعال (که باید دکمه 'Save Changes' باشد) یافته شد. در حال کلیک روی آن...")
        
        # کلیک روی دکمه Save Changes (می‌توانید از active_elem.click() استفاده کنید یا از دستور JavaScript برای اطمینان استفاده نمایید)
        try:
            active_elem.click()
        except Exception:
            browser.execute_script("arguments[0].click();", active_elem)
        print("کلیک روی دکمه 'Save Changes' انجام شد.")
        time.sleep(3)  # صبر جهت بارگذاری کامل پس از ذخیره تغییرات
        
        # گرفتن اسکرین‌شات از وضعیت نهایی
        save_screenshot_path = os.path.join("/root/Screen/", "save_changes_result.png")
        take_full_page_screenshot(browser, save_screenshot_path)
        print("اسکرین‌شات نتیجه ذخیره تغییرات در مسیر ذخیره شد:", save_screenshot_path)
        
    except Exception as e:
        print("خطا در عملیات 'Save Changes':", e)


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
toggle_start_after_first_use_and_capture()
print("تا اینجا عملیات در پنجره 'Edit Client' انجام شده. اکنون به مرحله تغییر مقدار فیلد 'Duration' می‌رویم.")
update_duration_field_and_capture("21")
print("تا اینجا عملیات ویرایش پنجره 'Edit Client' انجام شد. اکنون به مرحله ذخیره تغییرات (Save Changes) می‌رویم.")
save_changes_and_capture()
print("عملیات تمدید اشتراک کاربر با موفقیت انجام شد.")
browser.quit()
print("مرورگر بسته شد.")
