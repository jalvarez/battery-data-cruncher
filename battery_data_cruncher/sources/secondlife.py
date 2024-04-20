import requests
from filecache import filecache, MONTH
from bs4 import BeautifulSoup

from ..model import BatteryCell

_URL = "https://secondlifestorage.com/index.php?pages/cell-database/"
_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    + "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
)


@filecache(MONTH)
def get_page():
    headers = {"User-Agent": _AGENT}
    r = requests.get(_URL, headers=headers, allow_redirects=True)
    return r.text


def extract_cell_models():
    s = BeautifulSoup(get_page(), "html5lib")
    cells = []
    for r in s.find_all("table")[1].find_all("tr"):
        columns = r.find_all("td")
        content_columns = [
            c.contents[0] if len(c.contents) > 0 else None for c in columns
        ]
        # for c in content_columns:
        #     print(c)
        if len(content_columns) == 7:
            cells.append(BatteryCell(*content_columns))
    return cells


if __name__ == "__main__":
    models = extract_cell_models()
    for m in models:
        print(f"{m.brand} {m.model}")
