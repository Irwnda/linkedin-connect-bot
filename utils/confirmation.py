import time

from selenium.webdriver.common.by import By


def handle_confirmation(driver):
    time.sleep(2)
    modal_buttons = driver.find_element(By.CLASS_NAME, 'send-invite').find_elements(By.TAG_NAME, 'button')
    for button in modal_buttons:
        if button.get_attribute('aria-label') == 'Send without a note':
            button.click()
