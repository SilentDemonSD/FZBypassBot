from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
from logging import getLogger, FileHandler, StreamHandler, INFO, ERROR, basicConfig
from uvloop import install

install()
basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s", #  [%(filename)s:%(lineno)d]
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

getLogger("pyrogram").setLevel(ERROR)
LOGGER = getLogger(__name__)

load_dotenv('config.env', override=True)

class Config:
    BOT_TOKEN=getenv('BOT_TOKEN', '')
    API_HASH=getenv('API_HASH', '')
    API_ID=getenv('API_ID', '')
    if BOT_TOKEN == '' or API_HASH == '' or API_ID == '':
        LOGGER.critical('ENV Missing. Exiting Now...')
        exit(1)
    LARAVEL_SESSION=""
    XSRF_TOKEN=""
    GDTOT_CRYPT=""
    D_CRYPT=""
    K_CRYPT=""
    H_CRYPT=""
    KAT_CRYPT=""
    UPTOBOX_TOKEN=""
    TERA_COOKIE=""
    CF_COOKIE=""

Bypass = Client("FZ", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, plugins=dict(root="FZBypass/plugins"))
