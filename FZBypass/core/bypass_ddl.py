from base64 import b64decode
from http.cookiejar import MozillaCookieJar
from json import loads
from os import path
from re import findall, match, search, sub, compile
from time import sleep
from asyncio import sleep as asleep
from urllib.parse import parse_qs, quote, unquote, urlparse
from uuid import uuid4

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from curl_cffi.requests import Session as cSession
from lxml import etree
from requests import Session, get as rget

from FZBypass.core.exceptions import DDLException
from FZBypass.core.recaptcha import recaptchaV3


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


async def ouo(url: str): 
    tempurl = url.replace("ouo.press", "ouo.io") 
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    client = cSession(headers={'authority': 'ouo.io', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'cache-control': 'max-age=0', 'referer': 'http://www.google.com/ig/adde?moduleurl=', 'upgrade-insecure-requests': '1'}) 
    res = client.get(tempurl, impersonate="chrome110") 
    next_url = f"{p.scheme}://{p.hostname}/go/{id}" 
  
    for _ in range(2): 
         if res.headers.get('Location'): 
            break 
         bs4 = BeautifulSoup(res.content, 'lxml') 
         inputs = bs4.form.findAll("input", {"name": compile(r"token$")}) 
         data = { inp.get('name'): inp.get('value') for inp in inputs } 
         data['x-token'] = await recaptchaV3()
         res = client.post(next_url, data=data, headers= {'content-type': 'application/x-www-form-urlencoded'}, allow_redirects=False, impersonate="chrome110") 
         next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}" 
  
    return  res.headers.get('Location')


async def mdisk(url: str) -> str: 
    header = {'Accept': '*/*', 
         'Accept-Language': 'en-US,en;q=0.5', 
         'Accept-Encoding': 'gzip, deflate, br', 
         'Referer': 'https://mdisk.me/', 
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36' }
    URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={url.rstrip("/").split("/")[-1]}'
    res = rget(url=URL, headers=header).json() 
    return res['download'] + '\n\n' + res['source']


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


async def shareus(url: str) -> str: 
    DOMAIN = "https://us-central1-my-apps-server.cloudfunctions.net" 
    cget = create_scraper().request
    params = {'shortid': url.rstrip('/').split("/")[-1] , 'initial': 'true', 'referrer': 'https://shareus.io/'}
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    resp = cget("GET", f'{DOMAIN}/v', params=params, headers=headers)
    for page in range(1, 4): 
        resp = cget("POST", f'{DOMAIN}/v', headers=headers, json={'current_page': page}) 
    try:
        return (cget('GET', f'{DOMAIN}/get_link', headers=headers).json())["link_info"]["destination"]
    except:
        raise DDLException("Link Extraction Failed")


async def dropbox(url: str) -> str: 
     return url.replace("www.","").replace("dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")


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
