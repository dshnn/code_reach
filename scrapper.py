from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import re

def contact_page(url,soup,headers):
    keyword = ['contact', 'about', 'team', 'reach-us', 'get-in-touch']
    
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        a_text = a.get_text(strip=True).lower()
        if any(kw in href or kw in a_text for kw in keyword):
            contact_pg = urljoin(url, a['href'])
            if urlparse(contact_pg).netloc == urlparse(url).netloc:
                try:
                    beautisoup = requests.get(contact_pg, headers=headers, timeout=10)
                    return BeautifulSoup(beautisoup.text, "html.parser")
                except:
                    return None


def extract_fuzzy_email(text):
    standard_email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    encoded = re.findall(r"[A-Za-z0-9._%+-]+\s*[\[\(]?at[\]\)]?\s*[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text, re.IGNORECASE)
    
    cleaned_encoded = [
        re.sub(r'\s*[\[\(]?at[\]\)]?\s*', '@', e, flags=re.IGNORECASE)
        for e in encoded
    ]

    all_email = list(set(standard_email + cleaned_encoded))

    return [e for e in all_email 
            if not any(e.endswith(ext) for ext in ['.png','.jpg','.gif','.svg','.css'])]


def scraper(url):
    headers = {
       "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(e)
        return {"scrapping_failed":True, "reason":"hit error in try catch"}
    soup = BeautifulSoup(response.text,"html.parser")
    des = None
    links = []
    emails = []
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    body_text = soup.get_text(strip=True)

    if len(body_text) < 0:
        return {"scrapping_failed" : True, "reason":"Javascript"}

    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title=None
     
    contact_soup = contact_page(url, soup, headers)
    if contact_soup:
        contact_text = contact_soup.get_text(strip=True)
        emails.extend(re.findall(pattern, contact_text))
        emails.extend(extract_fuzzy_email(contact_soup.get_text(strip=True)))
        

    for a in contact_soup.find_all("a", href=True):
        if a["href"].startswith("mailto:"):
            email = a["href"].removeprefix("mailto:").split("?")[0]
            emails.append(email)
   
    for a in soup.find_all("a", href=True):
        an=a["href"]
        ab_url=urljoin(url, an)
        links.append(ab_url)

    for m in soup.find_all("meta"):
        if m.get("name") == "description":
            des=(m.get("content"))
            break

    result = {
             "url":url,
             "title":title,
             "description" : des,
             "body" : body_text[:2000],
             "link" : links[:20],
             "emails" : emails,
             "has_emails":len(emails)>0,
             "scrapping_failed":False
           }
    return result
    