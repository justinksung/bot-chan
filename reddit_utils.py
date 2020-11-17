import praw

import log_utils

client = None
logger = None
test_mode = False


def init(client_id, client_secret, test_md):
    global client
    client = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='AWS:Discord Image Extractor:0.1 (by u/xmangoslushie)'
    )
    global logger
    logger = log_utils.get_logger(test_md)
    global test_mode
    test_mode = test_md


async def on_message(message, sfw_override):
    submission = client.submission(url=message.content)
    tag_spoiler = sfw_override or submission.over_18

    if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
        msg = submission.url
        if tag_spoiler:
            msg = '||' + msg + '||'
        await message.channel.send(msg)
    else:
        logger.debug(f'DEBUG skipping non-image reddit submission {submission.id}')
