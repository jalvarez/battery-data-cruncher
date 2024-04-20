import requests
import re
from decimal import Decimal
from filecache import filecache, MONTH
from bs4 import BeautifulSoup
import logging
from ..model import BatteryCell

_BASE_URL = "https://secondlifestorage.com/index.php?pages/cell-database/"
_PARSER = "html5lib"
_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    + "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
)
_REQUEST_TIMEOUT_SECS = 30

logger = logging.getLogger(__name__)


@filecache(MONTH)
def get_page(url):
    headers = {"User-Agent": _AGENT}
    r = requests.get(
        url, headers=headers, allow_redirects=True, timeout=_REQUEST_TIMEOUT_SECS
    )
    return r.text


def extract_cell_models():
    s = BeautifulSoup(get_page(_BASE_URL), _PARSER)
    cells = []
    for r in s.find_all("table")[1].find_all("tr"):
        columns = r.find_all("td")
        content_columns = [
            c.contents[0] if len(c.contents) > 0 else None for c in columns[:5]
        ]
        if len(content_columns) == 5:
            logger.debug(f"Processing {content_columns[:1]}")
            image_url = columns[5].contents[0]["src"]
            details_url = columns[6].contents[0]["href"]
            if details_url is not None:
                try:
                    details = extract_cell_details(details_url)
                    cells.append(
                        BatteryCell(
                            *(content_columns + [image_url, details_url] + details)
                        )
                    )
                    break  # TODO DELETE
                except Exception as e:
                    logger.error(e)
    return cells


def extract_cell_details(page):
    details_page_content = BeautifulSoup(get_page(page), _PARSER)
    details_table = details_page_content.find_all("table")[0]
    details_rows = details_table.find_all("tr")
    capacity_row = details_rows[3]
    capacity_content = capacity_row.find_all("td")[1].contents[0]
    capacity = int(re.search("(\d+)mAh", capacity_content).group(1))
    voltaje_row = details_rows[4]
    voltaje_content = voltaje_row.find_all("td")[1].contents[0]
    nominal_voltaje = Decimal(re.search("(\d+\.\d+)V", voltaje_content).group(1))
    return [capacity, nominal_voltaje]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    models = extract_cell_models()
    for m in models[:10]:
        print(f"{m.brand} {m.model} {m.nominal_voltaje}")
    print(f"Battery cell models processed: {len(models)}")
