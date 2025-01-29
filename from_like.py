import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException, \
    NoSuchWindowException
from selenium.webdriver.common.by import By
from utils.login import set_login_state
from utils.confirmation import handle_confirmation

load_dotenv()
driver = webdriver.Chrome()

def open_url(url):
    set_login_state(driver, url)

def open_profile(link):
    link.click()
    original_window = driver.current_window_handle
    time.sleep(2)
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break

    try:
        connect()
        driver.close()
    except ElementNotInteractableException:
        print("Element not interactable")
    except NoSuchWindowException:
        print("Window already closed")

    driver.switch_to.window(original_window)

def show_likes():
    driver.find_element(By.XPATH, "//button[@data-reaction-details]").click()
    like_count_element = driver.find_element(By.CLASS_NAME, 'social-details-social-counts__social-proof-fallback-number')
    like_count = int(like_count_element.text)
    visited_account_count = 0
    time.sleep(2)

    while visited_account_count < like_count:
        try:
            scrollable_container = driver.find_element(By.CLASS_NAME, "social-details-reactors-tab-body")
            reactors = driver.find_elements(By.CLASS_NAME, "social-details-reactors-tab-body-list-item")
            while visited_account_count < len(reactors):
                reactor = reactors[visited_account_count]

                link = reactor.find_element(By.CSS_SELECTOR, "a")
                if '1st' in link.text:
                    visited_account_count += 1
                    continue

                open_profile(link)
                visited_account_count += 1
        except StaleElementReferenceException:
            print("Stale element encountered. Retrying...")
            continue
        except NoSuchElementException:
            print("No element encountered. Retrying...")
            driver.close()
            continue

        driver.execute_script(
            "document.querySelector('.social-details-reactors-tab-body').parentElement.scroll(0, arguments[0].offsetHeight);",
            scrollable_container
        )
        time.sleep(3)

def connect():
    time.sleep(2)
    more_button = driver.find_elements(By.XPATH, "//button[@aria-label='More actions']")[1]
    action_buttons_wrapper = more_button.find_element(By.XPATH, '../..')
    action_buttons = action_buttons_wrapper.find_elements(By.TAG_NAME, "button")

    connect_button = None
    for action_button in action_buttons:
        if action_button.text == "Pending":
            return
        if action_button.text == "Connect":
            connect_button = action_button
            break

    if connect_button is not None:
        connect_button.click()
        handle_confirmation(driver)
        return
    else:
        more_button.click()

    dropdown = more_button.find_element(By.XPATH, "following-sibling::div")
    li_elements = dropdown.find_elements(By.TAG_NAME, 'li')
    for li_element in li_elements:
        div_element = li_element.find_element(By.TAG_NAME, 'div')
        try:
            if 'connect' in div_element.get_attribute('aria-label'):
                div_element.click()
                handle_confirmation(driver)
                break
        except ElementNotInteractableException:
            more_button.click()
            div_element.click()
            handle_confirmation(driver)
            break

def proceed(target_url):
    open_url(target_url)
    show_likes()
    driver.quit()

if __name__ == '__main__':
    url = os.getenv("TARGET_URL")
    proceed(url)
