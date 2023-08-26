from asyncio import gather, create_task
from re import search
from requests import get as rget
from bs4 import BeautifulSoup

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
    if "/redirect/main.php?url=" in url:
        return f'┎ <b>Source Link:</b> {url}\n┃\n┖ <b>Bypass Link:</b> {rget(url).url}'
    xml = rget(url).text
    soup = BeautifulSoup(xml, 'html.parser')
    if '/episode/' not in url:
        epl = soup.select('a[href*="/episode/"]')
        tls = soup.select('div[class*="mks_accordion_heading"]')
        stitle = search(r'\"name\":\"(.+)\"', xml).group(1).split('"')[0]
        prsd = f'<b><i>{stitle}</i></b>'
        for n, (t, l) in enumerate(zip(tls, epl), start=1):
            prsd += f'''
        
{n}. <i><b>{t.strong.string}</b></i>
┃ 
┖ <b>Episode Link :</b> {l["href"]}'''
        return prsd
    links = soup.select('a[href*="/redirect/main.php?url="]')
    titles = soup.select('h5')
    prsd = f"<b><i>{titles[0].string}</i></b>"
    titles.pop(0)
    slicer, _ = divmod(len(links), len(titles))
    atasks = []
    for sl in links:
        atasks.append(create_task(transcript(rget(sl["href"]).url, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)))
    
    com_tasks = await gather(*atasks, return_exceptions=True)
    lstd = [com_tasks[i:i+slicer] for i in range(0, len(com_tasks), slicer)]
    
    for no, tl in enumerate(titles):
        prsd += f"\n\n<b>{tl.string}</b>\n\n<b>Links :</b> "
        for tl, sl in zip(links, lstd[no]):
            if isinstance(sl, Exception):
                prsd += str(sl)
            else:
                prsd += f"<a href='{sl}'>{tl.string}</a>, "
        prsd = prsd[:-2]
    return prsd