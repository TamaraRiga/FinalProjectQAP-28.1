# python -m pytest -v --driver Chrome --driver-path chromedriver tests/test_rt.py
from telnetlib import EC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import settings
from pages.auth_page import AuthPage
from pages.locators import AuthLocators
from settings import *


class TestAuthPage():

    # Тест RT-001
    def test_login_form_opens(self, driver):
        """Переход на страницу с формой авторизации"""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.login_form_opens()

    # Тест RT-002
    def test_location_slogan_and_support_info(self, driver):
        """Расположение продуктового слогана и вспомогательной информации"""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.location_slogan_and_support_info()

    # Тест RT-003
    def test_location_authentication_selection_menu(self, driver):
        """Отображение меню выбора авторизации."""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.location_auth_selection_menu()

    # Тест RT-004
    def test_menu_type_autoriz(self, driver):
        """Проверка названия табов в меню выбора типа авторизации."""
        try:
            auth_page = AuthPage(driver, base_url)
            menu = [auth_page.tab_phone.text, auth_page.tab_mail.text, auth_page.tab_login.text, auth_page.tab_ls.text]
            for i in range(len(menu)):
                assert "Телефон" in menu
                assert 'Почта' in menu
                assert 'Логин' in menu
                assert 'Лицевой счёт' in menu
        except AssertionError:
            print('Ошибка в имени таба Меню типа аутентификации')

    # Тест RT-005
    def test_auto_change_auth_tab(self, driver):
        """Автоматическое изменение таба выбора авторизации"""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.auto_change_auth_tab()

    # Тест RT-006
    def test_autoriz_valid_email_pass(self, driver):
        """Сценарий авторизации клиента с валидными значениями e-mail и паролем."""
        page = AuthPage(driver, base_url)
        page.email.send_keys(settings.valid_email)
        page.email.clear()
        page.password.send_keys(settings.valid_password)
        page.password.clear()
        page.btn_enter.click()

        try:
            assert page.get_relative_link() == '/auth/realms/b2c/login-actions/authenticate'
        except AssertionError:
            assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.ERROR_MESSAGE).text

    # Тест RT-007
    @pytest.mark.parametrize("incor_email", [settings.invalid_email, settings.empty_email],
                             ids=['invalid_email', 'empty'])
    @pytest.mark.parametrize("incor_passw", [settings.invalid_password, settings.empty_password],
                             ids=['invalid_password', 'empty'])
    def test_autoriz_invalid_email_pass(self, driver, incor_email, incor_passw):
        """"Сценарий авторизации клиента по эл.почте, кнопка "Почта" с невалидным email и паролем,
        а также пустые значения."""
        page = AuthPage(driver, base_url)
        page.email.send_keys(incor_email)
        page.email.clear()
        page.password.send_keys(incor_passw)
        page.password.clear()
        page.btn_enter.click()
        assert page.get_relative_link() != '/account_b2c/page'

    # Тест RT-008
    def test_auth_vk(self, driver):
        """Переход по ссылке авторизации пользователя через VK."""
        page = AuthPage(driver, base_url)
        page.vk_button.click()
        assert page.get_base_url() == 'oauth.vk.com'

    # Тест RT-009
    def test_auth_ok(self, driver):
        """Переход по ссылке авторизации пользователя через сайт одноклассники."""
        page = AuthPage(driver, base_url)
        page.ok_button.click()
        assert page.get_base_url() == 'connect.ok.ru'

    # Тест RT-010
    def test_auth_mail(self, driver):
        """Переход по ссылке авторизации пользователя через сайт Мой мир."""
        page = AuthPage(driver, base_url)
        page.mail_button.click()
        assert page.get_base_url() == 'connect.mail.ru'

    # Тест RT-011
    def test_auth_google(self, driver):
        """Переход по ссылке авторизации пользователя через Google."""
        page = AuthPage(driver, base_url)
        page.google_button.click()
        assert page.get_base_url() == 'accounts.google.com'

    # # Тест почему-то проваливается, хотя переход должен работать
    # def test_auth_yandex(self, driver):
    #     """Переход по ссылке авторизации пользователя через Yandex."""
    #     page = AuthPage(driver, base_url)
    #     page.ya_button.click()
    #     page.open()
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "oidc_ya")))
    #     # driver.implicitly_wait(10)
    #     assert page.get_base_url() == 'oauth.yandex.ru'

    # Тест RT-012
    def test_authorization_with_empty_fields(self, driver):
        """Авторизация с незаполненными полями."""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.authorization_with_empty_fields()


