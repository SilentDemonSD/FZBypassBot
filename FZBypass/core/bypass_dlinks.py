from base64 import b64decode
from http.cookiejar import MozillaCookieJar
from json import loads
from os import path
from re import findall, match, search, sub
from time import sleep
from urllib.parse import parse_qs, quote, unquote, urlparse
from uuid import uuid4

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from lk21 import Bypass
from lxml import etree
from requests import session
from aiohttp import ClientSession 

from FZBypass import LOGGER
from FZBypass.core.exceptions import DDLException


async def filepress(url: str):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        async with ClientSession() as sess:
            json_data = {
                'id': raw.path.split('/')[-1],
                'method': 'publicDownlaod',
            }
            async with await sess.post(f'{raw.scheme}://{raw.hostname}/api/file/downlaod/', headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data) as resp:
                d_id = await resp.json()
            if 'data' not in d_id:
                dl_link = f"https://drive.google.com/uc?id={d_id['data']}&export=download"
                parsed = BeautifulSoup(cget('GET', url).text, 'html.parser').find('span')
                combined = str(parsed).rsplit('(', maxsplit=1)
                name = combined[0]
                size = combined[1].replace(')', '') + 'B'
            else:
                dl_link = f'ERROR: {d_id["statusText"]}'
                name, size = "N/A", "N/A"
            del json_data['method']
            async with await sess.post(f'{raw.scheme}://{raw.hostname}/api/file/telegram/downlaod/', headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data) as resp:
                tg_id = await resp.json()
            if "data" in tg_id:
                url = f"https://tghub.xyz/?start={tg_id['data']}"
                bot_name = findall("filepress_\d+_bot", cget('GET', url).text)
                tg_link = f"https://t.me/{bot_name}/?start={tg_id['data']}"
            else:
                tg_link = f'ERROR: {tg_id["statusText"]}'
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__}')
    return f'''<b>Name :<b> <i>{name}</i>
<b>Size :</b> <i>{size}</i>

<b>Drive Link :</b> {dl_link}
<b>TG Link :</b> {tg_link}'''


def gdtot(url):
    cget = create_scraper().request
    try:
        res = cget('GET', f'https://gdtot.pro/file/{url.split("/")[-1]}')
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__}')
    token_url = etree.HTML(res.content).xpath("//a[contains(@class,'inline-flex items-center justify-center')]/@href")
    if not token_url:
        try:
            url = cget('GET', url).url
            p_url = urlparse(url)
            res = cget("GET", f"{p_url.scheme}://{p_url.hostname}/ddl/{url.split('/')[-1]}")
        except Exception as e:
            raise DDLException(f'ERROR: {e.__class__.__name__}')
        if (drive_link := findall(r"myDl\('(.*?)'\)", res.text)) and "drive.google.com" in drive_link[0]:
            return drive_link[0]
        elif Config.GDTOT_CRYPT:
            cget('GET', url, cookies={'crypt': Config.GDTOT_CRYPT})
            p_url = urlparse(url)
            js_script = cget('GET', f"{p_url.scheme}://{p_url.hostname}/dld?id={url.split('/')[-1]}")
            g_id = findall('gd=(.*?)&', js_script.text)
            try:
                decoded_id = b64decode(str(g_id[0])).decode('utf-8')
            except:
                raise DDLException("ERROR: Try in your browser, mostly file not found or user limit exceeded!")
            return f'https://drive.google.com/open?id={decoded_id}'
        else:
            raise DDLException('ERROR: Drive Link not found, Try in your broswer! GDTOT_CRYPT not Provided, it increases efficiency!')
    token_url = token_url[0]
    try:
        token_page = cget('GET', token_url)
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__} with {token_url}')
    path = findall('\("(.*?)"\)', token_page.text)
    if not path:
        raise DDLException('ERROR: Cannot bypass this')
    path = path[0]
    raw = urlparse(token_url)
    final_url = f'{raw.scheme}://{raw.hostname}{path}'
    return sharer_scraper(final_url)


def sharer_scraper(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        header = {"useragent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10"}
        res = cget('GET', url, headers=header)
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__}')
    key = findall('"key",\s+"(.*?)"', res.text)
    if not key:
        raise DDLException("ERROR: Key not found!")
    key = key[0]
    if not etree.HTML(res.content).xpath("//button[@id='drc']"):
        raise DDLException("ERROR: This link don't have direct download button")
    boundary = uuid4()
    headers = {
        'Content-Type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary}',
        'x-token': raw.hostname,
        'useragent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10'
    }

    data = f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
        f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
        f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
        f'------WebKitFormBoundary{boundary}--\r\n'
    try:
        res = cget("POST", url, cookies=res.cookies,
                   headers=headers, data=data).json()
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__}')
    if "url" not in res:
        raise DDLException('ERROR: Drive Link not found, Try in your broswer')
    if "drive.google.com" in res["url"]:
        return res["url"]
    try:
        res = cget('GET', res["url"])
    except Exception as e:
        raise DDLException(f'ERROR: {e.__class__.__name__}')
    if (drive_link := etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")) and "drive.google.com" in drive_link[0]:
        return drive_link[0]
    else:
        raise DDLException('ERROR: Drive Link not found, Try in your broswer')



