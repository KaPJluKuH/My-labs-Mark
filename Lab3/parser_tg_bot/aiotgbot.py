import logging

from crud_api import CrudApi
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *
import re
import json

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5043924535:AAG329Xbr5vly1_8RyToMxZsblookuJWQvg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

###
START_BUTTON_NAME = "start"
RUN_PARSE_BUTTON_NAME = "Run parse"

GET_BUTTON_NAME = "get_by_id"

SELECT_BUTTON_NAME = "Select"
SELECT_RANGE_NAME = "select_range"
SELECT_ALL_BUTTON_NAME = "Select all"

#DELETE_BUTTON_NAME = "Delete"
DELETE_RANGE_NAME = "delete_range"
TRUNCATE_BUTTON_NAME = "Truncate"
DELETE_BY_ID = "Delete by id"

UPDATE_BUTTON_NAME = "Update"
INSERT_BUTTON_NAME = "Insert"
###

default_kb_markup = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text=RUN_PARSE_BUTTON_NAME)],
        [KeyboardButton(text=SELECT_BUTTON_NAME)],  # by id/ all
        [KeyboardButton(text=DELETE_RANGE_NAME)],
        #[KeyboardButton(text=DELETE_BUTTON_NAME)],  # by id/ by range/ truncate
        [KeyboardButton(text=UPDATE_BUTTON_NAME)],
        [KeyboardButton(text=INSERT_BUTTON_NAME)]
    ]
)


@dp.message_handler(commands=[START_BUTTON_NAME])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nChoose operation", reply_markup=default_kb_markup)



# select handlers
# @dp.message_handler(commands=[SELECT_BUTTON_NAME])
# async def origin_select_btn_handler(message: types.Message):
#     result_markup = ReplyKeyboardMarkup([
#         [KeyboardButton(text=SELECT_RANGE_NAME)],
#         [KeyboardButton(text=SELECT_ALL_BUTTON_NAME)]
#     ])
#
#     await message.reply(text="Choose select query type", reply_markup=result_markup)

@dp.message_handler(commands=[GET_BUTTON_NAME])
async def origin_get_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + GET_BUTTON_NAME, "", m)
    result = CrudApi.get_by_id(int(m))
    await message.reply(result)


@dp.message_handler(commands=[SELECT_RANGE_NAME])
async def origin_select_by_id_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + SELECT_RANGE_NAME, "", m)
    m = re.sub(r'/s+', "", m)
    result = CrudApi.select_range(m.split(","))
    await message.reply(result)


@dp.message_handler(commands=[SELECT_ALL_BUTTON_NAME])
async def origin_select_all_btn_handler(message: types.Message):
    pass


@dp.message_handler(commands=[DELETE_RANGE_NAME])
async def origin_delete_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + DELETE_RANGE_NAME, "", m)
    m = re.sub(r'/s+', "", m)
    result = CrudApi.delete_range(m.split(","))
    result = json.loads(result)
    await message.reply(result.get('status'))

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text="Press start",
#                          reply_markup=ReplyKeyboardMarkup(keyboard=[
#                              [KeyboardButton(text="/start")]
#                          ]))


@dp.message_handler(commands=[UPDATE_BUTTON_NAME])
async def origin_update_btn_handler(message: types.Message):
    pass


@dp.message_handler(commands=[INSERT_BUTTON_NAME])
async def origin_insert_btn_handler(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
