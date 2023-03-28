import os
from .base_page import BasePage
from .locators import AuthLocators
from settings import valid_email


class AuthPage(BasePage):

    def __init__(self, driver, timeout=5):
        super().__init__(driver, timeout)
        url = os.getenv('MAIN_URL') or 'https://b2c.passport.rt.ru'
        driver.get(url)
        driver.maximize_window()

        # создаем нужные элементы:
        self.page_right = driver.find_element(*AuthLocators.PAGE_RIGHT)
        self.page_left = driver.find_element(*AuthLocators.PAGE_LEFT)
        self.tab_phone = driver.find_element(*AuthLocators.TAB_PHONE)
        self.tab_mail = driver.find_element(*AuthLocators.TAB_MAIL)
        self.tab_login = driver.find_element(*AuthLocators.TAB_LOGIN)
        self.tab_ls = driver.find_element(*AuthLocators.TUB_LS)
        self.email = driver.find_element(*AuthLocators.AUTH_MAIL)
        self.login = driver.find_element(*AuthLocators.AUTH_LOGIN)
        self.password = driver.find_element(*AuthLocators.AUTH_PASS)
        self.btn_enter = driver.find_element(*AuthLocators.AUTH_BTN_ENTER)
        self.register_link = driver.find_element(*AuthLocators.AUTH_REGISTER_LINK)
        self.forgot_password_link = driver.find_element(*AuthLocators.FORGOT_PASS_LINK)
        self.placeholder_name = driver.find_element(*AuthLocators.PLACEHOLDER_NAME)
        self.placeholder_mail = driver.find_element(*AuthLocators.PLACEHOLDER_MAIL)
        self.active_tab_phone = driver.find_element(*AuthLocators.ACTIVE_TAB_PHONE)
        self.card_of_auth = driver.find_element(*AuthLocators.CARD_OF_AUTH)
        self.menu_tab = driver.find_element(*AuthLocators.MENU_TAB)
        self.vk_button = driver.find_element(*AuthLocators.VK_BUTTON)
        self.ok_button = driver.find_element(*AuthLocators.OK_BUTTON)
        self.mail_button = driver.find_element(*AuthLocators.MAIL_BUTTON)
        self.google_button = driver.find_element(*AuthLocators.GOOGLE_BUTTON)
        self.ya_button = driver.find_element(*AuthLocators.YA_BUTTON)

    # для проверки перехода на форму авторизации
    def login_form_opens(self):
        assert self.is_element_present(AuthLocators.AUTH_HEADING)
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth" in self.driver.current_url, \
            "url do not match"

    # для проверки расположения логотипа и слогана
    def location_slogan_and_support_info(self):
        assert self.is_element_present(AuthLocators.AUTH_LOGO), "element not found"
        assert self.is_element_present(AuthLocators.AUTH_SLOGAN), "element not found"

    # для проверки расположения меню выбора типа авторизации
    def location_auth_selection_menu(self):
        assert self.is_element_present(AuthLocators.AUTH_TAB_MENU), "element not found"

    # для проверки автоматического изменения типа авторизации
    def auto_change_auth_tab(self):
        self.find_element(AuthLocators.AUTH_USERNAME_INPUT).send_keys(valid_email)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.AUTH_USERNAME_INPUT_EMAIL), "element not found"

    # для проверки авторизации с пустыми полями
    def authorization_with_empty_fields(self):
        self.find_element(AuthLocators.TAB_PHONE).click()
        self.find_element(AuthLocators.AUTH_BTN_ENTER).click()
        assert self.is_element_present(AuthLocators.AUTH_ERROR_ENTER_PHONE_NUMBER), "element not found"
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth" in self.driver.current_url, \
            "url do not match"

    # для проверки ссылки перехода на форму восстановления пароля
    def go_to_the_password_recovery_form(self):
        self.find_element(AuthLocators.FORGOT_PASSWORD_LINK).click()
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials" \
               in self.driver.current_url, "url do not match"
        assert self.is_element_present(AuthLocators.CHANGE_PASSWORD), "element not found"

    # для проверки на странице формы "Восстановление пароля" кнопки "Вернуться назад"
    def back_button(self):
        self.find_element(AuthLocators.PASSWORD_GO_BACK_BUTTON).click()
        assert self.is_element_present(AuthLocators.AUTH_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate" in self.driver.current_url, \
            "url do not match"

    # Проверка формы "Регистрация" на ввод действительного e-mail
    def valid_email_entry_check(self):
        self.find_element(AuthLocators.MAIL_REGISTRATION).send_keys(valid_email)
        self.find_element(AuthLocators.BODY).click()
        element = self.find_element(AuthLocators.MAIL_REGISTRATION_VALUE)
        value = element.get_attribute("value")
        assert valid_email == value, "email do not match"

    # Проверка формы "Регистрация" на ввод недействительного e-mail
    def invalid_email_entry_check(self, input_text):
        self.find_element(AuthLocators.MAIL_REGISTRATION).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.REG_ERROR_INVALID_MAIL_PHONE_INPUT), "element not found"

    # Проверка формы "Регистрация" на ввод недействительных данных в поле "Имя"
    def entering_invalid_name_data(self, input_text):
        self.find_element(AuthLocators.REG_FIRST_NAME_INPUT).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.REG_ERROR_FIRST_NAME_INPUT), "element not found"

    # Позитивная проверка формы "Регистрация" на ввод данных в поле "Фамилия"
    def entering_last_name_pozitiv(self, input_text):
        self.find_element(AuthLocators.REG_LAST_NAME_INPUT).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.LAST_NAME_FIELD), "element not found"

    # Негативная проверка формы "Регистрация" на ввод данных в поле "Фамилия"
    def entering_last_name_negativ(self, input_text):
        self.find_element(AuthLocators.REG_LAST_NAME_INPUT).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def find_YA_element(self):
        assert self.is_element_present(AuthLocators.YA_ENTER), "element not found"

    def find_other_element(self, by, location):
        return self.driver.find_element(by, location)

    def first_name(self, input_text):
        self.find_element(AuthLocators.FIRST_NAME).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def last_name(self, input_text):
        self.find_element(AuthLocators.LAST_NAME).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def last_name_field(self, input_text):
        self.find_element(AuthLocators.LAST_NAME_FIELD).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def address_registration(self, input_text):
        self.find_element(AuthLocators.REGION_REGISTRATION).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def email_registration(self, input_text):
        self.find_element(AuthLocators.MAIL_REGISTRATION).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def password_registration(self, input_text):
        self.find_element(AuthLocators.PASSWORD_REGISTRATION).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def password_registration_confirm(self, input_text):
        self.find_element(AuthLocators.PASSWORD_CONFIRM).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"

    def registration_btn(self, input_text):
        self.find_element(AuthLocators.REG_BTN).send_keys(input_text)
        self.find_element(AuthLocators.BODY).click()
        assert self.is_element_present(AuthLocators.WARNING_MESSAGE) != '', "element not found"




    # def enter_phone(self, value):
    #     self.tab_phone.click()
    #     self.login.send_keys(value)
    #
    # def enter_mail(self, value):
    #     self.tab_mail.click()
    #     self.login.send_keys(value)
    #
    # def enter_pass(self, value):
    #     self.password.send_keys(value)
    #
    # def btn_click(self):
    #     self.btn_enter.click()
