import discord
import praw
import sys
import tldextract


DISCORD_GUILD_ID = 735642741182169159  # FGO server
DISCORD_CHANNEL_ID = [
    774160071407697930,  # link-extractor-test channel
    760212029901504573,  # FGO #fanart channel
    766729741599244288,  # Genshin Impact #fanart channel
]

REDDIT_CLIENT_ID = 'mIs_r11zpS9AEg'
REDDIT_CLIENT_SECRET = 'gtGCzaPKDjkerwDHpByMU9abo4IvCA'
REDDIT_DOMAIN = 'reddit.com'
REDDIT_USER_AGENT = 'AWS:Discord Image Extractor:0.1 (by u/xmangoslushie)'

discord_client = discord.Client()
reddit_client = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return
    elif not is_valid_msg(message):
        return
    elif tldextract.extract(message.content).registered_domain == REDDIT_DOMAIN:
        await extract_images_from_reddit_submission(message)
    else:
        msg = 'not from reddit, behavior not implemented'
        print(msg)


def is_valid_msg(message):
    if message.guild.id != DISCORD_GUILD_ID:
        return False
    elif message.channel.id not in DISCORD_CHANNEL_ID:
        return False
    else:
        return True


async def extract_images_from_reddit_submission(message):
    submission = reddit_client.submission(url=message.content)
    if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
        await message.channel.send(submission.url)
    else:
        print(f'skipping non-image reddit submission {submission.id}')


# args: <Discord Token>
if len(sys.argv) != 4:
    print("Usage: main.py <Discord Token> <Reddit OAuth ID> <Reddit OAuth Secret>")
else:
    discord_client.run(sys.argv[1])
