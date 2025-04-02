import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict, Any
import re

logger = logging.getLogger(__name__)

class WebpageFetcher:
    """Fetches webpages and extracts metadata without changing the output structure."""

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    TIMEOUT = 10
    CTA_KEYWORDS = {'sign up', 'register', 'buy', 'download', 'try', 'get', 'subscribe'}

    @staticmethod
    def fetch(url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse webpage (synchronous version)."""
        try:
            response = requests.get(
                url,
                headers={"User-Agent": WebpageFetcher.USER_AGENT},
                timeout=WebpageFetcher.TIMEOUT
            )
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    @staticmethod
    def extract_metadata(html_content: str) -> Dict[str, Any]:
        """
        Extract metadata while maintaining EXACT original structure.
        Uses helper methods internally for better readability.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Maintain the exact same structure as your original code
        return {
            'title': WebpageFetcher._get_title(soup),
            'description': WebpageFetcher._get_description(soup),
            'h1_count': len(soup.find_all('h1')),
            'image_count': len(soup.find_all('img')),
            'links_count': len(soup.find_all('a')),
            'has_viewport_meta': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'images_without_alt': WebpageFetcher._count_images_without_alt(soup),
            'inputs_without_labels': WebpageFetcher._count_inputs_without_labels(soup),
            'nav_elements': WebpageFetcher._get_nav_elements(soup),
            'cta_elements': WebpageFetcher._get_cta_elements(soup),
            'has_canonical': bool(soup.find('link', attrs={'rel': 'canonical'}))
        }

    # Helper methods (private) that maintain the same logic but are better organized
    @staticmethod
    def _get_title(soup: BeautifulSoup) -> str:
        return soup.title.string if soup.title else "No title found"

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'] if meta else "No description found"

    @staticmethod
    def _count_images_without_alt(soup: BeautifulSoup) -> int:
        return sum(1 for img in soup.find_all('img') if not img.get('alt'))

    @staticmethod
    def _count_inputs_without_labels(soup: BeautifulSoup) -> int:
        return sum(
            1 for inp in soup.find_all('input')
            if inp.get('id') and not soup.find('label', {'for': inp['id']})
        )

    @staticmethod
    def _get_nav_elements(soup: BeautifulSoup) -> list:
        navs = soup.find_all('nav')
        if not navs:
            navs = soup.find_all(class_=re.compile(r'menu|nav|navigation', re.I))
        return [str(nav) for nav in navs[:3]]

    @staticmethod
    def _get_cta_elements(soup: BeautifulSoup) -> list:
        ctas = []
        for elem in soup.find_all(['a', 'button']):
            text = elem.get_text().lower()
            class_attr = elem.get('class', [])
            class_text = ' '.join(class_attr).lower() if class_attr else ""
            if any(word in text or word in class_text 
                  for word in WebpageFetcher.CTA_KEYWORDS):
                ctas.append(str(elem))
        return ctas[:3]