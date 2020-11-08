import praw

import log_utils


client = None


def init(client_id, client_secret):
    global client
    client = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='AWS:Discord Image Extractor:0.1 (by u/xmangoslushie)'
    )

async def on_message(message, test_mode):
    submission = client.submission(url=message.content)
    if hasattr(submission, 'post_hint') and submission.post_hint == 'image':
        if test_mode:
            log_utils.get_logger(test_mode).info(f'message.channel.send({submission.url})')
        else:
            await message.channel.send(submission.url)
    else:
        log_utils.get_logger(test_mode).debug(f'DEBUG skipping non-image reddit submission {submission.id}')
