from selenium.webdriver.remote.webelement import WebElement
from selenium.common import StaleElementReferenceException, NoSuchFrameException
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage

class ProductPage(BasePage):
    PHONES_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[6]/a")
    CAMERAS_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[7]/a")
    TABLETS_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[4]/a")
    WISHLIST_ON_PRODUCT_PAGE_BUTTON = (By.XPATH, "//*[@id=\"content\"]/div[1]/div[2]/form/div/button[1]")
    PRODUCT_NAME = (By.XPATH, "//*[@id=\"content\"]/div[2]/div/div/div[1]/a/img")
    OPTIONAL_SUBMENU = (By.XPATH, "//*[@id=\"input-option-226\"]")
    RED_COLOR = (By.XPATH, "//*[@id=\"input-option-226\"]/option[2]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//*[@id=\"button-cart\"]")
    REVIEWS_BUTTON = (By.XPATH, "//*[@id=\"content\"]/ul/li[3]/a")
    CONTINUE_REVIEW_BUTTON = (By.XPATH, "//*[@id=\"button-review\"]")
    REVIEW_NAME_FIELD = (By.XPATH, "//*[@id=\"input-name\"]")
    REVIEW_TEXT = (By.XPATH, "//*[@id=\"input-text\"]")
    REVIEW_RATING = (By.XPATH, "//*[@id=\"input-rating\"]")
    LOGIN_ALERT = (By.XPATH, "//*[@id=\"alert\"]/div")
    CART_ALERT = (By.XPATH, "//*[@id=\"alert\"]/div")

    def __init__(self, driver):
        super().__init__(driver)

    def open_main_page(self):
        self.driver.get(self.BASE_URL)

    def click_product_name(self, product_index, frame_locator=None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass

                products = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(self.PRODUCT_NAME))
                element = products[product_index]
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))

                try:
                    element.click()
                    return
                except StaleElementReferenceException as e:
                    print(f"StaleElementReferenceException при клике (попытка {attempt + 1}): {e}")
                    pass

            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                pass
            finally:
                try:
                    self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")

        print(f"Не удалось кликнуть на элемент с индексом {product_index} после {max_attempts} попыток")

    def find_and_click_element(self, locator: tuple[str, str], frame_locator: tuple[str, str] = None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass

                element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator))

                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))

                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except StaleElementReferenceException as e:
                    print(f"StaleElementReferenceException при клике (попытка {attempt + 1}): {e}")
                    pass

            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                pass
            finally:
                try:
                    if frame_locator:
                        self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")

        print(f"Не удалось кликнуть на элемент после {max_attempts} попыток с локатором {locator}")

    def open_phones_page(self):
        self.driver.find_element(*self.PHONES_PAGE_LINK).click()

    def open_cameras_page(self):
        self.driver.find_element(*self.CAMERAS_PAGE_LINK).click()

    def open_optional_options(self):
        self.driver.find_element(*self.OPTIONAL_SUBMENU).click()

    def open_tablets_page(self):
        self.driver.find_element(*self.TABLETS_PAGE_LINK).click()

    def select_red_color(self):
        self.driver.find_element(*self.RED_COLOR).click()

    def is_login_alert_displayed(self):
        try:
            self.driver.find_element(*self.LOGIN_ALERT).is_displayed()
            return True
        except:
            return False

    def is_cart_alert_displayed(self):
        try:
            self.driver.find_element(*self.CART_ALERT).is_displayed()
            return True
        except:
            return False

    def is_this_cart_alert(self, expected):
        actual = self.driver.find_element(*self.CART_ALERT).get_attribute("textContent")

        if actual == expected:
            return True
        else:
            print("Текст уведомления не совпадает")
            return False

    def write_a_review(self, name, review_text):
        self.find_and_click_element(self.REVIEW_NAME_FIELD)
        name_field = self.driver.find_element(*self.REVIEW_NAME_FIELD)
        name_field.clear()
        name_field.send_keys(name)
        self.find_and_click_element(self.REVIEW_TEXT)
        text_field = self.driver.find_element(*self.REVIEW_TEXT)
        text_field.clear()
        text_field.send_keys(review_text)

    def rate_the_product(self, rating):
        buttons = self.driver.find_elements(*self.REVIEW_RATING)

        for button in buttons:
            if button.get_attribute("value") == str(rating):
                button.click()
                return
        print(f"Кнопка с рейтингом {rating} не найдена")

    def get_actual_reviewer_name(self):
        return self.driver.find_element(*self.REVIEW_NAME_FIELD).get_attribute("value")

    def get_actual_review_text(self):
        return self.driver.find_element(*self.REVIEW_TEXT).get_attribute("value")