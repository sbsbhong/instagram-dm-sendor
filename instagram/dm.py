from typing import Self, Union, List
from instagram.base import InstagramService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class DMRoom:
    def __init__(self, url: str, element: WebElement) -> None:
        self.url = url
        self._context = element
    
    @property
    def textbox(self) -> Union[WebElement, None]:
        try:
            node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]'

            return self._context.find_element(By.XPATH, node)
        except:
            return None
        
    @property
    def file_attach_input(self) -> Union[WebElement, None]:
        try:
            node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/input'

            if self.is_like_btn_exist:
                node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/input'

            return self._context.find_element(By.XPATH, node)
        except:
            return None

    @property
    def send_message_button(self) -> Union[WebElement, None]:
        try:
            node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]'

            if self.is_like_btn_exist:
                node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]'
            
            return self._context.find_element(By.XPATH, node)
        except:
            return None
    
    @property
    def send_files_button(self) -> Union[WebElement, None]:
        try:
            node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div[2]/div[3]'
            if self.is_like_btn_exist:
                #node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]'
                node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]'
                #node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]'
                #node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]'
                #node = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]

            return self._context.find_element(By.XPATH, node)
        except:
            try:
                return self._context.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[3]')
            except:
                pass
            return None
        
    @property
    def like_button(self) -> Union[WebElement, None]:
        try:
            return self._context.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[3]')
        except:
            return None
        
    @property
    def is_like_btn_exist(self) -> bool:
        return self.like_button is not None


class InstagramDM(InstagramService):
    _room: Union[DMRoom, None] = None

    def __init__(self, context, default_timewait=1):
        super().__init__(context, default_timewait)

    @property
    def main_url(self):
        return self._routes.dm
    
    @property
    def name(self):
        return "Direct Message"
    
    @property
    def room(self):
        return self._room
    
    def new_message(self, recipient_id: str) -> Self:
        """ if self._context.current_url != self.main_url:
            self.open() """

        self._wait_element('/html/body/div[2]')
        new_message_btn = self.find_element(self._context, By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div')
        if new_message_btn:
            new_message_btn.click()
            self._logger.debug("New message button clicked")
        else:
            raise Exception("New message button not found")
        
        self._wait_element("//input[@name='queryBox']")
        
        recipient_input = self.find_element(self._context, By.XPATH, "//input[@name='queryBox']")
        recipient_input.send_keys(recipient_id)
        self._logger.debug("Recipient id entered")
        
        self._wait_element('/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div')

        searched_users = self.find_elements(self._context, By.CSS_SELECTOR, 'body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div.x9f619.x1ja2u2z.x1k90msu.x6o7n8i.x1qfuztq.x10l6tqk.x17qophe.x13vifvy.x1hc1fzr.x71s49j.xh8yej3 > div > div.xjp7ctv > div > div > div')

        self._logger.info("Searched users:" + str(len(searched_users)))
        if not searched_users:
            self._logger.error("No searched users found")

            return self
        
        is_found = False
        
        for searched_user in searched_users:
            id = self.find_element(searched_user, By.CSS_SELECTOR, 'div:nth-child(1) > div > div > div:nth-child(2) > div > div > span > span')
            if id and id.text == recipient_id:
                self._logger.info("Recipient found")
                is_found = True
                self.wait_random_time()
                id.click()
                break
            
        if not is_found:
            self._logger.error("Recipient not found")
            return self
        
        chat_btn = self.find_element(self._context, By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div')

        if chat_btn:
            self.wait_random_time()
            chat_btn.click()
            self._logger.debug("Chat button clicked")
        else:
            raise Exception("Chat button not found")
        
        dm_room_url = self._wait_redirection(self._routes.dm)

        if not dm_room_url:
            raise Exception("DM room did not create.")
        
        self._wait_element('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]')
        dm_room_elem = self.find_element(self._context, By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]')

        if not dm_room_elem:
            raise Exception("DM room did not create.")
        
        self._room = DMRoom(dm_room_url, dm_room_elem)
        self._logger.info("DM room created")
        
        return self
        
    
    def send_messsage(self, message: str) -> Self:
        if not self.room:
            raise Exception("DM room not found. Create a new message first.")
        
        if not self.room.textbox:
            raise Exception("Text box not found")
        
        self.room.textbox.send_keys(message)

        self.wait_random_time()
        self.room.textbox.send_keys(Keys.ENTER)

        """ self._wait_random_time()
        if not self.room.send_message_button:
            raise Exception("Send button not found")
        
        self._wait_random_time()
        self.room.send_message_button.click() """

        self._logger.info("Message sent")

        return self

        
    def send_files(self, files: List[str]) -> Self:
        if not self.room:
            raise Exception("DM room not found. Create a new message first.")
        
        if not self.room.file_attach_input or not self.room.textbox:
            raise Exception("File attach input not found")
        
        self.room.file_attach_input.send_keys("\n".join(files))

        self.wait_random_time()
        if not self.room.send_files_button:
            raise Exception("Send button not found")
        
        self.wait_random_time()
        self.room.send_files_button.click()

        self._logger.info("Files sent")

        return self
    
    def close_room(self):
        self._room = None
        self._logger.info("DM room closed")
        
        return self
