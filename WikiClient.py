import requests
import wikipediaapi
from constants import WikiConstants
from wikipediaapi import Wikipedia
from typing import Tuple
import logging, traceback, time
logging.basicConfig(level=logging.INFO)

class WikiClient:
    def __init__(self):
        self.session: Wikipedia = wikipediaapi.Wikipedia('llm-runner', 'en')

    def _get_random_page(self) -> str:
        r_resp = requests.get(WikiConstants.RANDOM_URL)
        return r_resp.url

    def get_random_page_text(self) -> Tuple[str, str]:
        back_off = 5.0
        while True:
            try:
                page = self._get_random_page()
                page = page[WikiConstants.WIKI_PREFIX_LEN:]
                result = self.session.page(page).text
                return page, result
            except Exception as e:
                logging.critical(traceback.format_exc())
                logging.critical(f"Exception caught with Wikiclient {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5