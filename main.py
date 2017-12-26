import discord, json, asyncio, os
from log_conf import logger


client = discord.Client()
cfg_path = os.path.join(".", "config.json")


NAME = "rename_joe"
my_user_id = "138565526799515648"
server_id = "355703346029527050"

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

def set_name(prefix, user_id):
    name = "{} Joe".format(prefix)
    user = _get_user_obj(user_id)
    client.change_nickname(user, name)
    return name




def main():


config = load_config(cfg_path)
client.run(config["token"])

main()

