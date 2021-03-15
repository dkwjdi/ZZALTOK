import os
from config import config


def convertURLToPath(URL: str, basePath: str = config.root) -> str:
    idx = URL.find(basePath)
    idx = (0 if idx == -1 else idx + len(basePath)) + 1


def convertPathToURL(path: str, baseUrl: str, basePath: str = config.root) -> str:
    idx = path.find(basePath)
    idx = (0 if idx == -1 else idx + len(basePath))
    return (baseUrl if baseUrl.endswith('/') else baseUrl + '/') + path[idx:]
