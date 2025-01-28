import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()
driver = webdriver.Chrome()

def login_linkedin():
    driver.get("https://linkedin.com/login")
    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    password = driver.find_element(By.XPATH, "//input[@name='session_password']")

    username.send_keys(os.environ["LINKEDIN_EMAIL"])
    password.send_keys(os.environ["LINKEDIN_PASSWORD"])

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

def set_login_state(url):
    cookie = os.environ["LI_AT"]
    if cookie is not None:
        driver.add_cookie({"name": "li_at",
                       "value": os.environ["LI_AT"]})
        driver.refresh()
    else:
        login_linkedin(url)

def open_url(url):
    driver.get(url)
    set_login_state(url)

def open_profile(link):
    link.click()
    original_window = driver.current_window_handle
    time.sleep(2)
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break

    connect()
    driver.close()
    driver.switch_to.window(original_window)

def show_likes():
    driver.find_element(By.XPATH, "//button[@data-reaction-details]").click()
    time.sleep(2)

    reactors = driver.find_elements(By.CLASS_NAME, "social-details-reactors-tab-body-list-item")
    for reactor in reactors:
        link = reactor.find_element(By.CSS_SELECTOR, "a")
        if '1st' in link.text:
            continue
        open_profile(link)

def check_confirmation():
    time.sleep(2)
    modal_buttons = driver.find_element(By.CLASS_NAME, 'send-invite').find_elements(By.TAG_NAME, 'button')
    for button in modal_buttons:
        if button.get_attribute('aria-label') == 'Send without a note':
            button.click()

def connect():
    time.sleep(5)
    action_buttons_wrapper = driver.find_element(By.CLASS_NAME, "umjiWHzhkMWxuVrcgedbAbMsQbYPbDdZ")
    action_buttons = action_buttons_wrapper.find_elements(By.TAG_NAME, "button")

    connect_button = None
    more_button = None
    for action_button in action_buttons:
        if action_button.text == "Pending":
            return
        if action_button.text == "Connect":
            connect_button = action_button
            break
        if action_button.text == "More":
            more_button = action_button

    if connect_button is not None:
        connect_button.click()
        check_confirmation()
        return
    else:
        more_button.click()

    dropdown = driver.find_elements(By.CLASS_NAME, 'UNBVgWooMfixbYCCrteHxZUAkbEaIuMMo')[1]
    li_elements = dropdown.find_elements(By.TAG_NAME, 'li')
    for li_element in li_elements:
        div_element = li_element.find_element(By.TAG_NAME, 'div')
        if 'connect' in div_element.get_attribute('aria-label'):
            div_element.click()
            check_confirmation()
            break

def proceed(target_url):
    open_url(target_url)
    show_likes()
    driver.quit()

if __name__ == '__main__':
    url = os.getenv("TARGET_URL")
    proceed(url)