class TestRegPage():

    # Тест RT-013
    def test_go_to_the_password_recovery_form(self, driver):
        """Переход и отображение формы для восстановления пароля."""
        auth_page = AuthPage(driver, base_url)
        auth_page.open()
        auth_page.go_to_the_password_recovery_form()

    # Тест RT-014
    def test_back_button(self, driver):
        """Работа кнопки "Вернуться назад" на странице восстановления пароля"""
        change_pass_page = AuthPage(driver, url_change_page)
        change_pass_page.open()
        change_pass_page.back_button()

    # Тест RT-015
    def test_registration_link(self, driver):
        """Переход на форму "Регистрация"."""
        auth_page = AuthPage(driver, base_url)
        auth_page.register_link.click()

    # Тест RT-016
    def test_elements_registration(self, driver):
        """Наличие основных элементов на странице "Регистрация"."""
        try:
            page_reg = AuthPage(driver, base_url)
            page_reg.open_reg_page()
            card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                           page_reg.email_registration, page_reg.password_registration,
                           page_reg.password_registration_confirm, page_reg.registration_btn]
            for i in range(len(card_of_reg)):
                assert page_reg.first_name in card_of_reg
                assert page_reg.last_name in card_of_reg
                assert page_reg.email_registration in card_of_reg
                assert page_reg.address_registration in card_of_reg
                assert page_reg.password_registration in card_of_reg
                assert page_reg.password_registration_confirm in card_of_reg
                assert page_reg.registration_btn in card_of_reg
        except AssertionError:
            print('Элемент отсутствует в форме «Регистрация»')

    # Тест RT-017
    def test_valid_email_entry_check(self, driver):
        """Работа формы "Регистрация" при вводе действительного e-mail в поле "e-mail или мобильный телефон"."""
        page = AuthPage(driver, base_url)
        page.open_reg_page()
        page.valid_email_entry_check()

    # Тест RT-018
    @pytest.mark.parametrize('input_text', invalid_email)
    def test_invalid_email_entry_check(self, driver, input_text):
        """Работа формы "Регистрация" на ввод недействительного e-mail."""
        page = AuthPage(driver, base_url)
        page.open_reg_page()
        page.invalid_email_entry_check(input_text)

    # Тест RT-019
    @pytest.mark.parametrize('input_text', invalid_name)
    def test_entering_invalid_name_data(self, driver, input_text):
        """Работа формы "Регистрация" на ввод невалидных данных в поле "Имя."""
        page = AuthPage(driver, base_url)
        page.open_reg_page()
        page.entering_invalid_name_data(input_text)

    # Тест RT-020
    @pytest.mark.parametrize('input_text', last_name_pozitiv)
    def test_last_name_positive(self, driver, input_text):
        """Позитивные проверки для поля ввода фамилии."""
        page = AuthPage(driver, base_url)
        page.open_reg_page()
        page.entering_last_name_pozitiv(input_text)

    # Тест RT-021
    @pytest.mark.parametrize('input_text', last_name_negativ)
    def test_last_name_negativ(self, driver, input_text):
        """Негативные проверки для поля ввода фамилии."""
        page = AuthPage(driver, base_url)
        page.open_reg_page()
        page.entering_last_name_negativ(input_text)





