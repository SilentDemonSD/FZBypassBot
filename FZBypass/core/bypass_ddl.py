from base64 import b64decode
from http.cookiejar import MozillaCookieJar
from json import loads
from os import path
from re import findall, match, search, sub
from time import sleep
from asyncio import sleep as asleep
from urllib.parse import parse_qs, quote, unquote, urlparse
from uuid import uuid4

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from lk21 import Bypass
from lxml import etree
from requests import Session

from FZBypass.core.exceptions import DDLException


async def gyanilinks(url: str) -> str:
    DOMAIN = "https://go.hipsonyc.com/"
    cget = create_scraper(allow_brotli=False).request
    code = url.rstrip("/").split("/")[-1]
    soup = BeautifulSoup(cget("GET", f"{DOMAIN}/{code}").content, "html.parser")
    try: 
        inputs = soup.find(id="go-link").find_all(name="input")
    except: 
        raise DDLException("Incorrect Link Provided")
    await asleep(5)
    resp = cget("POST", f"{DOMAIN}/links/go", data= { input.get('name'): input.get('value') for input in inputs }, headers={ "x-requested-with": "XMLHttpRequest" })
    try: 
        return resp.json()['url']
    except:
        raise DDLException("Link Extraction Failed")


async def tnlink(url: str) -> str:
    DOMAIN = "https://page.tnlink.in/"
    code = url.rstrip("/").split("/")[-1]
    cs = create_scraper()
    cget = cs.request
    while len(cs.cookies) == 0:
        resp = cget("GET", f"{DOMAIN}/{code}", headers={"referer": "https://usanewstoday.club/"})
        await asleep(2)
    soup = BeautifulSoup(resp.content, "html.parser")
    data = { input.get('name'): input.get('value') for input in soup.find_all("input") }
    await asleep(8)
    r = cget("POST", f"{DOMAIN}/links/go", data=data, headers={ "x-requested-with": "XMLHttpRequest" })
    try: 
        return r.json()['url']
    except: 
        raise DDLException("Link Extraction Failed")
