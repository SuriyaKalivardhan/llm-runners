import requests
import wikipediaapi
from constants import WikiConstants
from wikipediaapi import Wikipedia
from typing import Tuple
import logging, traceback, time
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.INFO)

class WikiClient:
    def __init__(self):
        self.session: Wikipedia = wikipediaapi.Wikipedia('llm-runner', 'en')

    def _get_random_page(self) -> str:
        r_resp = requests.get(WikiConstants.RANDOM_URL)
        return r_resp.url
    
    def _get_imageurl_from_page(self, url:str) -> Tuple[str, str]:
        r_resp = requests.get(url)        
        soup = BeautifulSoup(r_resp.text, 'html.parser')
        images = soup.find_all("meta", {"property": "og:image"})
        if len(images) > 0:
            title = soup.find("title")
            title = title.string.removesuffix(" - Wikipedia")
            imageUrl = images[-1]['content']
            prompt = f"Is the image related to {title}, can you explain more?"
            return prompt, imageUrl
        return None, None

    def get_random_page_text(self) -> Tuple[str, str]:
        back_off = 5.0
        while True:
            try:
                url = self._get_random_page()
                page = url[WikiConstants.WIKI_PREFIX_LEN:]
                result = self.session.page(page).text
                return page, result
            except Exception as e:
                logging.critical(traceback.format_exc())
                logging.critical(f"Exception caught with Wikiclient {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5

    def get_random_page_textAndImage(self) -> Tuple[str, str, str]:
        back_off = 5.0
        while True:
            try:
                url = self._get_random_page()
                prompt, imageUrl = self._get_imageurl_from_page(url)
                if imageUrl == None:
                    continue
                return prompt, imageUrl
            except Exception as e:
                logging.critical(traceback.format_exc())
                logging.critical(f"Exception caught with Wikiclient {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5