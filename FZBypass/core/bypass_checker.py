from re import match
from urllib.parse import urlparse

from FZBypass.core.bypass_dlinks import *
from FZBypass.core.bypass_ddl import *
from FZBypass.core.exceptions import DDLException

fmed_list = ['fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
             'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com']

anonfilesBaseSites = ['anonfiles.com', 'hotfile.io', 'bayfiles.com', 'megaupload.nz', 'letsupload.cc',
                      'filechan.org', 'myfile.is', 'vshare.is', 'rapidshare.nu', 'lolabits.se',
                      'openload.cc', 'share-online.is', 'upvid.cc']

def is_share_link(url):
    return bool(match(r'https?:\/\/.+\.gdtot\.\S+|https?:\/\/(filepress|filebee|appdrive|driveleech|driveseed)\.\S+', url))

async def direct_link_checker(link):
    domain = urlparse(link).hostname
    if bool(match(r"https?:\/\/(yadi|disk.yandex)\.\S+", link)):
        return await yandex_disk(link)
    elif bool(match(r"https?:\/\/try2link\.\S+", link)):
        return await try2link(link)

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
        return await transcript(link, "https://go.moneykamalo.com", "https://techkeshri.com/", 5)
    elif bool(match(r"https?:\/\/tinyfy\.\S+", link)):
        return await transcript(link, "https://tinyfy.in", "https://www.yotrickslog.tech/", 0)
    elif bool(match(r"https?:\/\/adrinolinks\.\S+", link)):
        return await transcript(link, "https://adrinolinks.in", "https://bhojpuritop.in/", 8)
    elif bool(match(r"https?:\/\/krownlinks\.\S+", link)):
        return await transcript(link, "https://go.hostadviser.net/", "blog.hostadviser.net/", 8)
    elif bool(match(r"https?:\/\/du-link\.\S+", link)):
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
    elif bool(match(r"https?:\/\/v2links\.\S+", link)):
        return await transcript(link, "https://v2links.com", "https://gadgetsreview27.com", 6)
    elif bool(match(r"https?:\/\/linkyearn\.\S+", link)):
        return await transcript(link, "https://linkyearn.com", "https://gktech.uk/", 5)
    elif bool(match(r"https?:\/\/earn4link\.\S+", link)):
        return await transcript(link, "https://m.open2get.in/", "https://ezeviral.com/", 8)
    
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
    elif bool(match(r"https?:\/\/(bit|tinyurl|9qr)\.\S+", link)):
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
