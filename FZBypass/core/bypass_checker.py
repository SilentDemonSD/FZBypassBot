from re import match
from urllib.parse import urlparse

from FZBypass.core.bypass_dlinks import *
from FZBypass.core.bypass_ddl import *
from FZBypass.core.bypass_scrape import *
from FZBypass.core.exceptions import DDLException

fmed_list = ['fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
             'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com']

anonSites = ['hotfile.io', 'bayfiles.com', 'megaupload.nz', 'letsupload.cc',
            'filechan.org', 'myfile.is', 'vshare.is', 'rapidshare.nu', 'lolabits.se',
            'openload.cc', 'share-online.is', 'upvid.cc']

def is_share_link(url):
    return bool(match(r'https?:\/\/.+\.(gdtot|gdflix)\.\S+|https?:\/\/(filepress|filebee|appdrive|driveleech|driveseed)\.\S+', url))

def is_excep_link(url):
    return bool(match(r'https?:\/\/.+\.(gdtot|gdflix)\.\S+|https?:\/\/(sharespark|skymovieshd|toonworld4all|kayoanime|cinevood|filepress|filebee|appdrive|driveleech|driveseed)\.\S+', url))

async def direct_link_checker(link):
    domain = urlparse(link).hostname

    # DDL Links
    if bool(match(r"https?:\/\/(yadi|disk.yandex)\.\S+", link)):
        return await yandex_disk(link)
    elif bool(match(r"https?:\/\/try2link\.\S+", link)):
        return await try2link(link)
    elif bool(match(r"https?:\/\/.+\.mediafire\.\S+", link)):
        return await mediafire(link)
    elif bool(match(r"https?:\/\/shrdsk\.\S+", link)):
        return await shrdsk(link)
    elif any(x in domain for x in anonSites):
        return await anonsites(link)
    elif any(x in domain for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
        return await terabox(link)

    elif bool(match(r"https?:\/\/(gyanilinks|gtlinks)\.\S+", link)):
        return await gyanilinks(link)
    elif bool(match(r"https?:\/\/.+\.tnshort\.\S+", link)):
        return await transcript(link, "https://news.speedynews.xyz/", "https://market.finclub.in/", 8)
    elif bool(match(r"https?:\/\/(xpshort|push.bdnewsx|techymozo)\.\S+", link)):
        return await transcript(link, "https://xpshort.com/", "https://www.twinthrottlers.xyz/", 8)
    elif bool(match(r"https?:\/\/go.lolshort\.\S+", link)):
        return await transcript(link, "https://get.lolshort.tech/", "https://tech.animezia.com/", 8)
    elif bool(match(r"https?:\/\/go.onepagelink\.\S+", link)):
        return await transcript(link, "go.onepagelink.in", "gorating.in", 9)
    elif bool(match(r"https?:\/\/earn.moneykamalo\.\S+", link)):
        return await transcript(link, "https://go.moneykamalo.com", "https://blog.techkeshri.com/", 5)
    elif bool(match(r"https?:\/\/tinyfy\.\S+", link)):
        return await transcript(link, "https://tinyfy.in", "https://www.yotrickslog.tech/", 0)
    elif bool(match(r"https?:\/\/adrinolinks\.\S+", link)):
        return await transcript(link, "https://adrinolinks.in", "https://bhojpuritop.in/", 8)
    elif bool(match(r"https?:\/\/krownlinks\.\S+", link)):
        return await transcript(link, "https://go.hostadviser.net/", "blog.hostadviser.net/", 8)
    elif bool(match(r"https?:\/\/(du-link|dulink)\.\S+", link)):
        return await transcript(link, "https://du-link.in", "https://profitshort.com/", 0)
    elif bool(match(r"https?:\/\/indianshortner\.\S+", link)):
        return await transcript(link, "https://indianshortner.com/", "https://moddingzone.in/", 5)
    elif bool(match(r"https?:\/\/m.easysky\.\S+", link)):
        return await transcript(link, "https://techy.veganab.co/", "https://veganab.co/", 8)
    elif bool(match(r"https?:\/\/linkbnao\.\S+", link)):
        return await transcript(link, "https://vip.linkbnao.com", "https://ffworld.xyz/", 2)
    elif bool(match(r"https?:\/\/go.indiurl\.\S+", link)):
        return await transcript(link, "https://file.earnash.com/", "https://indiurl.cordtpoint.co.in/", 10)
    elif bool(match(r"https?:\/\/go.earnl\.\S+", link)):
        return await transcript(link, "https://v.earnl.xyz", "https://link.modmakers.xyz/", 5)
    elif bool(match(r"https?:\/\/.+\.tnlink\.\S+", link)):
        return await transcript(link, "https://page.tnlink.in/", "https://financeyogi.net/", 8)
    elif bool(match(r"https?:\/\/link4earn\.\S+", link)):
        return await transcript(link, "https://link4earn.com", "https://studyis.xyz/", 6)
    elif bool(match(r"https?:\/\/shortingly\.\S+", link)):
        return await transcript(link, "https://shortingly.in", "https://tech.gyanitheme.com/", 5)
    elif bool(match(r"https?:\/\/go.flashlink\.\S+", link)):
        return await transcript(link, "https://files.earnash.com/", "https://flash1.cordtpoint.co.in", 15)
    elif bool(match(r"https?:\/\/short2url\.\S+", link)):
        return await transcript(link, "https://techyuth.xyz/blog", "https://blog.coin2pay.xyz/", 10)
    elif bool(match(r"https?:\/\/urlsopen\.\S+", link)):
        return await transcript(link, "https://blogpost.viewboonposts.com/e998933f1f665f5e75f2d1ae0009e0063ed66f889000", "https://blog.textpage.xyz/", 2)
    elif bool(match(r"https?:\/\/mdisk\.\S+", link)):
        return await transcript(link, "https://mdisk.pro", "https://m.meclipstudy.in/", 8)
    elif bool(match(r"https?:\/\/(pkin|go.paisakamalo)\.\S+", link)):
        return await transcript(link, "https://go.paisakamalo.in", "https://weightloss.techkeshri.com/", 9)
    elif bool(match(r"https?:\/\/linkpays\.\S+", link)):
        return await transcript(link, "https://tech.smallinfo.in/Gadget/", "https://finance.filmypoints.in/", 6)
    elif bool(match(r"https?:\/\/sklinks\.\S+", link)):
        return await transcript(link, "https://sklinks.in", "https://dailynew.online/", 5)
    elif bool(match(r"https?:\/\/link1s\.\S+", link)):
        return await transcript(link, "https://link1s.com", "https://anhdep24.com/", 9)
    elif bool(match(r"https?:\/\/tulinks\.\S+", link)):
        return await transcript(link, "https://tulinks.one", "https://www.blogger.com/", 8)
    elif bool(match(r"https?:\/\/.+\.tulinks\.\S+", link)):
        return await transcript(link, "https://go.tulinks.online", "https://tutelugu.co/", 8)
    elif bool(match(r"https?:\/\/powerlinks\.\S+", link)):
        return await transcript(link, "http://powerlinks.site", "http://powerlinks.site", 5)
    elif bool(match(r"https?:\/\/(.+\.)?vipurl\.\S+", link)):
        return await transcript(link, "https://count.vipurl.in/", "https://loanhelpful.net/", 9)
    elif bool(match(r"https?:\/\/indyshare\.\S+", link)):
        return await transcript(link, "https://indyshare.net", "https://bestdjsong.com", 6)
    elif bool(match(r"https?:\/\/linkyearn\.\S+", link)):
        return await transcript(link, "https://linkyearn.com", "https://gktech.uk/", 5)
    elif bool(match(r"https?:\/\/earn4link\.\S+", link)):
        return await transcript(link, "https://m.open2get.in/", "https://ezeviral.com/", 8)
    elif bool(match(r"https?:\/\/linksly\.\S+", link)):
        return await transcript(link, "https://go.linksly.co/", "https://en.themezon.net/", 5)
    elif bool(match(r"https?:\/\/.+\.mdiskshortner\.\S+", link)):
        return await transcript(link, "https://loans.yosite.net/", "https://yosite.net/", 10)
    elif bool(match(r"https?:\/\/.+\.rocklinks\.\S+", link)):
        return await transcript(link, "https://insurance.techymedies.com/", "https://highkeyfinance.com/", 5)
    elif bool(match(r"https?:\/\/mplaylink\.\S+", link)):
        return await transcript(link, "https://tera-box.cloud/", "https://zisnews.com/", 5)
    elif bool(match(r"https?:\/\/shrinke\.\S+", link)):
        return await transcript(link, "https://en.shrinke.me/", "https://themezon.net/", 15)
    elif bool(match(r"https?:\/\/urlspay\.\S+", link)):
        return await transcript(link, "https://finance.smallinfo.in/", "https://loans.techyinfo.in/", 5)
    elif bool(match(r"https?:\/\/.+\.tnvalue\.\S+", link)):
        return await transcript(link, "https://page.finclub.in/", "https://finclub.in/", 8)
    elif bool(match(r"https?:\/\/sxslink\.\S+", link)):
        return await transcript(link, "https://getlink.sxslink.com/", "https://cinemapettai.in/", 5)
    elif bool(match(r"https?:\/\/ziplinker\.\S+", link)):
        return await transcript(link, "https://ziplinker.net/web/", "https://ontechhindi.com/", 5)
    elif bool(match(r"https?:\/\/moneycase\.\S+", link)):
        return await transcript(link, "https://page.moneycase.link/", "https://www.infokeeda.xyz/", 5)
    elif bool(match(r"https?:\/\/urllinkshort\.\S+", link)):
        return await transcript(link, "https://web.urllinkshort.in", "https://suntechu.in/", 5)
    elif bool(match(r"https?:\/\/.+\.dtglinks\.\S+", link)):
        return await transcript(link, "https://happyfiles.dtglinks.in/", "https://tech.filohappy.in/", 5)
    elif bool(match(r"https?:\/\/v2links\.\S+", link)):
        return await transcript(link, "https://vzu.us/", "https://gadgetsreview27.com/", 5)
    
    elif bool(match(r"https?:\/\/ouo\.\S+", link)):
        return await ouo(link)
    elif bool(match(r"https?:\/\/(shareus|shrs)\.\S+", link)):
        return await shareus(link)
    elif bool(match(r"https?:\/\/dropbox\.\S+", link)):
        return await dropbox(link)
    elif bool(match(r"https?:\/\/linkvertise\.\S+", link)):
        return await linkvertise(link)
    elif bool(match(r"https?:\/\/rslinks\.\S+", link)):
        return await rslinks(link)
    elif bool(match(r"https?:\/\/(bit|tinyurl|9qr|shorturl|aylm.short.gy)\.\S+", link)):
        return await bitly_tinyurl(link)
    elif bool(match(r"https?:\/\/thinfi\.\S+", link)):
        return await thinfi(link)
        
    # DL Sites
    elif bool(match(r"https?:\/\/cinevood\.\S+", link)):
        return await cinevood(link)
    elif bool(match(r"https?:\/\/kayoanime\.\S+", link)):
        return await kayoanime(link)
    elif bool(match(r"https?:\/\/toonworld4all\.\S+", link)):
        return await toonworld4all(link)
    elif bool(match(r"https?:\/\/skymovieshd\.\S+", link)):
        return await skymovieshd(link)
    elif bool(match(r"https?:\/\/.+\.sharespark\.\S+", link)):
        return await sharespark(link)
    
    # DL Links
    elif is_share_link(link):
        if 'gdtot' in domain:
            return await gdtot(link)
        elif 'filepress' in domain:
            return await filepress(link)
        elif 'appdrive' in domain or 'gdflix' in domain:
            return await appflix(link)
        else:
            return await sharer_scraper(link)
    else:
        raise DDLException(f'<i>No Bypass Function Found for your Link :</i> <code>{link}</code>')
