from datetime import datetime
from enum import Enum

class LogType(Enum):
    SUCCESS = 1
    WARNING = 2
    FAILED = 3
    OTHER = 4

class Log:
    def __init__(self, logType:LogType, message:str | None):
        self._logType:LogType = logType
        self._message:str | None = message
        self._dateTime:datetime = datetime.now()
    def getLogType(self) -> LogType:
        return self._logType
    def getMessage(self) -> str | None:
        return self._message
    def getDateTime(self) -> datetime:
        return self._dateTime