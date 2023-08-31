from asyncio import gather, create_task
from re import search, match, findall, sub
from requests import get as rget
from cloudscraper import create_scraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup, NavigableString, Tag

from FZBypass import Config, LOGGER
from FZBypass.core.bypass_ddl import transcript


async def sharespark(url: str) -> str:
    gd_txt = ""
    cget = create_scraper().request
    res = cget("GET", "?action=printpage;".join(url.split('?'))) 
    soup = BeautifulSoup(res.text, 'html.parser') 
    for br in soup.findAll('br'): 
        next_s = br.nextSibling
        if not (next_s and isinstance(next_s, NavigableString)): 
            continue
        if (next2_s := next_s.nextSibling) and isinstance(next2_s, Tag) and next2_s.name == 'br' and str(next_s).strip():
            if match(r'^(480p|720p|1080p)(.+)? Links:\Z', next_s): 
                gd_txt += f'<b>{next_s.replace("Links:", "GDToT Links :")}</b>\n\n' 
            for s in next_s.split(): 
                ns = sub(r'\(|\)', '', s)
                if match(r'https?://.+\.gdtot\.\S+', ns):
                    soup = BeautifulSoup(cget("GET", ns).text, "html.parser")
                    parse_data = (soup.select('meta[property^="og:description"]')[0]['content']).replace('Download ' , '').rsplit('-', maxsplit=1)
                    gd_txt += f"┎ <b>Name :</b> {parse_data[0]}\n┠ <b>Size :</b> {parse_data[-1]}\n┃\n┖ <b>GDTot :</b> {ns}\n\n"
                elif match(r'https?://pastetot\.\S+', ns):
                    nxt = sub(r'\(|\)|(https?://pastetot\.\S+)', '', next_s) 
                    gd_txt += f"\n<b>{nxt}</b>\n┖ {ns}\n"
        if len(gd_txt) > 4000:
            return gd_txt # Broken Function
    if gd_txt != "": 
        return gd_txt


async def skymovieshd(url: str) -> str:
    soup = BeautifulSoup(rget(url, allow_redirects=False).text, 'html.parser')
    t = soup.select('div[class^="Robiul"]')
    gd_txt = f"<i>{t[-1].text.replace('Download ', '')}</i>"
    _cache = []
    for link in soup.select('a[href*="howblogs.xyz"]'):
        if link['href'] in _cache:
            continue
        _cache.append(link['href'])
        gd_txt += f"\n\n<b>{link.text} :</b> \n"
        nsoup = BeautifulSoup(rget(link['href'], allow_redirects=False).text, 'html.parser') 
        atag = nsoup.select('div[class="cotent-box"] > a[href]')
        for no, link in enumerate(atag, start=1): 
            gd_txt += f"{no}. {link['href']}\n"
    return gd_txt


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


async def kayoanime(url: str) -> str:
    soup = BeautifulSoup(rget(url).text, 'html.parser')
    titles = soup.select('h6')
    gdlinks = soup.select('a[href*="drive.google.com"], a[href*="tinyurl"]')
    prsd = f"<b>{soup.title.string}</b>"
    gd_txt, link = "GDrive", ""
    for n, gd in enumerate(gdlinks, start=1):
        if (link := gd["href"]) and "tinyurl" in link:
            link = rget(link).url
            domain = urlparse(link).hostname
            gd_txt = "Mega" if "mega" in domain else "G Group" if "groups" in domain else "Direct Link"
        prsd += f'''

{n}. <i><b>{gd.string}</b></i>
┗ <b>Links :</b> <a href='{link}'><b>{gd_txt}</b></a>'''
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
┖ <b>Link :</b> {l["href"]}'''
        return prsd
    links = soup.select('a[href*="/redirect/main.php?url="]')
    titles = soup.select('h5')
    prsd = f"<b><i>{titles[0].string}</i></b>"
    titles.pop(0)
    slicer, _ = divmod(len(links), len(titles))
    atasks, nsl = [], ""
    for sl in links:
        while "rocklinks" not in nsl:
            nsl = rget(sl["href"], allow_redirects=False).headers['location']
        atasks.append(create_task(transcript(nsl, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)))

    com_tasks = await gather(*atasks, return_exceptions=True)
    lstd = [com_tasks[i:i+slicer] for i in range(0, len(com_tasks), slicer)]
    
    for no, tl in enumerate(titles):
        prsd += f"\n\n<b>{tl.string}</b>\n┃\n┖ <b>Links :</b> "
        for tl, sl in zip(links, lstd[no]):
            if isinstance(sl, Exception):
                prsd += str(sl)
            else:
                prsd += f"<a href='{sl}'>{tl.string}</a>, "
        prsd = prsd[:-2]
    return prsd