from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
import logging
import asyncio
from aiogram import Bot,Dispatcher,types,F
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession


class SorawJuwapState(StatesGroup):
    name=State()
    surname=State()
    age=State()
    phone_number=State()
    suwret=State()


api='8818722219:AAGUBwg4xN4Gwl8pAyOiUzX6iSIkfph6R0s'
session = AiohttpSession(proxy='http://proxy.server:3128')
bot=Bot(api,session=session)
dp=Dispatcher()

@dp.message(Command('start'))
async def strat_bot(sms:types.Message):
    await sms.answer(text=f"Salem {sms.from_user.first_name}")

@dp.message(F.text=='registration')
async def reg_bot(sms:types.Message,state:FSMContext):
    await sms.answer(text='Atinizdi jazin: ')
    await state.set_state(SorawJuwapState.name)


@dp.message(SorawJuwapState.name)
async def save_name(sms:types.Message,state:FSMContext):
    name=sms.text
    if len(name)>5 and len(name)<20:
       await state.update_data(ati=sms.text)
       await sms.answer(text='Endi familiyanizdi jazin: ')
       await state.set_state(SorawJuwapState.surname)
       datas=await state.get_data()
       print(datas)
       
    else:
        await sms.answer(text="Atinizdi qaytaldan durislap jazin!")

@dp.message(SorawJuwapState.surname)
async def save_surename(sms:types.Message,state:FSMContext):
    surename=sms.text
    if surename.endswith('ov') or surename.endswith('va'):
       await state.update_data(familiyasi=sms.text)
       await sms.answer(text='Endi jasinizdi jazin: ')
       await state.set_state(SorawJuwapState.age)
       datas=await state.get_data()
       print(datas)
    else:
        await sms.answer(text='Familiyanizdi qaytaldan durislap jazin!')

@dp.message(SorawJuwapState.age)
async def save_age(sms:types.Message,state:FSMContext):
    age=sms.text
    if age.isdigit() and len(age)<2:
        await state.update_data(jasi=sms.text)
        await sms.answer(text='Endi nomerinizdi jazin: ')
        await state.set_state(SorawJuwapState.phone_number)
        datas=await state.get_data()
        print(datas)
    else:
        await sms.answer(text='Jasinizdi tek san menen jaziwiniz shart ham ueki tsifirdan kop bolmawi kerek!')

@dp.message(SorawJuwapState.phone_number)
async def save_phone_num(sms:types.Message,state:FSMContext):
    num=sms.text
    if num.startswith('+998') and num[1:].isdigit() and len(num)==13:
       await state.update_data(nomeri=sms.text)
       await sms.answer(text='Endi suwret jiberin: ')
       await state.set_state(SorawJuwapState.suwret)
       datas=await state.get_data()
       print(datas)
    else:
        await sms.answer(text='Telefon nomerinizdi qaytaldan durislap jazin!')

@dp.message(SorawJuwapState.suwret)
async def save_suwret(sms:types.Message,state:FSMContext):
    suwret=sms.photo[0].file_id
    print(sms.photo[0].file_id)
    await state.update_data(suwret=sms.photo[0].file_id)
    datas=await state.get_data()
    await sms.answer_photo(
        photo=datas['suwret'],
        caption=f'''
Atiniz: {datas['ati']}
Familiyaniz: {datas['familiyasi']}
Jasiniz: {datas['jasi']}
Nomeriniz: {datas['nomeri']}
'''
    )
    print(datas)
    

async def main():
   await dp.start_polling(bot)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
