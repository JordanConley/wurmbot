import discord
import asyncio
import async_timeout
import aiohttp
import json

client = discord.Client()
session = aiohttp.ClientSession()

PRIVATE_KEYS = {}

try:
    f = open('keys.json')
    PRIVATE_KEYS = json.load(f)
    assert PRIVATE_KEYS.__contains__('client_id')
    assert PRIVATE_KEYS.__contains__('client_secret')
    assert PRIVATE_KEYS.__contains__('token')
except FileNotFoundError:
    print('ERROR: key file `keys.json` does not exist.')
    exit(-1)
except (json.JSONDecodeError, AssertionError):
    print('ERROR: key file `keys.json` is invalid.')
    exit(-1)

INVITE_LINK = 'https://discordapp.com/api/oauth2/authorize?client_id=%s&scope=bot&permissions=0' % PRIVATE_KEYS['client_id']

@client.event
async def on_ready():
    print('WURMBOT: logged in as ' + client.user.name + ' (' + client.user.id + ')')
    ch = client.get_all_channels()


    client.send_message("WURMBOT logged in")
    print('invite me to the server using: ' + INVITE_LINK)
    print('-----------------------')


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            st = response.status
            body = await response.text()
            return (st, body)


async def get_ip(channel):
    status, text, = await fetch(session, 'http://ipinfo.io/json')
    if status == 200:
        print(text)
        js = json.loads(text)
        await client.send_message(channel, 'The server is currently at `' + js['ip'] + '`')


async def dispatch_message(msg):
    # print('got message: ' + msg)
    s = msg.content.lstrip().rstrip().split()

    if len(s) == 1:
        await client.send_message(msg.channel, 'Give me a command, fam. See `!wb help` for details.')
    elif s[1] == 'bully':
        await client.send_message(msg.channel, ''.join([':regional_indicator_' + x + ':' for x in "cease"]) + ' :gun:')
    elif s[1] == 'ip':
        await get_ip(msg.channel)
    elif s[1] == 'help':
        commandlist= '`' + '`, `'.join(['help', 'ip', 'invite']) + '`'
        await client.send_message(msg.channel, 'All commands start with `!wb `. Valid commands: ' + commandlist)
    elif s[1] == 'invite':
        await client.send_message(msg.channel, INVITE_LINK)
    else:
        await client.send_message(msg.channel, 'Command not implemented. See `!wb help` for details.')


@client.event
async def on_message(message):
    if message.content.startswith('!wb ') or message.content == '!wb':
        await dispatch_message(message)


client.run(PRIVATE_KEYS['token'])
