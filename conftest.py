import pytest
import xvfbwrapper

from selenium import webdriver
from selenium.webdriver.common.by import By

from test import content_view, folia_overview, home_page, login
from test.webdriver import WebDriver


@pytest.fixture(scope='session', autouse=True)
def driver():
    'Get WebDriver / launch Xvfb'
    xvfb = xvfbwrapper.Xvfb(width=1920, height=1280)
    xvfb.start()
    driver = WebDriver(webdriver.Chrome())
    yield driver
    driver.quit()
    xvfb.stop()


@pytest.fixture(scope='function')
def display_login_url(driver):
    'Display login URL'
    login.display_login_url(driver)


@pytest.fixture(scope='function')
def sign_in(driver, display_login_url):
    'Sign in (if necessary)'
    if driver.current_page == 'login':
        login.sign_in(driver)


# Folia Home Test

@pytest.fixture(scope='function')
def click_new_folia_button(driver, sign_in):
    'Click on New Folia Button'
    if not home_page.check_if_new_folia_popup_open(driver):
        home_page.click_new_folia_button(driver)


@pytest.fixture(scope='function')
def enter_new_folia_name(driver, click_new_folia_button):
    'Enter Folia Name in Textbox'
    if not home_page.check_if_folia_name_entered_in_textbox(driver):
        home_page.enter_folia_name(driver)


@pytest.fixture(scope='function')
def confirm_new_folia(driver, enter_new_folia_name):
    "Confirm New Folia"
    if not home_page.check_if_new_folia_needs_confirmation(driver):
        home_page.confirm_new_folia(driver)


@pytest.fixture(scope='function')
def return_to_home_page(driver, confirm_new_folia):
    'Return to Folia Home Page'
    content_view.return_to_home_page(driver)


@pytest.fixture(scope='function')
def click_folia_options(driver, return_to_home_page):
    "Click on the Folia Options Button"
    if not home_page.check_if_folia_options_popup_open(driver):
        home_page.click_folia_options_button(driver)


@pytest.fixture(scope='function')
def click_delete_folia(driver, click_folia_options):
    'Click on the Delete Button in Folia Options Popup'
    if not home_page.check_if_confirm_delete_popup_open(driver):
        home_page.delete_folia(driver)


# Folia Overview Test

@pytest.fixture(scope='session')
def folia_overview_setup(driver):
    'Quickly create new folia for overview tests'
    login.display_login_url(driver)

    if driver.current_page == 'login':
        login.sign_in(driver)

    content_view.return_to_home_page()

    if home_page.check_if_folia_already_exists(driver):
        home_page.click_existing_folia(driver, home_page.folia_name)
    else:
        driver.refresh()
        home_page.click_new_folia_button(driver)
        home_page.enter_folia_name(driver)
        home_page.confirm_new_folia(driver)

    folia_overview.wait_until_loaded(driver)

    yield
    content_view.return_to_home_page()
    home_page.delete_folia(driver)


@pytest.fixture(scope='session')
def add_blank_card(driver, folia_overview_setup):
    'Add a blank card'
    if not folia_overview.check_if_blank_card_exists(driver):
        folia_overview.add_blank_card(driver)


@pytest.fixture(scope='session')
def open_add_document(driver, add_blank_card):
    'Open add document popup'
    if not folia_overview.check_if_blank_card_exists(driver):
        folia_overview.add_blank_card(driver)

    if not folia_overview.check_if_add_document_popup_open(driver):
        folia_overview.add_document_popup_open(driver)


@pytest.fixture(scope='function')
def click_existing_connection(driver, open_add_document):
    'Click existing connection'
    if not folia_overview.check_if_add_document_connection_selected(driver):
        folia_overview.click_existing_connection(driver)


@pytest.fixture(scope='function')
def click_document_to_import(driver, click_existing_connection):
    'Click doc to import'
    if not folia_overview.check_if_document_selected_to_import(driver):
        folia_overview.click_document(driver, folia_overview.document_name)

    folia_overview.wait_until_add_document_popup_closes(driver)


@pytest.fixture(scope='function')
def preview_image_setup(driver, folia_overview_setup):
    if not folia_overview.check_if_blank_card_exists(driver):
        folia_overview.add_blank_card(driver)
        folia_overview.add_document_popup_open(driver)
        folia_overview.click_existing_connection(driver)
        folia_overview.click_document(driver, folia_overview.document_name)
        locator_path = folia_overview.Locator.ADD_DOC_POPUP_TITLE
        driver.get_invisible_element(By.XPATH, locator_path)


@pytest.fixture(scope='function')
def click_subtitle_textbox(driver, folia_overview_setup):
    if not folia_overview.check_if_cursor_in_subtitle_textbox(driver):
        folia_overview.click_subtitle(driver)


@pytest.fixture(scope='session')
def click_description_textbox(driver, add_blank_card):
    if not folia_overview.check_if_cursor_in_card_description_textbox(driver):
        folia_overview.click_card_description(driver)


# Content View Test
@pytest.fixture(scope='session')
def content_view_cleanup(driver, sign_in):
    yield
    if driver.current_page == 'content_view':
        content_view.exit(driver)

    folia_overview.delete_card(driver)


