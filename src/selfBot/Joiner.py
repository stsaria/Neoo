import os
import platform
import random
from urllib.parse import urlparse, parse_qs

import plyvel
import time

from uuid import uuid4

import requests
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc

class Joiner:
    def __init__(self, token:str, inviteId:str, goTime:int):
        self.DRIVER = ".chrome/Driver/chromedriver" + (".exe" if platform.system() == "Windows" else "")
        self.BROWSER_BIN_PATH = ".chrome/App/chrome" + (".exe" if platform.system() == "Windows" else "")
        self.BROWSER_PROFILE_PATH = os.path.abspath(f".chrome/Data/profile-{uuid4()}/")
        self.SELECTORS = {
            "serverAddButton": '[data-list-item-id="guildsnav___create-join-button"]',
            "popupServerJoinButton": '[class="button__6af3a md__6af3a secondary__6af3a hasText__6af3a fullWidth__6af3a"]',
            "inviteIdInput": '[placeholder="https://discord.gg/hTKzmak"]',
            "serverJoinSubmitButton": '[class="button__6af3a md__6af3a primary__6af3a hasText__6af3a"]',
            "recaptchaIframe": "iframe[src*='recaptcha']"
        }

        self._token:str = token
        self._inviteId:str = inviteId
        self._goTime = goTime

        os.makedirs(self.BROWSER_PROFILE_PATH, exist_ok=True)

        options = self._geneOptions()

        self._driver:uc.Chrome = uc.Chrome(options=options)
        self._driver.quit()
        time.sleep(0.5)
        self._writeTokenInfo()
        options = self._geneOptions()
        self._driver = uc.Chrome(options=options, driver_executable_path=self.DRIVER)
        self._driver.set_window_size(500, 500)
    def _geneOptions(self) -> uc.ChromeOptions:
        options = uc.ChromeOptions()
        options.binary_location = self.BROWSER_BIN_PATH
        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-data-dir={self.BROWSER_PROFILE_PATH}")
        options.add_argument("--profile-directory=Default")
        return options
    def _writeTokenInfo(self) -> None:
        db = plyvel.DB(f"{self.BROWSER_PROFILE_PATH}/Default/Local Storage/leveldb", create_if_missing=False)
        db.put(b'_https://discord.com\x00\x01token', b'\x01"'+self._token.encode("utf-8")+b'"')
        db.close()
    def _isJoined(self) -> bool:
        r = requests.get(f"https://discord.com/api/v9/invites/{self._inviteId}")
        if str(r.status_code)[0] != "2": return False
        guildId = r.json()["guild"]["id"]
        r = requests.get(f"https://discord.com/api/v9/guilds/{guildId}", headers={"Authorization": self._token})
        return str(r.status_code)[0] == "2"
    def _clickButton(self, selector:str) -> None:
        while True:
            try:
                self._driver.find_element(By.CSS_SELECTOR, selector).click()
            except:
                continue
            return
    def _inputInput(self, selector:str, value:str) -> None:
        while True:
            try:
                self._driver.find_element(By.CSS_SELECTOR, selector).send_keys(value)
            except:
                continue
            return
    def join(self) -> int:
        r = requests.get(f"https://discord.com/api/v9/invites/{self._inviteId}")
        if str(r.status_code)[0] != "2":
            self._driver.quit()
            return 1
        self._driver.get(f"https://discord.com/app")
        self._clickButton(self.SELECTORS["serverAddButton"])
        self._clickButton(self.SELECTORS["popupServerJoinButton"])
        self._inputInput(self.SELECTORS["inviteIdInput"], self._inviteId)
        while not self._goTime <= int(time.time()):
            pass
        print("aaa")
        self._driver.find_element(By.CSS_SELECTOR, self.SELECTORS["serverJoinSubmitButton"]).click()
        for i in range(100):
            if self._isJoined():
                self._driver.quit()
                return 0
            time.sleep(0.2)
        self._driver.quit()
        return 2

