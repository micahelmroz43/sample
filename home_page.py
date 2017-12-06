from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from test import locator, quote, trace
from . import folia_overview


folia_name = 'Peaches'
default_folia = 'Welcome to Folia!'


class Locator:
    ADD_FOLIA_BUTTON = locator.create_folia.add_folia_button
    ADD_FOLIA_POPUP_TITLE = locator.create_folia.add_folia_popup_title_text
    ADD_FOLIA_TEXTBOX = locator.create_folia.add_folia_textbox
    CLOSE_ACCOUNT_SETTINGS_BUTTON = locator.account_settings.close_button
    CONFIRM_ADD_FOLIA_BUTTON = locator.create_folia.add_folia_confirm_button
    CONFIRM_ADD_FOLIA_CSS = locator.create_folia.add_folia_confirm_button_css
    CONFIRM_DELETE_FOLIA_BUTTON = locator.delete_folia.confirm_delete_button
    DELETE_FOLIA_BUTTON = locator.home_page.delete_folia_button
    DELETE_FOLIA_POPUP_TITLE = locator.delete_folia.delete_folia_popup_title
    FOLIA_COUNT = locator.home_page.folia_count
    FOLIA_NAME_TEXT = locator.home_page.folia_name_text
    FOLIA_OPTIONS_BUTTON = locator.home_page.folia_options_button
    FOLIA_PAGE_TITLE = locator.folia_overview.folia_title
    GENERAL_FOLIA_TITLE = locator.home_page.general_folia_title_text
    LOGOUT_BUTTON = locator.account_settings.logout_button
    SIGN_IN_BUTTON = locator.login.sign_in_button
    SITE_POPUP_CANCEL = locator.site_wide.popup_cancel_button
    SITE_WHITESPACE = locator.site_wide.whitespace

    @classmethod
    def folia_name_text(cls, name=None):
        folia_name_text = locator.home_page.folia_name_text
        if not name:
            return folia_name_text
        return folia_name_text.replace('folia_name', quote(name))

    @classmethod
    def folia_options_path(cls, name=None):
        folia_name_text = Locator.folia_name_text(name or folia_name)
        return folia_name_text + Locator.FOLIA_OPTIONS_BUTTON


@trace
def check_if_confirm_delete_popup_open(driver):
    return driver.verify_element(By.XPATH, Locator.CONFIRM_DELETE_FOLIA_BUTTON)


@trace
def check_if_folia_already_exists(driver):
    return driver.verify_element(By.XPATH, Locator.folia_name_text(folia_name))


@trace
def check_if_folia_name_entered_in_textbox(driver):
    locator_path = Locator.ADD_FOLIA_TEXTBOX
    textbox = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    return textbox.get_attribute('value') == folia_name


@trace
def check_if_new_folia_needs_confirmation(driver):
    locator_path = folia_overview.Locator.FOLIA_TITLE
    return driver.verify_element(By.CSS_SELECTOR, locator_path)


@trace
def check_if_new_folia_popup_open(driver):
    return driver.verify_element(By.CSS_SELECTOR, Locator.ADD_FOLIA_TEXTBOX)


@trace
def check_if_folia_options_popup_open(driver):
    return driver.verify_element(By.CSS_SELECTOR, Locator.DELETE_FOLIA_BUTTON)


@trace
def click_account_settings_button(driver):
    driver.click_element(By.XPATH, Locator.CLOSE_ACCOUNT_SETTINGS_BUTTON)


@trace
def click_existing_folia(driver, folia_name):
    driver.click_element(By.XPATH, Locator.folia_name_text(folia_name))
    driver.verify_element(By.XPATH, folia_overview.Locator.SUBTITLE)


@trace
def click_folia_options_button(driver):
    driver.click_element(By.XPATH, Locator.folia_options_path())
    driver.verify_element(By.CSS_SELECTOR, Locator.DELETE_FOLIA_BUTTON)


@trace
def click_delete_folia(driver):
    driver.click_element(By.CSS_SELECTOR, Locator.DELETE_FOLIA_BUTTON)


@trace
def confirm_delete_folia(driver):
    driver.click_element(By.XPATH, Locator.CONFIRM_DELETE_FOLIA_BUTTON)


@trace
def confirm_new_folia(driver):
    driver.click_element(By.XPATH, Locator.CONFIRM_ADD_FOLIA_BUTTON)
    driver.verify_element(By.CSS_SELECTOR, folia_overview.Locator.FOLIA_TITLE)


@trace
def click_new_folia_button(driver):
    driver.click_element(By.CSS_SELECTOR, Locator.ADD_FOLIA_BUTTON)
    driver.verify_element(By.CSS_SELECTOR, Locator.ADD_FOLIA_TEXTBOX)


@trace
def click_whitespace(driver):
    driver.click_element(By.CSS_SELECTOR, Locator.SITE_WHITESPACE)


@trace
def enter_folia_name(driver):
    locator_path = Locator.ADD_FOLIA_TEXTBOX
    driver.enter_text(By.CSS_SELECTOR, locator_path, folia_name)
    textbox = driver.get_visible_element(By.CSS_SELECTOR, locator_path)
    assert textbox.get_attribute('value') == folia_name


@trace
def open_default_folia(driver, default_folia):
    driver.click_element(By.XPATH, Locator.folia_name_text(default_folia))


@trace
def click_popup_close_button(driver):
    driver.click_element(By.CSS_SELECTOR, Locator.SITE_POPUP_CANCEL)


def delete_folia(driver):
    click_folia_options_button(driver)
    click_delete_folia(driver)
    confirm_delete_folia(driver)
    try:
        check_if_folia_already_exists(driver)
    except NoSuchElementException:
        return False
    return True
