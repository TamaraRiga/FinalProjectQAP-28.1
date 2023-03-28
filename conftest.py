import pytest
from selenium import webdriver
import time
from datetime import datetime



@pytest.fixture(scope="function")
def driver():
    print("\nstart driver for test..")
    driver = webdriver.Chrome('chromedriver')
    driver.maximize_window()

    yield driver

    print("\nquit driver..")
    driver.quit()


# Для скриншота провалившегося теста напишем перехватчик, который определит - провален тест или нет
@pytest.hookimpl(tryfirst=True, hookwrapper=True)  # tryfirst определяет то, что необх.перхватывать
def pytest_runtest_makereport(item, call):   # ф-ция, кот.будет вести репорт о том, какие у нас состояния, и как они называются
    outcome = yield   # будем перхватывать все yield
    rep = outcome.get_result()  # получаем результат: упал или нет
    setattr(item, "rep_" + rep.when, rep)   # определяем атрибут, кот.будет определять, что с нами стало


# ф-ция, кот.будет обрабатывать падение
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    if request.node.rep_setup.failed:
        print("test is failed", request.node.nodeid)
    elif request.node.rep_setup.passed:   # м.б. что тест прошел, но провалился
        if request.node.rep_call.failed:  # если он упал, его все равно нужно засчитать
            driver = request.node.funcargs["driver"]  # ф-ция, кот. передаст, что падение на уровне driver
            save_screenshot(driver, request.node.nodeid)
            print("executing is failed", request.node.nodeid)


def save_screenshot(driver, nodeid):  # ф-ция, кот. делает скриншот
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M:%S")}.png'.replace('/', '_').replace('::', '__')
    driver.save_screenshot(file_name)



