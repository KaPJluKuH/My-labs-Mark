import logging

from crud_api import CrudApi
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *
import re
import json
from Lab3.StopGameParser import parser

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5043924535:AAG329Xbr5vly1_8RyToMxZsblookuJWQvg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


#класс для описания состояния общения с пользователем
class Mydialog(StatesGroup):
    get_otvet = State()
    select_otvet = State()
    insert_otvet = State()
    delete_otvet = State()
    update_otvet = State()


#Комманды
START_BUTTON_NAME = "start"

GET_BUTTON_NAME = "get_by_id"
SELECT_RANGE_NAME = "select_range"
UPDATE_BUTTON_NAME = "update_row"
INSERT_BUTTON_NAME = "insert_row"
DELETE_RANGE_NAME = "delete_range"

#Интерфейс+общение
START_BUTTON_NAME_INT = "Бот"

RUN_PARSE_BUTTON_NAME = "Парсинг страницы"

SELECT_BUTTON_NAME = "Искать"
SELECT_BUTTON_NAME_GET = "Искать по одному id"
SELECT_BUTTON_NAME_MANY = "Искать по нескольким id"
INSERT_BUTTON_NAME_INT = "Добавить"
UPDATE_BUTTON_NAME_INT = "Обновить"
DELETE_BUTTON_NAME = "Удалить"


default_kb_markup = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text=RUN_PARSE_BUTTON_NAME),
        KeyboardButton(text=SELECT_BUTTON_NAME),
        KeyboardButton(text=INSERT_BUTTON_NAME_INT),
        KeyboardButton(text=UPDATE_BUTTON_NAME_INT),
        KeyboardButton(text=DELETE_BUTTON_NAME)]
    ], resize_keyboard=True
)


@dp.message_handler(commands=[START_BUTTON_NAME])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nСделай свой выбор, жалкий человечишка!", reply_markup=default_kb_markup)


#Общение
@dp.message_handler(lambda message: message.text == RUN_PARSE_BUTTON_NAME)
async def origin_parse_handler(message: types.Message):
    parser.main_parser()
    await message.reply("Парсинг выполнен!")


#Выбор поиска
@dp.message_handler(lambda message: message.text == SELECT_BUTTON_NAME)
async def origin_select_btn_handler(message: types.Message):
    select_kb_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=SELECT_BUTTON_NAME_GET),
            KeyboardButton(text=SELECT_BUTTON_NAME_MANY)]
        ], resize_keyboard=True
    )
    await message.reply(text="Выберите какой тип поиска вас интересует:", reply_markup=select_kb_markup)


#Поиск по одному
@dp.message_handler(lambda message: message.text == SELECT_BUTTON_NAME_GET)
async def catch_id_get(message: types.Message, state: FSMContext):
    await Mydialog.get_otvet.set()
    await message.answer(text="Введите id по которому хотите найти запись в базе:")


@dp.message_handler(state=Mydialog.get_otvet)
async def process_message_get(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].strip()
        result = CrudApi.get_by_id(int(user_message))
        for res in result:
            title = res[0]
            data = res[1]
            link = res[2]
            bs64 = res[3]
            await message.reply(title + '\n' + data + '\n' + link + '\n' + bs64, reply_markup=default_kb_markup)
        # await message.reply("Время сделать еще выбор!", reply_markup=default_kb_markup)
    await state.finish()


#Поиск нескольких
@dp.message_handler(lambda message: message.text == SELECT_BUTTON_NAME_MANY)
async def catch_id_select(message: types.Message, state: FSMContext):
    await Mydialog.select_otvet.set()
    await message.answer(text="Введите список id по которым хотите найти запись в базе. Например: 1, 2, 3")


@dp.message_handler(state=Mydialog.select_otvet)
async def process_message_select(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].strip()
        result = CrudApi.select_range(user_message.split(","))
        for res in result:
            title = res[0]
            data = res[1]
            link = res[2]
            bs64 = res[3]
            await message.reply(title + '\n' + data + '\n' + link + '\n' + bs64, reply_markup=default_kb_markup)
        # await message.reply("Время сделать еще выбор!", reply_markup=default_kb_markup)
    await state.finish()


#Заполнение
@dp.message_handler(lambda message: message.text == INSERT_BUTTON_NAME_INT)
async def catch_id_insert(message: types.Message, state: FSMContext):
    await Mydialog.insert_otvet.set()
    await message.answer(text="Введите ваши данные в следующем обязательном порядке -> \n"
                              "Заголовок, Дата, Ссылка, src, base64 изображения")


@dp.message_handler(state=Mydialog.insert_otvet)
async def process_message_insert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].strip()
        result = CrudApi.insert_row(user_message.split(","))

        await message.reply("Ваша сзапись добавлена в базу. Найти её вы можете через поиск по последнему id.")

    await state.finish()


#Обновление
@dp.message_handler(lambda message: message.text == UPDATE_BUTTON_NAME_INT)
async def catch_id_update(message: types.Message, state: FSMContext):
    await Mydialog.update_otvet.set()
    await message.answer(text="Введите данные для обновления в следующем формате -> \n"
                              " id $ Колонки на выбор (title, date, link, src, base64) $ Данные последовательно как колонки \n"
                              "Пример: 000 $ title,data $ Заголовок, 00.00.0000")


@dp.message_handler(state=Mydialog.update_otvet)
async def process_message_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].strip().split('$')
        id = user_message[0].strip()
        cols = user_message[1].strip().split(",")
        vals = user_message[2].strip().split(",")
        result = CrudApi.update_row(id, cols, vals)
        await message.reply("Запись в таблице обновлена. Можете проверить через поиск по id строки.")

    # Finish conversation
    await state.finish()

#Удаление
@dp.message_handler(lambda message: message.text == DELETE_BUTTON_NAME)
async def catch_id_delete(message: types.Message, state: FSMContext):
    await Mydialog.delete_otvet.set()
    await message.answer(text="Введите (id/список id) по (которому/которым) хотите удалить данные в базе:")


@dp.message_handler(state=Mydialog.delete_otvet)
async def process_message_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text'].strip()
        result = CrudApi.delete_range(user_message.split(","))
        result = json.loads(result)
        await message.reply(result.get('status'))

    await state.finish()


#Работа с командами
#Поиск по одному
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


#Поиск нескольких
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


#Заполнение
@dp.message_handler(commands=[INSERT_BUTTON_NAME])
async def origin_insert_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + INSERT_BUTTON_NAME, "", m)
    m = m.strip()
    result = CrudApi.insert_row(m.split(","))
    await message.reply("Ваша сзапись добавлена в базу. Найти её вы можете через поиск по последнему id.")


#Обновление
@dp.message_handler(commands=[UPDATE_BUTTON_NAME])
async def origin_update_btn_handler(message: types.Message):
    m = message.text.strip()
    #/update_row  456 $ title,date $ DARKSOULS III,2017
    m = re.sub("/" + UPDATE_BUTTON_NAME, "", m)
    m = m.split('$')
    id = m[0].strip()
    cols = m[1].strip().split(",")
    vals = m[2].strip().split(",")
    result = CrudApi.update_row(id, cols, vals)
    await message.reply("Запись в таблице обновлена. Можете проверить через поиск по id строки.")


#Удаление
@dp.message_handler(commands=[DELETE_RANGE_NAME])
async def origin_delete_btn_handler(message: types.Message):
    m = message.text.strip()
    m = re.sub("/" + DELETE_RANGE_NAME, "", m)
    m = m.strip()
    result = CrudApi.delete_range(m.split(","))
    result = json.loads(result)
    await message.reply(result.get('status'))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
