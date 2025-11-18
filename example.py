from playwright.sync_api import sync_playwright, Page, expect
import time
import pytest
from random import randint
from pathlib import Path
from datetime import datetime

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

DEFAULT_UI_TIMEOUT = 30000  # Пример значения таймаута

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)  # Установка таймаута по умолчанию
    yield context  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()  # Контекст закрывается после завершения теста

@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context) -> Page:
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста


class Tools:
    @staticmethod
    def project_dir():
        """ Возвращает корневую директорию проекта.
        Предполагается, что текущий файл находится в поддиректории `common`. """
        return Path(__file__).parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """ Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу. """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        """ Возвращает текущую временную метку в формате YYYY-MM-DD_HH-MM-SS. """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def test_text_box(page: Page):
    page.pause()
    page.goto('https://demoqa.com/text-box')

    # вариант №2
    page.locator('#userName').fill('testQa')
    page.fill('#userEmail', 'test@qa.com')
    page.type('#currentAddress', 'Phuket, Thalang 99', delay=200)

    page.fill('#permanentAddress', 'Moscow, Mashkova 1')

    page.click('button#submit')

    expect(page.locator('#output #name')).to_have_text('Name:testQa')
    expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Moscow, Mashkova 1')


    time.sleep(10)

def test_cinescope_registration(page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    user_email = f'test_{randint(1, 9999)}@email.qa'

    page.fill("[name='fullName']", 'Жмышенко Валерий Альбертович')
    page.fill("[name='email']", user_email)
    page.type("[name='password']", 'qwerty123Q', delay=100)
    page.type("[name='passwordRepeat']", 'qwerty123Q', delay=100)

    # page.get_by_role("button", name="Зарегистрироваться").click()

    # page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    # expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True, timeout=5000)
    time.sleep(5)

@pytest.mark.flaky(reruns=2, reruns_delay=5)
def test_web_tables(page):
    # page.pause()
    page.goto('https://demoqa.com/webtables', timeout=40000)

    page.get_by_role("button", name = "add").click()
    expect(page.locator('[class="modal-content"]')).to_be_visible()
    expect(page.get_by_text('Registration Form')).to_be_visible()
    expect(page.locator('[class="modal-body"]')).to_be_visible()

    page.fill('#firstName', 'Sanek')
    page.get_by_placeholder('last name').fill('Sanechek')
    page.fill('#userEmail', 'SanekSanechek@mail.com')
    page.get_by_placeholder('age').type('29', delay=200)
    page.type('#salary', '0')
    page.type('#department-wrapper [class="col-md-6 col-sm-6"] #department', '12')

    page.click('#submit')

    table = page.locator('.web-tables-wrapper')
    expect(table).to_contain_text('Sanek')
    expect(table).to_contain_text("Sanechek")
    expect(table).to_contain_text("SanekSanechek@mail.com")
    expect(table).to_contain_text("29")
    expect(table).to_contain_text("0")

def test_tools(page):
    page.goto('https://demoqa.com/checkbox', referer='https://google.com')

    page.get_by_role("button", name="Toggle").click(timeout=3000)
    page.get_by_role("button", name="Toggle").nth(2).click(timeout=3000)
    page.get_by_role("button", name="Toggle").nth(4).click(timeout=3000)

    page.locator('.rct-checkbox').nth(6).click()
    page.locator('.rct-checkbox').nth(7).click()

    expect(page.locator(".rct-icon.rct-icon-check").nth(0)).to_be_visible()
    expect(page.locator(".rct-icon.rct-icon-check").nth(1)).to_be_visible()
    expect(page.locator('#result')).to_contain_text("privateclassified")

    time.sleep(2)

    page.goto('https://demoqa.com/radio-button', referer='https://google.com')

    page.locator('label', has_text="Impressive").click()

    expect(page.locator('.mt-3')).to_contain_text("Impressive")

    time.sleep(2)

def test_active(page):
    page.goto('https://demoqa.com/radio-button')
    print('')
    print(f"Кнопка Yes активна?: {(page.locator('label', has_text='yes')).is_enabled()}")
    print(f"Кнопка Impressive активна?: {(page.locator('label', has_text='impressive')).is_enabled()}")
    print(f"Кнопка No не активна?: {not (page.locator('label', has_text='no')).is_enabled()}")
    expect(page.locator('label', has_text='yes')).to_be_enabled()
    expect(page.locator('label', has_text='impressive')).to_be_enabled()
    expect(page.locator('label', has_text='no')).not_to_be_enabled()

    page.locator('label', has_text="Impressive").click()
    expect(page.locator('label', has_text="Impressive")).to_be_checked()  # проверяем, что отмечен


    page.goto('https://demoqa.com/checkbox')
    print(f"Раздел Home виден?: {(page.locator('.rct-text').nth(0)).is_visible()}")
    print(f"Раздел Desktop не виден?: {not (page.locator('.rct-text').nth(1)).is_visible()}")
    page.get_by_role('button', name="Toggle").click()
    print(f"Раздел Desktop виден?: {(page.locator('.rct-text').nth(1)).is_visible()}")

    print(f"Раздел WorkSpace не виден?: {not (page.locator('.rct-text').nth(4)).is_visible()}")
    page.get_by_role("button", name="Toggle").nth(2).click(timeout=3000)
    print(f"Раздел WorkSpace виден?: {(page.locator('.rct-text').nth(4)).is_visible()}")

    page.goto('https://demoqa.com/dynamic-properties')
    a = time.time()
    print(f"Элемент не виден?: {not page.is_visible('#visibleAfter')}")
    print(f"Элемент не активен?: {not page.is_enabled('#enableAfter')}")
    page.wait_for_selector('#visibleAfter', timeout=10000)
    b = time.time()
    print(f"Элемент виден?: {page.is_visible('#visibleAfter')}")
    print(b - a)
    print(f"Элемент активен?: {page.is_enabled('#enableAfter')}")