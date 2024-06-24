from requests import post as rpost ,get as rget
from re import findall, compile
from time import sleep, time
from asyncio import sleep as asleep
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from curl_cffi.requests import Session as cSession
from requests import Session, get as rget
from aiohttp import ClientSession

from FZBypass import Config
from FZBypass.core.exceptions import DDLException
from FZBypass.core.recaptcha import recaptchaV3

async def get_readable_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h{minutes}m{seconds}s"


async def yandex_disk(url: str) -> str:
    cget = create_scraper().request
    try:
        return cget(
            "get",
            f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={url}",
        ).json()["href"]
    except KeyError:
        raise DDLException("File not Found / Download Limit Exceeded")


async def mediafire(url: str):
    if final_link := findall(
        r"https?:\/\/download\d+\.mediafire\.com\/\S+\/\S+\/\S+", url
    ):
        return final_link[0]
    cget = create_scraper().request
    try:
        url = cget("get", url).url
        page = cget("get", url).text
    except Exception as e:
        raise DDLException(f"{e.__class__.__name__}")
    if final_link := findall(
        r"\'(https?:\/\/download\d+\.mediafire\.com\/\S+\/\S+\/\S+)\'", page
    ):
        return final_link[0]
    elif temp_link := findall(
        r'\/\/(www\.mediafire\.com\/file\/\S+\/\S+\/file\?\S+)', page
    ):
        return await mediafire("https://"+temp_link[0].strip('"'))
    else:
        raise DDLException("No links found in this page")


async def shrdsk(url: str) -> str:
    cget = create_scraper().request
    try:
        url = cget("GET", url).url
        res = cget(
            "GET",
            f'https://us-central1-affiliate2apk.cloudfunctions.net/get_data?shortid={url.split("/")[-1]}',
        )
    except Exception as e:
        raise DDLException(f"{e.__class__.__name__}")
    if res.status_code != 200:
        raise DDLException(f"Status Code {res.status_code}")
    res = res.json()
    if "type" in res and res["type"].lower() == "upload" and "video_url" in res:
        return quote(res["video_url"], safe=":/")
    raise DDLException("No Direct Link Found")


async def terabox(url: str) -> str:
    sess = Session()

    def retryme(url):
        while True:
            try:
                return sess.get(url)
            except:
                pass

    url = retryme(url).url
    key = url.split("?surl=")[-1]
    url = f"http://www.terabox.com/wap/share/filelist?surl={key}"
    sess.cookies.update({"ndus": Config.TERA_COOKIE})

    res = retryme(url)
    key = res.url.split("?surl=")[-1]
    soup = BeautifulSoup(res.content, "lxml")
    jsToken = None

    for fs in soup.find_all("script"):
        fstring = fs.string
        if fstring and fstring.startswith("try {eval(decodeURIComponent"):
            jsToken = fstring.split("%22")[1]

    res = retryme(
        f"https://www.terabox.com/share/list?app_id=250528&jsToken={jsToken}&shorturl={key}&root=1"
    )
    result = res.json()
    if result["errno"] != 0:
        raise DDLException(f"{result['errmsg']}' Check cookies")
    result = result["list"]
    if len(result) > 1:
        raise DDLException("Can't download mutiple files")
    result = result[0]

    if result["isdir"] != "0":
        raise DDLException("Can't download folder")
    try:
        return result["dlink"]
    except:
        raise DDLException("Link Extraction Failed")

async def try2link(url: str) -> str:
    DOMAIN = 'https://try2link.com'
    code = url.split('/')[-1]

    async with ClientSession() as session:
        referers = ['https://hightrip.net/', 'https://to-travel.netl', 'https://world2our.com/']
        for referer in referers:
            async with session.get(f'{DOMAIN}/{code}', headers={"Referer": referer}) as res:
                if res.status == 200:
                    html = await res.text()
                    break
        soup = BeautifulSoup(html, "html.parser")
        inputs = soup.find(id="go-link").find_all(name="input")
        data = { input.get('name'): input.get('value') for input in inputs }
        await asleep(6)
        async with session.post(f"{DOMAIN}/links/go", data=data, headers={ "X-Requested-With": "XMLHttpRequest" }) as resp:
            if 'application/json' in resp.headers.get('Content-Type'):
                json_data = await resp.json()  
                try:
                    return json_data['url']
                except:        
                    raise DDLException("Link Extraction Failed")


async def gyanilinks(url: str) -> str:
    '''
    Based on https://github.com/whitedemon938/Bypass-Scripts
    '''
    code = url.split('/')[-1]
    useragent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    DOMAIN = "https://go.bloggingaro.com"
    
    async with ClientSession() as session:
        async with session.get(f"{DOMAIN}/{code}", headers={'Referer':'https://tech.hipsonyc.com/','User-Agent': useragent}) as res:
            cookies = res.cookies
            html = await res.text()
        async with session.get(f"{DOMAIN}/{code}", headers={'Referer':'https://hipsonyc.com/','User-Agent': useragent}, cookies=cookies) as resp:
            html = await resp.text()
        soup = BeautifulSoup(html, 'html.parser')
        data = {inp.get('name'): inp.get('value') for inp in soup.find_all('input')}
        await asleep(5)
        async with session.post(f"{DOMAIN}/links/go", data=data, headers={'X-Requested-With':'XMLHttpRequest','User-Agent': useragent, 'Referer': f"{DOMAIN}/{code}"}, cookies=cookies) as links:
            if 'application/json' in links.headers.get('Content-Type'):
                try:
                    return (await links.json())['url']
                except Exception:
                      raise DDLException("Link Extraction Failed")


