from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
import random


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

attemps = 7
user = {'in_game':False,'secret_number':None, 'attemps':None, 'total_games':0, 'wins':0}

def get_number()->int:
    return random.randint(1,100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - /help')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Правила игры:\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно за {attemps} попыток его угадать\n\n'
                         'Команды:\n/help - правила\n/stat - статистика\n'
                         '/cancel - закончить игру\nСыграем?\n/start - начало')
@dp.message(Command(commands='cancel'))
async def process_cencel_command(message:Message):
    if user['in_game']:
        user['in_game']=False
        await message.answer(text='Игра окончена')
    else:
        await message.answer('Мы не играем.\nХотите сыграть?')

@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(f'Всего сыграно {user['total_games']} игр\n'
                         f'Вы выйграли {user["wins"]}')

@dp.message(F.text.lower().in_(['да','давай','сыграем','играть']))
async def process_positive_answer(message: Message):
    if not user['in_game']:    
        user['in_game']= True
        user['secret_number']=get_number()
        user['attemps']=attemps
        await message.answer('Я загадал число от 1 до 100\nПопробуй угадать')
    else:
        await message.answer('Мы уже играем\nвведите число от 1 до 100 или /cancel для окончания игры')
@dp.message(F.text.lower().in_(['не','нет','не буду','не хочу']))
async def process_negative_answer(message:Message):
    if not user['in_game']:
        await message.answer('Если захотите играть, просто напишите "играть"')
    else:
        await message.answer('Мы уже играем\nвведите число от 1 до 100 или /cancel для окончания игры')
@dp.message(lambda x: x.text and x.text.isdigit() and 1<=int(x.text)<=100)
async def process_number_answer(message:Message):
    if user['in_game']:
        if int(message.text)==user['secret_number']:
            user['in_game']=False
            user['total_games']+=1
            user['wins']+=1
            await message.answer('Вы угадали число\nСыграем еще?')
        elif int(message.text)<user['secret_number']:
            user['attemps']-=1
            await message.answer('Мое число больше')
        else:
            user['attemps']-=1
            await message.answer('Мое число меньше')
        if user['attemps']==0:
            user['in_game']=False
            user['total_games']+=1
            await message.answer('Попытки закончились, вы проиграли\n'
                                 f'Моим числом было {user['secret_number']}\n'
                                 'Сыграем еще?')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_answer(message:Message):
    if user['in_game']:
        await message.answer('Мы уже играем\nвведите число от 1 до 100 или /cancel для окончания игры')
    else:
        await message.answer('Ты ограниченный? Хотите сыграть?\n'
                             'Воспользуйтесь командой /help')

if __name__=='__main__':
    dp.run_polling(bot)