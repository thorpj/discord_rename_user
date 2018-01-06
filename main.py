import discord, json, asyncio, os
from log_conf import logger


client = discord.Client()
#cfg_path = os.path.join(".", "config.json")


NAME = "change_nickname"
PREFIX = "!r"
commands = {}

my_user_id = "138565526799515648"
server_id = "376745782566453249"

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

def get_name(user_id):
    user = _get_user_obj(user_id)
    return user.name

def find_member(nickname, server):
    member = discord.utils.get(server.members, display_name=nickname)
    return member


async def change_nickname(nickname, user_id):
    user = _get_user_obj(user_id)
    print(user.id, user.name)
    try:
        await client.change_nickname(user, nickname)
    except discord.Forbidden:
        logger.debug("The nickname of user [name: {}, id: {}] cannot be changed: forbidden. This is most likely because they are the server owner, or this bot does not have the correct permissions to change their nickname.".format(user.name, user.id))


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
    user_id = (find_member(name, server)).id
    await change_nickname(nickname, user_id)

async def main():
    pass

@client.event
async def on_ready():
    logger.debug("Logged in as {} {}".format(client.user.name, client.user.id))
    #await main()


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    text = message.content
    if text.startswith(PREFIX):
        cmd, *args = text[2:].split()
    else:
        return
    if cmd in commands:
        await commands[cmd](message, *args)


#config = load_config(cfg_path)
token = os.environ["discord_rename_user_token"]
client.run(token)