async def ouo(url: str):
    tempurl = url.replace("ouo.io", "ouo.press")
    p = urlparse(tempurl)
    id = tempurl.split("/")[-1]
    client = cSession(
        headers={
            "authority": "ouo.press",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "referer": "http://www.google.com/ig/adde?moduleurl=",
            "upgrade-insecure-requests": "1",
        }
    )
    res = client.get(tempurl, impersonate="chrome110")
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get("Location"):
            break
        bs4 = BeautifulSoup(res.content, "lxml")
        inputs = bs4.form.findAll("input", {"name": compile(r"token$")})
        data = {inp.get("name"): inp.get("value") for inp in inputs}
        data["x-token"] = await recaptchaV3()
        res = client.post(
            next_url,
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"},
            allow_redirects=False,
            impersonate="chrome110",
        )
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return res.headers.get("Location")


async def mdisk(url: str) -> str:
    """
    Depreciated ( Code Preserved )
    """
    header = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://mdisk.me/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    }
    URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={url.rstrip("/").split("/")[-1]}'
    res = rget(url=URL, headers=header).json()
    return res["download"] + "\n\n" + res["source"]


async def transcript(url: str, DOMAIN: str, ref: str, sltime) -> str:
    code = url.rstrip("/").split("/")[-1]
    useragent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'

    async with ClientSession() as session:
         async with session.get(f"{DOMAIN}/{code}", headers={'Referer': ref, 'User-Agent': useragent}) as res:
             html = await res.text()
             cookies = res.cookies
         soup = BeautifulSoup(html, "html.parser")
         title_tag = soup.find('title')
         if title_tag and title_tag.text == 'Just a moment...':
             return "Unable To Bypass Due To Cloudflare Protected"
         else:
             data = {inp.get('name'): inp.get('value') for inp in soup.find_all('input') if inp.get('name') and inp.get('value')}
             await asleep(sltime)
             async with session.post(f"{DOMAIN}/links/go", data=data, headers={'Referer': f"{DOMAIN}/{code}", 'X-Requested-With':'XMLHttpRequest', 'User-Agent': useragent}, cookies=cookies) as resp:
                  try:
                      if 'application/json' in resp.headers.get('Content-Type'):
                          return (await resp.json())['url']
                  except Exception:
                      raise DDLException("Link Extraction Failed")


async def justpaste(url: str):
    resp = rget(url, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    inps = soup.select('div[id="articleContent"] > p')
    return ", ".join(elem.string for elem in inps)
    

async def linksxyz(url: str):
    resp = rget(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    inps = soup.select('div[id="redirect-info"] > a')
    return inps[0]["href"]


async def shareus(url: str) -> str:
    DOMAIN = f"https://api.shrslink.xyz"
    code = url.split('/')[-1]
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Origin':'https://shareus.io',
    }
    api = f"{DOMAIN}/v?shortid={code}&initial=true&referrer="
    id = rget(api, headers=headers).json()['sid']
    if id:
        api_2 = f"{DOMAIN}/get_link?sid={id}"
        res = rget(api_2, headers=headers)
        if res:
            return res.json()['link_info']['destination']
        else:
            raise DDLException("Link Extraction Failed")
    else:
        raise DDLException("ID Error")     


async def dropbox(url: str) -> str:
    return (
        url.replace("www.", "")
        .replace("dropbox.com", "dl.dropboxusercontent.com")
        .replace("?dl=0", "")
    )


async def linkvertise(url: str) -> str:
    resp = rget("https://bypass.pm/bypass2", params={"url": url}).json()
    if resp["success"]:
        return resp["destination"]
    else:
        raise DDLException(resp["msg"])


async def rslinks(url: str) -> str:
    resp = rget(url, stream=True, allow_redirects=False)
    code = resp.headers["location"].split("ms9")[-1]
    try:
        return f"http://techyproio.blogspot.com/p/short.html?{code}=="
    except:
        raise DDLException("Link Extraction Failed")


async def shorter(url: str) -> str:
    try:
        cget = create_scraper().request
        resp = cget("GET", url, allow_redirects=False)
        return resp.headers["Location"]
    except:
        raise DDLException("Link Extraction Failed")


async def appurl(url: str):
    cget = create_scraper().request
    resp = cget("GET", url, allow_redirects=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.select('meta[property="og:url"]')[0]["content"]


async def surl(url: str):
    cget = create_scraper().request
    resp = cget("GET", f"{url}+")
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.select('p[class="long-url"]')[0].string.split()[1]


async def thinfi(url: str) -> str:
    try:
        return BeautifulSoup(rget(url).content, "html.parser").p.a.get("href")
    except:
        raise DDLException("Link Extraction Failed")
