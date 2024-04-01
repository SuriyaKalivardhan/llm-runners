import requests
import wikipediaapi
from constants import WikiConstants
from wikipediaapi import Wikipedia
from typing import Final
from typing import Tuple

class WikiClient:
    def __init__(self):
        self.session: Wikipedia = wikipediaapi.Wikipedia('llm-runner', 'en')

    def _get_random_page(self) -> str:
        r_resp = requests.get(WikiConstants.RANDOM_URL)
        return r_resp.url

    def get_random_page_text(self) -> Tuple[str, str]:
        page = self._get_random_page()
        page = page[WikiConstants.WIKI_PREFIX_LEN:]
        result = self.session.page(page).text
        return page, result