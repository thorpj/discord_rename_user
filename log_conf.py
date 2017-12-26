import logging, sys

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(funcName)s():%(lineno)s:: %(message)s')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

printout = logging.StreamHandler(sys.stdout)
printout.setLevel(logging.DEBUG)
printout.setFormatter(formatter)
logger.addHandler(printout)

