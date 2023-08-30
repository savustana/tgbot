from datetime import datetime
import logging, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram. dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram. types import InlineKeyboardMarkup, InlineKeyboardButton
from States import *


TOKEN = os.getenv("6599339456:AAHy2QsvDzNkhyAp0Uz-o35b_20pifui0Z8")
logging.basicConfig(level=logging. INFO)
bot = Bot(token='6599339456:AAHy2QsvDzNkhyAp0Uz-o35b_20pifui0Z8')
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = []


def baza1():
    baza = dict()
    with open("bot.txt", "r") as bb:
        for i in bb.readlines():
            if i == "\n":
                continue
            else:
                s =i.split(":")
                baza.update({s[0] : s[1]})
    return baza


local_dt = datetime.now()



@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    words_choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text = "Today's date", callback_data = 'today')
    words_choice.add(button)
    button1 = InlineKeyboardButton(text='Choose date', callback_data='choose')
    words_choice.add(button1)
    button1 = InlineKeyboardButton(text='Add event', callback_data='add')
    words_choice.add(button1)
    await message.answer(text="Hello! I'm Event-Bot 2023!\nWhat do you want to do?", reply_markup=words_choice)
    await States.begin.set()
@dp.callback_query_handler(state=States.begin)
async def menu(callback_query: types.CallbackQuery, state: FSMContext):
    baza=baza1()
    words_choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Today's date", callback_data='today')
    words_choice.add(button)
    button1 = InlineKeyboardButton(text='Choose date', callback_data='choose')
    words_choice.add(button1)
    button1 = InlineKeyboardButton(text='Add event', callback_data='add')
    words_choice.add(button1)
    if callback_query.data == 'today':
        if str(local_dt.day) + '.' + str(local_dt.month) in baza:
            await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                         message_id=callback_query.message.message_id
                                         , text=f'{str(local_dt.day) + "." + str(local_dt.month)}\n{baza[str(local_dt.day) + "." + str(local_dt.month)]}',
                                         reply_markup = words_choice)
        else:
            await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                         message_id=callback_query.message.message_id
                                         , text='Event not found(',
                                         reply_markup=words_choice)
        await state.finish()
        await States.begin.set()
    elif callback_query.data == 'choose':
        await bot.send_message(callback_query.message.chat.id,'Enter date \n(for example: 16.3): ')
        await state.finish()
        await States.choose.set()
    elif callback_query.data == 'add':
        await callback_query.answer('add')
        await bot.send_message(callback_query.message.chat.id,
                               "Enter date (for example: 16.3) and event\n(for example: 16.5, My Birthday): ")


        await state.finish()
        await States.add.set()
@dp.message_handler(state=States.choose)
async def choose(message: types.Message, state: FSMContext):
    baza = baza1()
    await state.finish()
    if message.text in baza:
        await message.answer(f"{message.text} 's event:\n{baza[message.text]}")
        words_choice = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Today's date", callback_data='today')
        words_choice.add(button)
        button1 = InlineKeyboardButton(text='Choose date', callback_data='choose')
        words_choice.add(button1)
        button1 = InlineKeyboardButton(text='Add event', callback_data='add')
        words_choice.add(button1)
        await message.answer(text="Hello! I'm Event-Bot 2023!\nWhat do you want to do?", reply_markup=words_choice)
        await States.begin.set()
    else:
        await message.answer(f'Event not found(')
        words_choice = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Today's date", callback_data='today')
        words_choice.add(button)
        button1 = InlineKeyboardButton(text='Choose date', callback_data='choose')
        words_choice.add(button1)
        button1 = InlineKeyboardButton(text='Add event', callback_data='add')
        words_choice.add(button1)
        await message.answer(text="Hello! I'm Event-Bot 2023!\nWhat do you want to do?", reply_markup=words_choice)
        await States.begin.set()


@dp.message_handler(state=States.add)
async def add(message: types.Message, state: FSMContext):
    baza = baza1()
    ans = message.text.split(",")
    with open("bot.txt", "a") as bb:
        bb.write("\n"+ans[0]+":"+ans[1])
    

    await message.answer(text = "Event successfully added!")
    words_choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Today's date", callback_data='today')
    words_choice.add(button)
    button1 = InlineKeyboardButton(text='Choose date', callback_data='choose')
    words_choice.add(button1)
    button1 = InlineKeyboardButton(text='Add event', callback_data='add')
    words_choice.add(button1)
    await message.answer(text = "Hello! I'm Event-Bot 2023!\nWhat do you want to do?", reply_markup=words_choice)
    await state.finish()
    await States.begin.set()
if __name__ == '__main__':
     executor.start_polling(dp)
