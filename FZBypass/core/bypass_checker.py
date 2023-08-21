from re import match
from urllib.parse import urlparse

from FZBypass.core.bypass_dlinks import *
from FZBypass.core.bypass_ddl import *
from FZBypass.core.exceptions import DDLException

def is_share_link(url):
    return bool(match(r'https?:\/\/.+\.gdtot\.\S+|https?:\/\/(filepress|filebee|appdrive|gdflix|driveseed)\.\S+', url))

async def direct_link_checker(link):
    domain = urlparse(link).hostname
    if bool(match(r"https?:\/\/(gyanilinks|gtlinks)\.\S+", link)):
        return await gyanilinks(link)
    elif bool(match(r"https?:\/\/.+\.tnshort\.\S+", link)):
        return await transcript(link, "https://news.speedynews.xyz/", "https://market.finclub.in/")
    elif bool(match(r"https?:\/\/xpshort\.\S+", link)):
        return await transcript(link, "https://xpshort.com", "https://www.twinthrottlers.xyz/")
    elif bool(match(r"https?:\/\/(bit|tinyurl)\.\S+", link)):
        return await bitly_tinyurl(link)
    elif bool(match(r"https?:\/\/thinfi\.\S+", link)):
        return await thinfi(link)
    elif is_share_link(link):
        if 'gdtot' in domain:
            return await gdtot(link)
        elif 'filepress' in domain:
            return await filepress(link)
        elif 'appdrive' in domain:
            return await appdrive(link)
        else:
            return await sharer_scraper(link)
    else:
        raise DDLException(f'<i>No Bypass Function Found for your Link :</i> <code>{link}</code>')