@pytest.fixture(scope='session')
def content_view_setup(driver, content_view_cleanup):
    'Setup: Get to Annotation View'
    if home_page.check_if_folia_already_exists(driver):
        home_page.click_existing_folia(driver)
    else:
        driver.refresh()

        home_page.click_new_folia_button(driver)
        home_page.enter_folia_name(driver)
        home_page.confirm_new_folia(driver)

    folia_overview.wait_until_loaded(driver)

    if not folia_overview.check_if_blank_card_exists(driver):
        folia_overview.add_blank_card(driver)
        folia_overview.add_document_popup_open(driver)
        folia_overview.click_existing_connection(driver)
        folia_overview.click_document(driver, folia_overview.document_name)
        folia_overview.preview_image_spinner_disappears(driver)
        folia_overview.check_card_preview_image_present(driver)

    folia_overview.click_first_card(driver)
    content_view.wait_until_loaded(driver)

    yield
    if content_view.check_if_canvas_present(driver):
        content_view.annotation_switch_to_default_content(driver)

    if not content_view.check_if_comment_popup_open(driver):
        content_view.close_comment_button(driver)

    if content_view.check_close_ink_button_present(driver):
        content_view.confirm_ink_annotation_checkmark(driver)


@pytest.fixture(scope='function')
def open_ink_tool(driver, content_view_setup):
    'Open ink tool'
    content_view.wait_until_loaded(driver)
    locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
    if not driver.verify_element(By.CSS_SELECTOR, locator_path):
        content_view.annotation_open_ink_tool(driver)


@pytest.fixture(scope='function')
def switch_to_iframe(driver, content_view_setup):
    'Switch to iFrame'
    locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
    if driver.verify_element(By.CSS_SELECTOR, locator_path):
        content_view.annotation_switch_to_iframe(driver)

    locator_path = content_view.Locator.RETURN_TO_OVERVIEW
    driver.get_invisible_element(By.XPATH, locator_path)


@pytest.fixture(scope='function')
def create_annotation(driver, content_view_setup):
    'Create an annotation'
    if not content_view.check_if_annotation_exists(driver):
        locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
        if not driver.verify_element(By.CSS_SELECTOR, locator_path):
            content_view.annotation_open_ink_tool(driver)

        locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
        if driver.verify_element(By.CSS_SELECTOR, locator_path):
            content_view.annotation_switch_to_iframe(driver)

        content_view.create_ink_annotation(driver)

        if driver.verify_element(By.CSS_SELECTOR, content_view.Locator.CANVAS):
            content_view.annotation_switch_to_default_content(driver)

    yield
    locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
    if driver.verify_element(By.CSS_SELECTOR, locator_path):
        content_view.confirm_ink_annotation_checkmark(driver)


@pytest.fixture(scope='function')
def create_ink_confirm_annotation(driver, create_annotation):
    'Confirm an annotation'
    locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
    if driver.verify_element(By.CSS_SELECTOR, locator_path):
        content_view.confirm_ink_annotation_checkmark(driver)

    locator_path = content_view.Locator.CLOSE_INK_ANNOTATION
    driver.get_invisible_element(By.XPATH, locator_path)

    locator_path = content_view.Locator.NAV_PANEL_ANNO_COUNT
    driver.verify_element(By.CSS_SELECTOR, locator_path)


@pytest.fixture(scope='function')
def close_ink_tool(driver, create_annotation):
    'Close tool'
    locator_path = content_view.Locator.OPEN_INK_ANNOTATION
    if driver.verify_element(By.XPATH, locator_path):
        content_view.confirm_ink_annotation_checkmark(driver)


@pytest.fixture(scope='function')
def click_anno_nav_panel(driver, create_ink_confirm_annotation):
    'Click the annotation in the nav panel'
    if not content_view.check_if_annotation_options_open(driver):
        content_view.anno_panel_click_first(driver)

    locator_path = content_view.Locator.OPEN_INK_ANNOTATION
    if driver.verify_element(By.XPATH, locator_path):
        content_view.annotation_switch_to_iframe(driver)

    locator_path = content_view.Locator.OPEN_INK_ANNOTATION
    driver.get_invisible_element(By.XPATH, locator_path)


@pytest.fixture(scope='function')
def open_comment_popup(driver, click_anno_nav_panel):
    'Click on the Comment button'
    if not content_view.check_if_comment_popup_open(driver):
        content_view.open_comment_button(driver)

    if driver.verify_element(By.CSS_SELECTOR, content_view.Locator.CANVAS):
        content_view.annotation_switch_to_default_content(driver)


@pytest.fixture(scope='function')
def close_comment_popup(driver, submit_comment):
    'Close the comment popup'
    if content_view.check_if_comment_popup_open(driver):
        content_view.close_comment_button(driver)

    if driver.verify_element(By.CSS_SELECTOR, content_view.Locator.CANVAS):
        content_view.annotation_switch_to_default_content(driver)


@pytest.fixture(scope='function')
def enter_comment(driver, open_comment_popup):
    'Enter comment in textbox'
    if content_view.check_if_comment_popup_open(driver):
        content_view.enter_comment(driver)


@pytest.fixture(scope='function')
def submit_comment(driver, enter_comment):
    'Submit a comment'
    if content_view.check_if_comment_popup_open(driver):
        content_view.submit_comment(driver)
