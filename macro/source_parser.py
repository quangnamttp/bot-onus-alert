import requests
from bs4 import BeautifulSoup

def parse_news_from_url(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(p.text for p in paragraphs[:5])
        return content.strip()
    except:
        return "Không thể phân tích nội dung từ nguồn."
