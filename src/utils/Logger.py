from threading import Lock
from src.utils.Log import Log, LogType


class Logger:
    _logs:list[Log] = []
    _lock:Lock = Lock()
    def other(self, msg:str) -> None:
        with self._lock:
            self._logs.append(Log(LogType.OTHER, msg))
    def success(self, msg:str | None = None) -> None:
        with self._lock:
            self._logs.append(Log(LogType.SUCCESS, msg))
    def warning(self, msg:str | None = None) -> None:
        with self._lock:
            self._logs.append(Log(LogType.WARNING, msg))
    def failed(self, msg:str | None = None) -> None:
        with self._lock:
            self._logs.append(Log(LogType.FAILED, msg))
    def toStr(self) -> str:
        s = ""
        with self._lock:
            for log in self._logs:
                match log.getLogType():
                    case LogType.SUCCESS:
                        s += "[+]Success"
                    case LogType.WARNING:
                        s += "[~]Warning"
                    case LogType.FAILED:
                        s += "[!]Failed"
                    case LogType.SUCCESS:
                        s += "[?]Other"
                msg = log.getMessage()
                s += (f" - {msg}" if msg else "")+"\n"
        return s
    def clear(self) -> None:
        self._logs.clear()
