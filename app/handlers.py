from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generate import ai_generate
import app.keyboards as kb

start_message = 'Привет я TelegramBot, в который интегрирована нейросеть DeepSeek. Напиши мне что-нибудь😉!'

class Gen(StatesGroup):
    wait = State()


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=start_message, reply_markup=kb.start_kb) 

@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Подождите, Ваш запрос генерируется...')

@router.message(F.text)
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    thinking_msg = await message.answer('Бот думает...') 
    response = await ai_generate(message.text)
    await thinking_msg.delete()
    await message.answer(response)
    
    await state.clear()

@router.callback_query(F.data == 'support')
async def contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Основатель и разработчик бота:\n@novikovyo', reply_markup=kb.continue_start)

@router.callback_query(F.data == 'return')
async def contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=start_message, reply_markup=kb.start_kb)