import discord
import pathlib
import pixivapi
import praw
import sys
import tempfile
import tldextract
import uuid
from urllib.parse import urlparse

'''
Dockerize this on Ubuntu Server 20.04 LTS

sudo apt-get update
sudo apt install python3-pip
pip3 install discord praw pixiv-api tldextract 
git clone https://github.com/justinksung/bot-chan
nohup bot-chan main.py <args> &
'''

DISCORD_GUILD_ID = 735642741182169159  # FGO server
DISCORD_CHANNEL_ID = [
    #774160071407697930,  # bot-chan-test channel
    760212029901504573,  # FGO #fanart channel
    766729741599244288,  # Genshin Impact #fanart channel
]

REDDIT_DOMAIN = 'reddit.com'
REDDIT_USER_AGENT = 'AWS:Discord Image Extractor:0.1 (by u/xmangoslushie)'

discord_client = discord.Client()
pixiv_client = pixivapi.Client()
pixiv_refresh_token = None
reddit_client = None


@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return
    elif not is_valid_guild_msg(message):
        return
    elif tldextract.extract(message.content).registered_domain == 'pixiv.net':
        await on_pixiv_message(message)
    elif tldextract.extract(message.content).registered_domain == 'reddit.com':
        await on_reddit_message(message)
    else:
        msg = 'not from reddit, behavior not implemented'
        print(msg)


def is_valid_guild_msg(message):
    if message.guild.id != DISCORD_GUILD_ID:
        return False
    elif message.channel.id not in DISCORD_CHANNEL_ID:
        return False
    else:
        return True


def pixiv_authenticate(username, password):
    pixiv_client.login(username, password)
    return pixiv_client.refresh_token


async def on_pixiv_message(message):
    path = urlparse(message.content).path.split("/")
    type = path[-2]
    id = int(path[-1])
    if type == 'artworks':
        try:
            illustration = pixiv_client.fetch_illustration(id)
        except pixivapi.LoginError:
            pixiv_client.login(sys.argv[4], sys.argv[5])
            illustration = pixiv_client.fetch_illustration(id)

        sizes = illustration.image_urls.keys()
        size_to_download = None
        if pixivapi.Size.MEDIUM in sizes:
            size_to_download = pixivapi.Size.MEDIUM
        elif pixivapi.Size.LARGE in sizes:
            size_to_download = pixivapi.Size.LARGE
        elif pixivapi.Size.ORIGINAL in sizes:
            size_to_download = pixivapi.Size.ORIGINAL

        if size_to_download is not None:
            with tempfile.TemporaryDirectory() as temp_dirname:
                temp_dirpath = pathlib.Path(temp_dirname)
                temp_filename = str(uuid.uuid4())
                illustration.download(temp_dirpath, filename=temp_filename)

                temp_filepath = None
                for x in temp_dirpath.iterdir():
                    temp_filepath = x
                    break
                print(f'downloaded illustration {id} to {temp_filepath}')

                f = open(temp_filepath)

                to_send = discord.File(temp_filepath)
                await message.channel.send(file=to_send)
        else:
            print(f'DEBUG illustration id={id} has no appropriate sizes image_urls={illustration.image_urls}')
    else:
        print(f'DEBUG skipping non-illustration pixiv model type={type} id={id}')


async def on_reddit_message(message):
    submission = reddit_client.submission(url=message.content)
    if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
        await message.channel.send(submission.url)
    else:
        print(f'DEBUG skipping non-image reddit submission {submission.id}')


if len(sys.argv) != 6:
    print("Usage: main.py <Discord Token> <Reddit OAuth ID> <Reddit OAuth Secret> <Pixiv Username> <Pixiv Password>")
else:
    reddit_client = praw.Reddit(
        client_id=sys.argv[2],
        client_secret=sys.argv[3],
        user_agent=REDDIT_USER_AGENT
    )
    pixiv_client.login(sys.argv[4], sys.argv[5])
    discord_client.run(sys.argv[1])
