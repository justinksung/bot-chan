import pathlib
import tempfile
import uuid
from urllib.parse import urlparse

import discord
import pixivapi

import log_utils

client = None
refresh_token = None
logger = None
test_mode = False


def init(pixiv_client, username, password, test_md):
    pixiv_client.login(username, password)

    global client
    client = pixiv_client
    global refresh_token
    refresh_token = pixiv_client.refresh_token
    global logger
    logger = log_utils.get_logger(test_md)
    global test_mode
    test_mode = test_md


def authenticate():
    global refresh_token
    client.authenticate(refresh_token)
    logger.debug(f'replacing old refresh token')
    refresh_token = client.refresh_token


async def on_message(message):
    path = urlparse(message.content).path.split("/")
    type = path[-2]
    id = int(path[-1])
    if type == 'artworks':
        try:
            logger.info(f'fetching artwork id={id}')
            illustration = client.fetch_illustration(id)
        except Exception as e:
            logger.info(f're-attempting fetch of artwork id={id} because of error="{e}"')
            authenticate()
            illustration = client.fetch_illustration(id)
        if illustration is None:
            raise Exception("could not fetching artwork id={id}")

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
                illustration.download(temp_dirpath, size=size_to_download, filename=temp_filename)

                temp_filepath = None
                for x in temp_dirpath.iterdir():
                    temp_filepath = x
                    break
                logger.debug(f'downloaded illustration {id} to {temp_filepath}')

                if test_mode:
                    logger.info(f'message.channel.send(file={temp_filepath})')
                else:
                    to_send = discord.File(temp_filepath)
                    await message.channel.send(file=to_send)
        else:
            logger.debug(
                f'DEBUG illustration id={id} has no appropriate sizes image_urls={illustration.image_urls}')
    else:
        logger.debug(f'DEBUG skipping non-illustration pixiv model type={type} id={id}')
