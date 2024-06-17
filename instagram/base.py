import time, random
from abc import ABCMeta, abstractmethod
from typing import Union, Self
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from instagram.routes import IntagramRoutes
from instagram.log import get_logger

class InstagramService(metaclass=ABCMeta):
    _MAXIMUM_WAIT_LOOPS = 30
    _routes = IntagramRoutes()

    def __init__(self, context: Chrome, default_timewait: int=1) -> None:
        self._context = context
        self._timewait = default_timewait

        self._logger = get_logger()

        self._logger.debug(f"{self.name} service object created")

    @property
    @abstractmethod
    def main_url(self) -> str:
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def _wait_loading(self):
        for _ in range(10):
            if self._context.execute_script("return document.readyState") == "complete":
                break
            self.wait_random_time()
    
    def _wait_element(self, value="", by: str=None, element: WebElement=None, ) -> None:
        if not element:
            element = self._context

        if not by:
            by = By.XPATH

        WebDriverWait(element, self._timewait).until(
            EC.presence_of_element_located((by, value))
        )

        self.wait_random_time()

    def _wait_redirection(self, origin_url: str) -> Union[None, str]:
        for _ in range(self._MAXIMUM_WAIT_LOOPS):
            if self._context.current_url != origin_url:
                return self._context.current_url
            self.wait()
        
        raise Exception(f"Redirection failed. Origin url: {origin_url}")

    def wait(self):
        time.sleep(self._timewait)

    def wait_random_time(self):
        time.sleep(self._timewait * (1 + random.random()))
    
    def open(self) -> Self:
        previous = self._context.current_url
        self._context.get(self.main_url)
        self._wait_redirection(previous)
        self._logger.debug(f"{self.name} service is ready")
        return self
    
    def close(self) -> None:
        self._context.quit()

    def find_element(self, element: WebElement, by: str, value: str) -> Union[WebElement, None]:
        try:
            return element.find_element(by, value)
        except:
            self._logger.error(f"Element not found: {by}, {value}")
            return None 
        
    def find_elements(self, element: WebElement, by: str, value: str) -> Union[WebElement, None]:
        try:
            return element.find_elements(by, value)
        except:
            self._logger.error(f"Element not found: {by}, {value}")
            return None
