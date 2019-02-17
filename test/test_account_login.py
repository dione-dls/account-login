#!/usr/bin/env python3
import unittest
from selenium import webdriver


class TestAccountLogin(unittest.TestCase):

    login_page = "https://app.perkbox.com"
    registered_user = "pooja@perkbox.co.uk"
    scroll = "window.scrollTo(0, document.body.scrollHeight);"
    continue_btn = "login__global-login__btn-submit"
    confirm_btn = "login__global-login__tenant-select__btn-submit"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(30)
        self.driver.fullscreen_window()
        self.driver.get(self.login_page)
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_name("email").click()

    def tearDown(self):
        self.driver.close()

    def scroll_then_click_submit_button(self, button):
        self.driver.execute_script(self.scroll)
        self.driver.find_element_by_id(button).click()
        self.driver.implicitly_wait(20)

    def input_email(self, input_):
        return self.driver.find_element_by_name("email").send_keys(input_)

    def show_text(self, element, text):
        return self.driver.find_element_by_xpath(f"//{element}[contains(text(),'{text}')]")


if __name__ == "main":
    unittest.main()
