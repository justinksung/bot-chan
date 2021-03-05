import re


async def on_message(message):
    msg = bakamitai(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = despacito(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = emojify(message)
    if msg is not None:
        await message.channel.send(msg)


def bakamitai(message):
    if re.compile(r'\.bakamitai').match(message.content) is not None:
        return "https://www.youtube.com/watch?v=MJbE3uWN9vE"
    else:
        return None


def despacito(message):
    if re.compile(r'\.despacito').match(message.content) is not None:
        return "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    else:
        return None


def emojify(message):
    if re.compile(r'\.emojify').match(message.content) is not None:
        emojified = ""
        for char in re.compile('(?<=\.emojify )\w+').search(message.content).group().lower():
            emojified += ':regional_indicator_' + char + ':'
        return emojified
    else:
        return None
