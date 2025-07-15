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

DRIVER = ".chrome/Driver/chromedriver" + (".exe" if platform.system() == "Windows" else "")
BROWSER_BIN_PATH = ".chrome/App/chrome" + (".exe" if platform.system() == "Windows" else "")
BROWSER_PROFILE_PATH = os.path.abspath(f".chrome/Data/profile-{uuid4()}/")
SELECTORS = {
    "serverAddButton": "div.listItemWrapper__91816:nth-child(1) > div:nth-child(1) > svg:nth-child(1) > foreignObject:nth-child(3) > div:nth-child(1)",
    "popupServerJoinButton": ".md__6af3a",
    "inviteIdInput": ".inputDefault__0f084",
    "serverJoinSubmitButton": "#app-mount > div.appAsidePanelWrapper_a3002d > div.notAppAsidePanel_a3002d > div:nth-child(4) > div.layer_bc663c > div > div > div > div > div > div > div > div.flex__7c0ba.horizontalReverse__7c0ba.justifyStart_abf706.alignStretch_abf706.noWrap_abf706.footer__49fc1.footer__991a0.footerSeparator__49fc1 > button.button__6af3a.md__6af3a.primary__6af3a.hasText__6af3a",
    "recaptchaIframe": "iframe[src*='recaptcha']"
}

class Joiner:
    def __init__(self, token:str, inviteId:str, goTime:int):
        self._token:str = token
        self._inviteId:str = inviteId
        self._goTime = goTime

        os.makedirs(BROWSER_PROFILE_PATH, exist_ok=True)

        options = self._geneOptions()

        self._driver:uc.Chrome = uc.Chrome(options=options)
        self._driver.quit()
        time.sleep(0.5)
        self._writeTokenInfo()
        options = self._geneOptions()
        self._driver = uc.Chrome(options=options, driver_executable_path=DRIVER)
        self._driver.set_window_size(500, 500)
    def _geneOptions(self) -> uc.ChromeOptions:
        options = uc.ChromeOptions()
        options.binary_location = BROWSER_BIN_PATH
        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-data-dir={BROWSER_PROFILE_PATH}")
        options.add_argument("--profile-directory=Default")
        return options
    def _writeTokenInfo(self) -> None:
        db = plyvel.DB(f"{BROWSER_PROFILE_PATH}/Default/Local Storage/leveldb", create_if_missing=False)
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
        self._clickButton(SELECTORS["serverAddButton"])
        self._clickButton(SELECTORS["popupServerJoinButton"])
        self._inputInput(SELECTORS["inviteIdInput"], self._inviteId)
        while not self._goTime >= int(time.time()):
            pass
        self._driver.find_element(By.CSS_SELECTOR, SELECTORS["serverJoinSubmitButton"]).click()
        for i in range(100):
            if self._isJoined():
                self._driver.quit()
                return 0
            time.sleep(0.2)
        self._driver.quit()
        return 2

