from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig
from uvloop import install

install()
basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s", #  [%(filename)s:%(lineno)d]
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

LOGGER = getLogger(__name__)

load_dotenv('config.env', override=True)

class Config:
    BOT_TOKEN=getenv('BOT_TOKEN', '')
    TG_API_HASH=getenv('TG_API_HASH', '')
    TG_API_ID=getenv('TG_API_ID', '')
    if BOT_TOKEN == '' or TG_API_HASH == '' or TG_API_ID == '':
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

Bypass = Client("FZ", api_id=Config.TG_API_ID, api_hash=Config.TG_API_HASH, bot_token=Config.BOT_TOKEN)
