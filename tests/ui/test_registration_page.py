import time
from playwright.sync_api import Page, expect
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

    @staticmethod
    def get_user():  # 2 отдельных теста
        pass

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

    @staticmethod
    def get_user():  # 2 отдельных теста
        pass

class TestUI:
    movi_url = "https://dev-cinescope.coconutqa.ru/"
    movies_url = 'https://dev-cinescope.coconutqa.ru/movies'

    def test_movies_page(self, page: Page):
        page.goto(self.movi_url)
        zag_locator = page.locator(".text-4xl")
        expect(zag_locator).to_contain_text('Последние фильмы', timeout=10000)
        expect(zag_locator).to_have_text('Последние фильмы', timeout=10000)
        page.screenshot(path="my_tests.png", full_page=True)

        page.click(".text-3xl[href='/']", timeout=20000)
        page.wait_for_url('https://dev-cinescope.coconutqa.ru/')

        l = page.locator(".rounded-xl.border.bg-card.text-card-foreground.shadow")
        # l = page.locator(".flex.flex-col.space-y-1\.5.p-6")

        p = l.count()
        for i in range(p):
            assert (l.nth(i)).is_visible(), 'не виден'

        loccc = page.locator("xpath=/html/body/div[2]/main/div[1]/div[1]/div[2]/p")
        expect (loccc).to_have_text("Charge identify history study.")

        loc = page.get_by_role("button", name='Подробнее').nth(0)
        loc.click()
        loc2 = loc.locator("xpath=ancestor::a[1]")
        a = loc2.get_attribute('href')
        page.wait_for_url(f'https://dev-cinescope.coconutqa.ru{a}', timeout=2000)
        expect (page.get_by_role('heading', name='Debra Fuller')).to_be_visible()
        expect (page.locator(".mt-10.text-lg")).to_have_text('Charge identify history study.')
        # time.sleep(1)

    @pytest.mark.parametrize('n', [0, 1, 2])
    def test_movie_card_redirect(self, page: Page, n):
        page.goto(self.movies_url)
        param_loc = page.locator(".rounded-xl.border.bg-card.text-card-foreground.shadow").nth(n)
        text_loc = param_loc.locator("h3.text-md")
        param_loc_href = param_loc.locator("a")
        param_loc_button = param_loc.locator("button")

        name_film = text_loc.inner_text()
        loc_href = param_loc_href.get_attribute("href")
        param_loc_button.click()
        page.wait_for_url(f'https://dev-cinescope.coconutqa.ru{loc_href}', timeout=2000)
        assert (page.inner_text(".text-6xl")).strip() == name_film.strip(), "неа"

    def test_movie(self, page: Page):
        page.goto(self.movies_url)
        span_locator = page.locator("button[role='combobox']").filter(has_text="Жанр")
        span_locator.click(timeout=2000)

        data = "open"
        aria = "true"
        assert span_locator.get_attribute('data-state') == data
        assert span_locator.get_attribute('aria-expanded') == aria

        janr_loc = page.locator("span").filter(has_text="Комедия")
        janr_loc.click(timeout=2000)
        # time.sleep(2)

        page.wait_for_url(lambda url: "/movies" in url and "genreId=" in url, timeout=3000)
        a = page.url
        print(a)
        assert "genreId=" in a

        genre_combo = page.locator("button[role='combobox']").nth(1)
        selected = genre_combo.locator("span")
        expect(selected).to_have_text("Комедия")

        j_loc = page.locator(".rounded-xl.border.bg-card.text-card-foreground.shadow")
        count = j_loc.count()
        for i in range(count):
            bot_loc = j_loc.nth(i).locator(".inline-flex.items-center.justify-center")
            bot_loc.click()
            expect (page.locator(".text-lg.mt-5")).to_contain_text("Комедия")
            page.go_back()

        page.click(".inline-flex.items-center[href='/movies?page=2&']")
        page.wait_for_url(lambda url: "page=2" in url, timeout=3000)
        a = page.url
        assert "page=2" in a
        expect(selected).to_have_text("Комедия")
