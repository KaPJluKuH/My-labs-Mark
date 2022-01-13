import logging

from crud_api import CrudApi
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *
import re
import json
from Lab3.StopGameParser import parser

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5043924535:AAG329Xbr5vly1_8RyToMxZsblookuJWQvg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

###
START_BUTTON_NAME = "start"
RUN_PARSE_BUTTON_NAME = "Run parse"

GET_BUTTON_NAME = "get_by_id"

SELECT_BUTTON_NAME = "Искать"
SELECT_RANGE_NAME = "select_range"
SELECT_ALL_BUTTON_NAME = "Select all"

#DELETE_BUTTON_NAME = "Delete"
DELETE_RANGE_NAME = "delete_range"
TRUNCATE_BUTTON_NAME = "Truncate"
# DELETE_BY_ID = "Delete by id"

UPDATE_BUTTON_NAME = "update_row"
INSERT_BUTTON_NAME = "insert_row"

###

default_kb_markup = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text=RUN_PARSE_BUTTON_NAME)],
        [KeyboardButton(text=SELECT_BUTTON_NAME)],  # by id/ all
        [KeyboardButton(text=DELETE_RANGE_NAME)],
        # [KeyboardButton(text=DELETE_BUTTON_NAME)],  # by id/ by range/ truncate
        [KeyboardButton(text=UPDATE_BUTTON_NAME)],
        [KeyboardButton(text=INSERT_BUTTON_NAME)]
    ]
)


@dp.message_handler(commands=[START_BUTTON_NAME])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nChoose operation", reply_markup=default_kb_markup)


@dp.message_handler(lambda message: message.text == RUN_PARSE_BUTTON_NAME)
async def origin_parse_handler(message: types.Message):
    parser.main_parser()
    await message.reply("Парсинг выполнен!")


# select handlers
@dp.message_handler(lambda message: message.text == SELECT_BUTTON_NAME)
async def origin_select_btn_handler(message: types.Message):
    select_kb_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Искать по одному id")],
            [KeyboardButton(text="Искать по нескольким id")]
        ]
    )
    await message.reply(text="Выберите какой тип поиска вас интересует:", reply_markup=select_kb_markup)


# @dp.message_handler(lambda message: message.text == "Искать по одному id")
# async def origin_answer_get_btn_handler(message: types.Message):
#     await message.reply(text="Введите id", reply=False)



# @dp.message_handler(lambda message: message.text == "Искать по нескольким id")
# async def origin_select_btn_handler(message: types.Message):
#
#     await message.reply(text="Ваш запрос выдан") and json.dumps(res)


@dp.message_handler(commands=[GET_BUTTON_NAME])
async def origin_get_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + GET_BUTTON_NAME, "", m)
    m = m.strip()
    result = CrudApi.get_by_id(int(m))
    for res in result:
        title = res[0]
        data = res[1]
        link = res[2]
        bs64 = res[3]
        await message.reply(title+'\n'+data+'\n'+link+'\n'+bs64)


@dp.message_handler(commands=[SELECT_RANGE_NAME])
async def origin_select_by_id_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + SELECT_RANGE_NAME, "", m)
    m = m.strip()
    result = CrudApi.select_range(m.split(","))
    for res in result:
        title = res[0]
        data = res[1]
        link = res[2]
        bs64 = res[3]
        await message.reply(title+'\n'+data+'\n'+link+'\n'+bs64)


@dp.message_handler(commands=[DELETE_RANGE_NAME])
async def origin_delete_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + DELETE_RANGE_NAME, "", m)
    m = m.strip()
    result = CrudApi.delete_range(m.split(","))
    result = json.loads(result)
    await message.reply(result.get('status'))


@dp.message_handler(commands=[INSERT_BUTTON_NAME])
async def origin_insert_btn_handler(message: types.Message):
    m = message.text.strip()
    # print(m)
    m = re.sub("/" + INSERT_BUTTON_NAME, "", m)
    # print(m)
    m = m.strip()
    # print(m)
    result = CrudApi.insert_row(m.split(","))
    # print(result)
    await message.reply("Ваша сзапись добавлена в базу. Найти её вы можете через поиск по последнему id.")


@dp.message_handler(commands=[UPDATE_BUTTON_NAME])
async def origin_update_btn_handler(message: types.Message):
    m = message.text.strip()
    #/update_row  456 $ title,data $ DARKSOULS III,2017
    m = re.sub("/" + UPDATE_BUTTON_NAME, "", m)
    m = m.split('$')
    id = m[0].strip()
    cols = m[1].strip().split(",")
    vals = m[2].strip().split(",")
    result = CrudApi.update_row(id, cols, vals)
    await message.reply("Запись в таблице обновлена. Можете проверить через поиск по id строки.")
# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text="Press start",
#                          reply_markup=ReplyKeyboardMarkup(keyboard=[
#                              [KeyboardButton(text="/start")]
#                          ]))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
