import discord
import asyncio
import async_timeout
import aiohttp
import json

client = discord.Client()
session = aiohttp.ClientSession()


PRIVATE_KEYS = json.load(open('keys.json'))


@client.event
async def on_ready():
    print('WURMBOT: logged in as ' + client.user.name + ' (' + client.user.id + ')')
    ch = client.get_all_channels()

    client.send_message("WURMBOT logged in")
    print('-----------------------')

    print('invite me to the server using: https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(PRIVATE_KEYS['client_id']))


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            st = response.status
            body = await response.text()
            return (st, body)


async def getip(channel):
    status, text, = await fetch(session, 'http://ipinfo.io/json')
    if status == 200:
        print(text)
        js = json.loads(text)
        await client.send_message(channel, 'The server is currently at ' + js['ip'])


async def dispatch_message(msg):
    # print('got message: ' + msg)
    s = msg.content.lstrip().rstrip().split()
    print(s)

    if len(s) == 1:
        await client.send_message(msg.channel, 'I need an argument. See `!wb help` for details.')
    elif s[1] == 'ip':
        await getip(msg.channel)
    elif s[1] == 'help':
        await client.send_message(msg.channel, 'All commands start with `!wb `. Valid commands: `help`, `ip`')
    elif s[1] == 'invite':
        await client.send_message(msg.channel, 'https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(PRIVATE_KEYS['client_id']))
    else:
        await client.send_message(msg.channel, 'Command not implemented. See `!wb help` for details.')


@client.event
async def on_message(message):
    if message.content.startswith('!wb ') or message.content == '!wb':
        await dispatch_message(message)

    elif message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit = 100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages'.format(counter))

client.run(PRIVATE_KEYS['token'])
