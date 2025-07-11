# rajkaj_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC

url = "https://rajkaj.rajasthan.gov.in"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

notifications = soup.select("ul#notification li a")

rss_items = []
for link in notifications:
    title = link.text.strip()
    href = link.get("href")
    if not href.startswith("http"):
        href = url + href
    pub_date = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')

    item = f"""
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{href}</link>
        <description><![CDATA[{title}]]></description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """
    rss_items.append(item)

rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>RajKaj Rajasthan Notifications</title>
    <link>{url}</link>
    <description>Auto-generated feed from RajKaj</description>
    <language>en-IN</language>
    <lastBuildDate>{datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
    {''.join(rss_items)}
</channel>
</rss>"""

with open("rajkaj_feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("✅ RajKaj RSS feed generated: rajkaj_feed.xml")
