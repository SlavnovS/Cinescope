import time
from playwright.sync_api import sync_playwright, Page
import allure
import pytest
from models.page_object_models import CinescopRegisterPage, CinescopLoginPage
from utils.data_generator import DataGenerator

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
@pytest.mark.flaky(reruns=2, reruns_delay=2)
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, common_user, page: Page):
        # with sync_playwright() as playwright:
        #     browser = playwright.chromium.launch(
        #         headless=False)  # Запуск браузера headless=False для визуального отображения
        #     page = browser.new_page()
        login_page = CinescopLoginPage(page)  # Создаем объект страницы Login

        login_page.open()
        login_page.check_enabled_home_button()
        login_page.check_enabled_all_movies_button()
        login_page.login(common_user.email, common_user.password)  # Осуществяем вход
        login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
        login_page.assert_allert_was_pop_up("Вы вошли в аккаунт")  # Проверка появления и исчезновения алерта

        # login_page.reload_page()

        login_page.assert_was_redirect_to_home_page()  # Проверка редиректа на домашнюю страницу

        # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
        time.sleep(2)
        # browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page: Page):
        # Подготовка данных для регистрации
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopRegisterPage(page)  # Создаем объект страницы регистрации cinescope
        register_page.open()
        register_page.check_enabled_home_button()
        register_page.check_enabled_all_movies_button()
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                               random_password)  # Выполняем регистрацию

        register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
        register_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
        register_page.assert_allert_was_pop_up()  # Проверка появления и исчезновения алерта
        # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
        time.sleep(2)