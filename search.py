import argparse
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.confirmation import handle_confirmation
from utils.login import set_login_state
from dotenv import load_dotenv

load_dotenv()
driver = webdriver.Chrome()
parser = argparse.ArgumentParser(description="Add LinkedIn connection based on the search filter")

parser.add_argument("--keyword", type=str, help='Keyword to search for, use double quotes ("...") for multiple words')
parser.add_argument("--location", type=str,
                    help="The location of connection you're looking for, use comma (..,..) for multiple locations")
parser.add_argument("--company", type=str,
                    help="The company of connection you're looking for, use comma (..,..) for multiple companies")


def handle_filter(selector, filter_values):
    time.sleep(3)
    filter_button = driver.find_element(By.CSS_SELECTOR, selector)
    filter_button.click()
    filter_button_wrapper = filter_button.find_element(By.XPATH, '..')

    dropdown = filter_button_wrapper.find_element(By.XPATH, "preceding-sibling::div")
    input_text = dropdown.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    filter_button = dropdown.find_elements(By.TAG_NAME, 'button')[2]

    for filter_value in filter_values:
        input_text.send_keys(filter_value)
        time.sleep(2)
        search_result = driver.find_element(By.CLASS_NAME, 'search-typeahead-v2__hit')
        search_result.click()
        input_text.clear()

    filter_button.click()


def handle_location(locations):
    handle_filter('#searchFilter_geoUrn', locations)


def handle_company(companies):
    handle_filter('#searchFilter_currentCompany', companies)


def get_filtered_account_list_element(main_element, ul_index=0):
    result_wrapper = main_element.find_elements(By.TAG_NAME, 'ul')[ul_index]
    results = result_wrapper.find_elements(By.TAG_NAME, 'li')

    if len(results) < 10:
        return get_filtered_account_list_element(main_element, ul_index + 1)

    return results


def connect_all():
    main_element = driver.find_element(By.TAG_NAME, 'main')
    results = get_filtered_account_list_element(main_element)

    for result in results:
        buttons = result.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            aria_label = button.get_attribute('aria-label')
            if aria_label and 'connect' in aria_label:
                button.click()
                handle_confirmation(driver)


def change_page(page):
    parsed_url = urlparse(driver.current_url)
    query_params = parse_qs(parsed_url.query)

    query_params['page'] = [str(page)]
    new_query_string = urlencode(query_params, doseq=True)

    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query_string,
        parsed_url.fragment
    ))

    driver.get(new_url)
    time.sleep(3)


def proceed(url):
    driver.get(url)
    set_login_state(driver, url)

    if args.location is not None:
        handle_location(args.location.split(','))

    if args.company is not None:
        handle_company(args.company.split(','))

    time.sleep(3)
    connect_all()
    current_page = 2

    while current_page < 10:
        change_page(current_page)

        connect_all()
        current_page += 1


if __name__ == '__main__':
    args = parser.parse_args()
    search_url = 'https://www.linkedin.com/search/results/people/?network=%5B%22S%22%2C%22O%22%5D'
    if args.keyword:
        search_url += '&keywords=' + args.keyword
    proceed(search_url)
