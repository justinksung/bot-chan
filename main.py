import sys
from datetime import datetime

import discord
import pixivapi
import tldextract
from pytz import timezone, utc

import log_utils
import pixiv_utils
import reddit_utils

'''
Dockerize this on Ubuntu Server 20.04 LTS

sudo apt-get update
sudo apt install python3-pip
pip3 install configmanager discord praw pixiv-api tldextract pytz
git clone https://github.com/justinksung/bot-chan
cd bot-chan
nohup python3 main.py <args> &
'''

TEST_MODE = False
discord_client = discord.Client()


@discord_client.event
async def on_ready():
    logger.info(f'{discord_client.user} has connected to Discord!')


@discord_client.event
async def on_message(message):
    if not is_valid_guild_msg(message):
        return
    elif tldextract.extract(message.content).registered_domain == 'pixiv.net':
        logger.debug(f"routed message id={message.id} to pixiv handler")
        await pixiv_utils.on_message(message, sfw_mode())
    elif tldextract.extract(message.content).registered_domain == 'reddit.com':
        logger.debug(f"routed message id={message.id} to reddit handler")
        await reddit_utils.on_message(message, sfw_mode())
    else:
        logger.debug(f'Unsupported messsage id={message.id}')


def is_valid_guild_msg(message):
    if message.author == discord_client.user:
        return False
    elif message.guild.id != 735642741182169159:  # FGO server
        return False
    elif message.channel.id not in channels_to_subscribe():
        return False
    else:
        return True


def channels_to_subscribe():
    test_channels = [
        774160071407697930,  # Text Channels / #bot-chan-test
    ]
    live_channels = [
        760212029901504573,  # FGO / #fanart
        766729741599244288,  # Genshin Impact / #fanart
        803710798543192096,  # Priconne / #fanart
    ]
    return test_channels if TEST_MODE else live_channels


def sfw_mode(current=None):
    time = current if current is not None else datetime.now(tz=utc).astimezone(timezone('US/Pacific'))
    return 1 <= time.isoweekday() <= 5 and 7 <= time.hour < 18


if len(sys.argv) != 6:
    print("Usage: main.py <Discord Token> <Reddit OAuth ID> <Reddit OAuth Secret> <Pixiv Username> <Pixiv Password>")
else:
    log_utils.load_config()
    logger = log_utils.get_logger(TEST_MODE)

    #pixiv_utils.init(pixivapi.Client(), sys.argv[4], sys.argv[5], TEST_MODE)
    reddit_utils.init(sys.argv[2], sys.argv[3], TEST_MODE)
    discord_client.run(sys.argv[1])
