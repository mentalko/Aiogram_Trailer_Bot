import os
from typing import List
import requests
import re
import logging

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, WEBHOOK_URL
import tmdb_helper
import telegraph_helper

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from youtubesearchpython import VideosSearch
# import concatenate as conc

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


#https://youtube-scrape.herokuapp.com/api/search?q=It%20takes%20two
def get_video_url(title):
    res = VideosSearch(title, limit = 1).result()
    return res["result"][0]["link"]
    
def prepare_page_data(name_list) -> List[dict]:
    title_and_links = []
    for title in name_list:
        if '/' in title:
            title = title.split('/')[1].strip()
            url = get_video_url(title)
            title_and_links.append({'title': title, 'url': url})
            
    print(title_and_links)
    return title_and_links  


@dp.message_handler(lambda message: message.text.startswith('Фильм на'))
async def movies_list(message):
    try:
        print(message.text)
        question = message.text.split("\n")[0]
        movie_titles = message.text.split("\n")[1:]

        await bot.send_poll(message.from_user.id, question, movie_titles,
                            is_anonymous=False,
                            allows_multiple_answers=True,
                            type='regular'
                            )
        tmdb_helper.get_large_poster([title.split("/")[1].strip() for title in movie_titles if '/' in title])
        post_link = telegraph_helper.create_page(prepare_page_data(movie_titles))
        await bot.send_message(message.chat.id, "<a href='{}'>Ссылка на трейлеры</a>".format(post_link),parse_mode='HTML')
    except Exception as e:
        await message.answer(e)
        


@dp.message_handler (content_types=['poll'])
async def handle_poll (message):   
    try:
        movie_titles = [ x.text for x in message.poll.options]
        tmdb_helper.get_large_poster([title.split("/")[1].strip() for title in movie_titles if '/' in title])
        post_link = telegraph_helper.create_page(prepare_page_data(movie_titles))
        print(post_link)
        await message.answer("<a href='{}'>Ссылка на трейлеры</a>".format(post_link),parse_mode='HTML')
        
    
    except Exception as e:
        await message.answer(e)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Hello, I'm Trailer Bot v2.1! \n\n It's the same bot, but completely rewritten\nand running much faster than ever!")

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    
async def on_shutdown(dispatcher):
    await bot.delete_webhook()


    
    
if 'ON_HEROKU' in os.environ:
    executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 5000))
)
else:
    if __name__ == '__main__':
        executor.start_polling(dispatcher=dp)
