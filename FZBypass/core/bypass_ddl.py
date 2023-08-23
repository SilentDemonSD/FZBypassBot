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
from lxml import etree
from requests import Session, get as rget

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


async def transcript(url: str, DOMAIN: str, ref: str, sltime) -> str:
    code = url.rstrip("/").split("/")[-1]
    cget = create_scraper(allow_brotli=False).request
    resp = cget("GET", f"{DOMAIN}/{code}", headers={"referer": ref})
    soup = BeautifulSoup(resp.content, "html.parser")
    data = { inp.get('name'): inp.get('value') for inp in soup.find_all("input") }
    await asleep(sltime)
    resp = cget("POST", f"{DOMAIN}/links/go", data=data, headers={ "x-requested-with": "XMLHttpRequest" })
    try: 
        return resp.json()['url']
    except: 
        raise DDLException("Link Extraction Failed")


async def linkvertise(url: str) -> str:
    resp = rget('https://bypass.pm/bypass2', params={'url': url}).json()
    if resp["success"]: 
        return resp["destination"]
    else: 
        raise DDLException(resp["msg"])


async def rslinks(url: str) -> str:
      resp = rget(url, stream=True, allow_redirects=False)
      code = resp.headers["location"].split('ms9')[-1]
      try:
          return f"http://techyproio.blogspot.com/p/short.html?{code}=="
      except:
          raise DDLException("Link Extraction Failed")
      

async def bitly_tinyurl(url: str) -> str:
	try: 
	    return rget(url).url
	except: 
	    raise DDLException("Link Extraction Failed")


async def thinfi(url: str) -> str:
	try: 
	    return BeautifulSoup(rget(url).content,  "html.parser").p.a.get("href")
	except: 
	    raise DDLException("Link Extraction Failed")
