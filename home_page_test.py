from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from test import folia_overview, home_page


def test_click_new_folia_button(driver, folia_home_setup):
    home_page.click_new_folia_button(driver)

    locator_path = home_page.Locator.ADD_FOLIA_POPUP_TITLE
    popup_title = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    assert popup_title.text == 'New Folia'


def test_new_folia_enter_name(driver, click_new_folia_button):
    home_page.enter_folia_name(driver)

    locator_path = home_page.Locator.ADD_FOLIA_TEXTBOX
    textbox = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    assert textbox.get_attribute('value') == home_page.folia_name


def test_new_folia_click_confirm(driver, enter_new_folia_name):
    home_page.confirm_new_folia(driver)

    locator_path = folia_overview.Locator.FOLIA_TITLE
    folia_title = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    assert folia_title.get_attribute('value') == home_page.folia_name


def test_verify_new_folia_on_home_page(driver, confirm_new_folia):
    folia_overview.exit(driver)
    driver.verify_element(By.XPATH, home_page.Locator.folia_name_text())


def test_home_page_click_options_button(driver, return_to_home_page):
    home_page.click_folia_options_button(driver)

    locator_path = home_page.Locator.DELETE_FOLIA_BUTTON
    driver.verify_element(By.CSS_SELECTOR, locator_path)


def test_home_page_click_delete_folia_button(driver, click_folia_options):
    home_page.click_delete_folia(driver)

    locator_path = home_page.Locator.DELETE_FOLIA_POPUP_TITLE
    popup_title = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    assert popup_title.text == 'Delete'


def test_confirm_delete(driver, click_delete_folia):
    home_page.confirm_delete_folia(driver)

    try:
        driver.find_element(By.XPATH, home_page.Locator.folia_name_text())
    except NoSuchElementException:
        return False
    return True
