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

    def test_no_email_input(self):
        self.scroll_then_click_submit_button(self.continue_btn)
        self.assertEqual(f"{self.login_page}/welcome/login", self.driver.current_url)
        prompt = self.show_text("div", "Please enter your email")
        self.assertTrue(prompt.is_displayed())

    def test_unregistered_user_email_input(self):
        self.input_email("dione@mail.com")
        self.scroll_then_click_submit_button(self.continue_btn)
        prompt = self.show_text("div", "User is not found")
        self.assertTrue(prompt.is_displayed())

    def test_invalid_email_input(self):
        self.input_email("kgVghgea6778")
        self.scroll_then_click_submit_button(self.continue_btn)
        prompt = self.show_text("div", "This email address is not valid")
        self.assertTrue(prompt.is_displayed())

    def test_registered_user_email_with_account_selection(self):
        selected_acct = "login__global-login__tenant-select__themistrypenguin__tenant__title"
        acct_url = "https://themistrypenguin.perkbox.com/welcome/login"
        self.input_email(self.registered_user)
        self.scroll_then_click_submit_button(self.continue_btn)
        message = self.show_text("span", "Please select a company you want to sign in to")
        self.assertTrue(message.is_displayed())
        self.driver.find_element_by_id(selected_acct).click()
        self.scroll_then_click_submit_button(self.confirm_btn)
        self.assertEqual(acct_url, self.driver.current_url)
        email = self.driver.find_element_by_xpath(f"//input[@value='{self.registered_user}']")
        self.assertTrue(email.is_displayed())

    def test_registered_user_email_no_account_selection(self):
        self.input_email(self.registered_user)
        self.scroll_then_click_submit_button(self.continue_btn)
        message = self.show_text("span", "Please select a company you want to sign in to")
        self.assertTrue(message.is_displayed())
        self.scroll_then_click_submit_button(self.confirm_btn)
        self.assertEqual(f"{self.login_page}/welcome/login", self.driver.current_url)
        self.assertTrue(message.is_displayed())

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
