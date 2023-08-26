from requests import get as rget
from bs4 import BeautifulSoup
from re import search

from FZBypass import Config, LOGGER
from FZBypass.core.bypass_ddl import transcript

async def cinevood(url: str) -> str:
    soup = BeautifulSoup(rget(url).text, 'html.parser')
    titles = soup.select('h6')
    gtlinks = soup.select('a[href*="gdtot"]')
    gflinks = soup.select('a[href*="gdflix"]')
    prsd = f"<b><u>{soup.title.string}</u></b>"
    for n, (t, gt, gf) in enumerate(zip(titles, gtlinks, gflinks), start=1):
        prsd += f'''
        
{n}. <i><b>{t}</b></i>
┃ 
┖ <a href='{gt["href"]}'><b>GDToT Link</b></a> | <a href='{gf["href"]}'><b>GDFlix Link</b></a>'''
    return prsd
    
async def toonworld4all(url: str):
    xml = rget(url).text
    soup = BeautifulSoup(xml, 'html.parser')
    if '/episode/' not in url:
        epl = soup.select('a[href*="/episode/"]')
        tls = soup.select('div[class*="mks_accordion_heading"]')
        stitle = search(r'\"name\":\"(.+)\"', resp.text).group(1).split('"')[0]
        prsd = f'<b><u>{stitle}</u></b>'
        for n, (t, l) in enumerate(zip(tls, epl)):
            prsd += f'''
        
{n}. <i><b>{t.strong.string}</b></i>
┃ 
┖ <b>Episode Link :</b> {l["href"]}'''
        return prsd
    titles = soup.select('h5')
    links = soup.select('a[href*="/redirect/main.php?url="]')
    prsd = f"<b><u>{titles[0].string}</u></b>\n\n<b>Links :</b> "
    prsd += ", ".join(f'''<a href='{await transcript(sl["href"], "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)}'>{sl.string}</a>''' for sl in links)
    return prsd