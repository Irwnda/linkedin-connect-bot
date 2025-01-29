import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()

def login_linkedin(driver):
    driver.get("https://linkedin.com/login")
    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    password = driver.find_element(By.XPATH, "//input[@name='session_password']")

    username.send_keys(os.environ["LINKEDIN_EMAIL"])
    password.send_keys(os.environ["LINKEDIN_PASSWORD"])

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

def set_login_state(driver, url):
    cookie = os.environ["LI_AT"]
    if cookie is not None:
        driver.add_cookie({"name": "li_at",
                       "value": os.environ["LI_AT"]})
        driver.refresh()
    else:
        login_linkedin(driver)