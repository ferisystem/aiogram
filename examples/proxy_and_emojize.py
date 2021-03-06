import asyncio
import logging

import aiohttp

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.executor import start_polling
from aiogram.utils.markdown import bold, code, italic, text

# Configure bot here
API_TOKEN = 'BOT TOKEN HERE'
PROXY_URL = 'http://PROXY_URL'  # Or 'socks5://...'

# If authentication is required in your proxy then uncomment next line and change login/password for it
# PROXY_AUTH = aiohttp.BasicAuth(login='login', password='password')
# And add `proxy_auth=PROXY_AUTH` argument in line 25, like this:
# >>> bot = Bot(token=API_TOKEN, loop=loop, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
# Also you can use Socks5 proxy but you need manually install aiohttp_socks package.

# Get my ip URL
GET_IP_URL = 'http://bot.whatismyipaddress.com/'

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, proxy=PROXY_URL)
dp = Dispatcher(bot)


async def fetch(url, proxy=None, proxy_auth=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy, proxy_auth=proxy_auth) as response:
            return await response.text()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    content = []

    # Make request (without proxy)
    ip = await fetch(GET_IP_URL)
    content.append(text(':globe_showing_Americas:', bold('IP:'), code(ip)))
    # This line is formatted to '🌎 *IP:* `YOUR IP`'

    # Make request through proxy
    ip = await fetch(GET_IP_URL, bot.proxy, bot.proxy_auth)
    content.append(text(':locked_with_key:', bold('IP:'), code(ip), italic('via proxy')))
    # This line is formatted to '🔐 *IP:* `YOUR IP` _via proxy_'

    # Send content
    await bot.send_message(message.chat.id, emojize(text(*content, sep='\n')), parse_mode=ParseMode.MARKDOWN)

    # In this example you can see emoji codes: ":globe_showing_Americas:" and ":locked_with_key:"
    # You can find full emoji cheat sheet at https://www.webpagefx.com/tools/emoji-cheat-sheet/
    # For representing emoji codes into real emoji use emoji util (aiogram.utils.emoji)
    # (you have to install emoji module)

    # For example emojize('Moon face :new_moon_face:') is transformed to 'Moon face 🌚'


if __name__ == '__main__':
    start_polling(dp, loop=loop, skip_updates=True)
