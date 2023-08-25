from requests import get as rget
from bs4 import BeautifulSoup


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
┠ <b>GDToT Link :</b> <code>{gt["href"]}</code>
┖ <b>GDFlix Link :</b> <code>{gf["href"]}</code>'''
    return prsd