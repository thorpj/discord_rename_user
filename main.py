import discord, json, asyncio, os
from log_conf import logger


client = discord.Client()
#cfg_path = os.path.join(".", "config.json")


NAME = "rename_user"
PREFIX = "!r"
commands = {}

server_id = os.environ["server_id"]

def _get_server_obj(server_id):
    logger.debug(server_id)
    server = client.get_server(server_id)
    return server

def _get_user_obj(user_id):
    logger.debug(user_id)
    user = discord.Server.get_member(_get_server_obj(server_id), user_id)
    return user

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_config(path, config):
    with open(path, 'w') as f:
        f.write(json.dump(config))

def find_member(nickname, server):
    member = discord.utils.get(server.members, display_name=nickname)
    return member


async def change_nickname(message, nickname, user_id):
    user = _get_user_obj(user_id)
    server = _get_server_obj(server_id)
    owner = server.owner
    if owner == user:
        await client.send_message(message.channel, "User {} is the server owner, you can't rename them.".format(owner.display_name))
        return
    await client.change_nickname(user, nickname)



def cmd(func):
    commands[func.__name__] = func
    def dec(*args, **kwargs):
        return func(*args, **kwargs)
    return dec

@cmd
async def rename(message, name, *args):
    nickname = ' '.join(args)
    logger.debug("Nickname: {}".format(nickname))
    server = _get_server_obj(server_id)
    try:
        user_id = (find_member(name, server)).id
    except AttributeError:
        await client.send_message(message.channel, "Could not find user: {}.".format(name))
        return
    await change_nickname(message, nickname, user_id)

@cmd
async def help(message, *args):
    with open("help.txt", 'r') as f:
        help_message = f.read()
        await client.send_message(message.channel, help_message)

async def main():
    pass

@client.event
async def on_ready():
    logger.debug("Logged in as {} {}".format(client.user.name, client.user.id))
    #await main()





@client.event
async def on_message(message):
    def interpret_delimited_items(text, ignore_items, delimiter):
        items = text.split(" ")
        items = [item for item in items if item not in ignore_items]
        new_items = []
        new_item = []
        for item in items:
            if item == delimiter:
                new_items.append(' '.join(new_item))
                logger.debug(' '.join(new_item))
                new_item = []
            else:
                new_item.append(item)
        new_items.append(' '.join(new_item))
        logger.debug(1)
        return new_items


    if message.author.id == client.user.id:
        return
    text = message.content
    if text.startswith(PREFIX):
        cmd, *args = text[2:].split()
        if cmd == "rename":
            nicknames = interpret_delimited_items(text, [PREFIX, cmd], "->")
            logger.debug(nicknames)
            if len(nicknames) < 2:
                await client.send_message(message.channel, "Invalid input, see '{} help'".format(PREFIX))
                return
            current_nickname = nicknames[0]
            new_nickname = nicknames[1]
            if current_nickname == new_nickname:
                await client.send_message(message.channel, "Maybe try renaming them to something different?")
                return
            args = [current_nickname, new_nickname]
    else:
        return
    if cmd in commands:
        await commands[cmd](message, *args)


#config = load_config(cfg_path)
token = os.environ["token"]
client.run(token)


