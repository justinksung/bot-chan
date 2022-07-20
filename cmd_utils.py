import re


async def on_message(message):
    msg = help(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = bakamitai(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = despacito(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = emojify(message)
    if msg is not None:
        await message.channel.send(msg)

    msg = glasses(message)
    if msg is not None:
        await message.channel.send(msg)


def help(message):
    if re.compile(r'\.help').match(message.content) is not None:
        return """ .bakamitai
.despacito
.emojify <string>
.glasses
"""
    else:
        return None


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


def glasses(message):
    if re.compile(r'\.glasses').match(message.content) is not None:
        return "Glasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly " \
               "become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the " \
               "protagonist's glasses and putting them on like, \"Haha, got your glasses!' That's just way too cute! " \
               "Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, " \
               "and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all " \
               "those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is " \
               "a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame " \
               "glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want " \
               "Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to " \
               "become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. " \
               "To. Officially. Give. Everyone. Glasses? "
    else:
        return None
