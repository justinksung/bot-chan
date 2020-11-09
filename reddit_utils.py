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


async def on_message(message):
    submission = client.submission(url=message.content)
    if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
        if test_mode:
            logger.info(f'message.channel.send({submission.url})')
        else:
            await message.channel.send(submission.url)
    else:
        logger.debug(f'DEBUG skipping non-image reddit submission {submission.id}')
