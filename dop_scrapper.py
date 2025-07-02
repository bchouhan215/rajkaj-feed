# dop_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://dop.rajasthan.gov.in/Content/news.aspx"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"id": "cpMain_grdNews"})

items = []
rows = table.find_all("tr")[1:]

for row in rows:
    tds = row.find_all("td")
    link = tds[1].find("a")
    title = link.text.strip()
    href = link['href']
    if not href.startswith("http"):
        href = "https://dop.rajasthan.gov.in" + href
    pub_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    item = f"""
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{href}</link>
        <description><![CDATA[{title}]]></description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """
    items.append(item)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>DOP Rajasthan Notifications</title>
    <link>{url}</link>
    <description>Auto feed for DOP Rajasthan updates</description>
    <language>en-IN</language>
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
    {''.join(items)}
</channel>
</rss>"""

with open("dop_feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)
