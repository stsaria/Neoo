import os
import platform
import shutil

import requests


class ChromeSetuper:
    @staticmethod
    def setup() -> None:
        osArch = ""

        os.makedirs(".tmp/", exist_ok=True)
        os.makedirs(".chrome/", exist_ok=True)
        os.makedirs(".chrome/Data", exist_ok=True)

        match platform.system():
            case "Linux":
                osArch = "linux64"
            case "Darwin":
                osArch = "mac-"
                osArch += {
                    "amd64": "x64",
                    "x86_64": "x64",
                    "arm64": "arm64",
                    "aarch64": "arm64"
                }.get(platform.machine().lower(), "")
            case "Windows":
                osArch = "win64"
        r = requests.get("https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
        version = r.json()["channels"]["Stable"]["version"]
        r = requests.get(f"https://storage.googleapis.com/chrome-for-testing-public/{version}/{osArch}/chrome-{osArch}.zip")
        with open(".tmp/chrome.zip", mode="wb") as f:
            f.write(r.content)
        shutil.unpack_archive(".tmp/chrome.zip", ".tmp/chrome/")
        shutil.copytree(f".tmp/chrome/chrome-{osArch}", ".chrome/App/", dirs_exist_ok=True)

        r = requests.get(f"https://storage.googleapis.com/chrome-for-testing-public/{version}/{osArch}/chromedriver-{osArch}.zip")
        with open(".tmp/chromedriver.zip", mode="wb") as f:
            f.write(r.content)
        shutil.unpack_archive(".tmp/chromedriver.zip", ".tmp/chromedriver/")
        shutil.copytree(f".tmp/chromedriver/chromedriver-{osArch}", ".chrome/Driver", dirs_exist_ok=True)

        shutil.rmtree(".tmp/")