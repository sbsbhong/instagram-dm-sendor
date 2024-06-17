from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from instagram.base import InstagramService
from instagram.main import InstagramFeautures

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('start-maximized')
options.add_argument('window-size=1920,1080')

class Instagram(InstagramService):
    def __init__(self, window_options: webdriver.ChromeOptions=options, default_timewait=1):
        user_agent = "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0"

        window_options.add_argument(user_agent)

        context = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=window_options)
        
        super().__init__(context, default_timewait)

    @property
    def main_url(self):
        return self._routes.home
    
    @property
    def name(self):
        return "Instagram"
    
    def login(self, id: str, password: str):
        self._logger.info("Logging in...")
        self._context.get(self._routes.login)
        self._wait_loading()
        self._login(id, password)
        redirected_url = self._wait_redirection(self._routes.login)

        if redirected_url == self._routes.two_factor_auth:
            self._enter_2_factor()

        # 로그인 성공 여부 확인
        if "There was a problem logging you into Instagram" in self._context.page_source:
            self._logger.info("Login failed, please try again later.")
        else:
            self._logger.info("Login successful!")
        
        redirected_url = self._wait_redirection(self._routes.two_factor_auth)

        # 로그인 정보를 저장할거냐 묻는 모달이 뜨면
        if redirected_url == self._routes.account_onetap_modal:
            self._logger.debug("One tap modal is shown")
            # 나중에 하기 버튼 클릭
            notnow_btn = self._context.find_element(By.CLASS_NAME, "_ac8f")
            if notnow_btn:
                notnow_btn.click()
            else: 
                raise Exception("Not now button not found")
            self._logger.debug("Not now button clicked")

        redirected_url = self._wait_redirection(self._routes.account_onetap_modal)

        # 홈으로 리다이렉트 되면 알림을 허용할 것인지 묻는 모달이 뜬다.
        if redirected_url == self._routes.home:
            self._logger.debug("Notification modal is shown")
            notnow_btn = None

            for _ in range(60):
                try:
                    # 알림 허용 버튼 클릭
                    notnow_btn = self._context.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")
                    # 나중에 하기 버튼 클릭
                    notnow_btn.click()

                    break
                except:
                    self.wait_random_time()

            if notnow_btn is None:
                raise Exception("Not now button not found")
            
            self._logger.debug("Not now button clicked")
            
        return InstagramFeautures(self._context, self._timewait)
    
    def _login(self, id: str, password: str):
        self._wait_element('//*[@id="loginForm"]/div/div[1]/div/label/input')
        self.wait_random_time()

        self._context.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(id)
        self._logger.debug("ID entered")
        self.wait_random_time()

        self._context.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        self._logger.debug("Password entered")
        self.wait_random_time()

        self._context.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        self._logger.debug("Login button clicked")
    
    def _enter_2_factor(self):
        self._logger.info("Two factor authentication is required")
        two_factor = input("Enter the two factor code: ")
        # 2 factor 입력
        self._context.find_element(By.XPATH, '//form/div[1]/div/label/input').send_keys(two_factor)
        self._logger.debug("Two factor code entered")
        # 기기 신뢰 체크 박스 해제
        self._context.find_element(By.XPATH, '//form/div[3]/label/div/input').click()
        self._logger.debug("Trust this device checkbox unchecked")
        # 컨펌 버튼 클릭
        self._context.find_element(By.XPATH, '//form/div[2]/button').click()
        self._logger.debug("Confirm button clicked")