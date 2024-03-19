import requests
import wikipediaapi
from wikipediaapi import Wikipedia
from typing import Final

class WikiResponse:
    Prompt: str
    Expected_Generation: str
    def __init__(self, p:str, eg:str) -> None:
        self.Prompt = p
        self.Expected_Generation = eg

class WikipediaProcessor:
    RANDOM_URL: Final[str] = 'https://en.wikipedia.org/wiki/Special:Random'
    WIKI_PREFIX_LEN: Final[int] = len('https://en.wikipedia.org/wiki/')
    WIKI_SESSION: Final[Wikipedia] = wikipediaapi.Wikipedia('llm-runner', 'en')

    def get_random_page(self) -> str:
        r_resp = requests.get(self.RANDOM_URL)
        return r_resp.url

    def get_input(self, n_prompt:int) -> WikiResponse:
        page = self.get_random_page()
        page = page[self.WIKI_PREFIX_LEN:]
        result = self.WIKI_SESSION.page(page).text
        return WikiResponse(result[:n_prompt], result[n_prompt:])
