import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import nest_asyncio
import datetime
import requests
import threading
import os.path
import time
import site
from subprocess import Popen
nest_asyncio.apply()

directory=os.path.abspath("").split("\\")
directory="\\".join([i for i in directory if directory.index(i)!=len(directory)-1])

gt=0
while 1:
    time.sleep(0.05)
    try:
        if os.path.isfile("account.json"):
            account = json.load(open('account.json'))
            if account["token"]!=None:
                break
            elif (account["token"]==None) and (gt==0):
                print("enter your token")
                json.dump({"token":None,"proxy":None}, open('account.json','w'))
                gt+=1
        elif gt==0:
            print("enter your token")
            json.dump({"token":None,"proxy":None}, open('account.json','w'))
            gt+=1
    except Exception as error:
        pass
    
if account["proxy"]!=None:
    bot = Bot(account["token"], proxy=account["proxy"])
    
else:
    bot = Bot(token=account["token"])
dp = Dispatcher(bot)

first={}
second={}

entry_trader={ "st": None , "leverage": None , "sl": None , "sellorbuy": None , "stopPrice_sl": None , "stop_trail": None ,
             "symbol": None , "number_user": None , "rond": None ,
              "token_machin": None ,"commission": None , "change_st_leverage": None , "limit_money": None }

users={ "api_key": None , "api_secret": None , "api_passphrase": None , "balance_trade": None ,
       "username_user": None , "proxy": None , "permission": None }

username=None
@dp.message_handler(commands=['start'])
async def registration(message: types.Message):
    global entry_trader
    global users
    
    buttons = ["entry trader","new user","watch_position","open","close"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await bot.send_message(message.from_id, f"entry_trader:  {entry_trader} \n\n\nusers:  {users}")
    
    await message.answer("Hello \n select one of them", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Menu"])
async def registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['entry trader','new user',"watch_position","open","close"]
    keyboard.add(*buttons)
    await message.answer('select one of them',reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ['entry trader'])
async def registration(message: types.Message):
    global first
    first[str(message.from_id)]=message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["st", "sl", "leverage", "sellorbuy", "stopPrice_sl", "stop_trail", "symbol",
              "rond", "token_machin", "commission", "change_st_leverage", "limit_money","see","send","Menu"]
    keyboard.add(*buttons)
    await message.answer('select one of them',reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["st", "sl", "leverage", "sellorbuy", "stopPrice_sl",
                                                     "stop_trail", "symbol","rond", "token_machin",
                                                    "commission","change_st_leverage", "limit_money"])
async def registration(message: types.Message):
    global first
    global second
    if first[str(message.from_id)]=='entry trader':
        second[str(message.from_id)]=message.text

@dp.message_handler(lambda message: message.text in ['new user'])
async def registration(message: types.Message):
    global first
    first[str(message.from_id)]=message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["api_key","api_secret","api_passphrase","balance_trade","username_user","permission",
               "see","send","Menu"]
    keyboard.add(*buttons)
    await message.answer('select one of them \n you must enter your message in this way:\n details account user:username_user \n for exampel for permission:\n permission:username_user',reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["api_key", "api_secret", "api_passphrase",
                                                     "balance_trade", "username_user", "permission"])
async def registration(message: types.Message):
    global first
    global second
    if first[str(message.from_id)]=='new user':
        second[str(message.from_id)]=message.text

@dp.message_handler(lambda message: message.text in ["see","send"])
async def registration(message: types.Message):
    global first
    global second
    global entry_trader
    global users
    global directory
    exit=None

    if first[str(message.from_id)]=='new user':
        if message.text=="see":
            await bot.send_message(message.from_id, str(users))
        else:
            while 1:
                time.sleep(0.05)
                try:
                    if os.path.isfile("%s\\users.json" % directory):
                        
                        update_users=json.load(open("%s\\users.json" % directory))
                        break
                    else:
                        await bot.send_message(message.from_id, "No exist users in directory")
                        exit=0
                        break
                except Exception as error:
                    pass
            if exit==None:
                if users["username_user"] not in update_users:
                    update_users[users["username_user"]]=users
                else:
                    for i in users:
                        if users[i]!=None:
                            update_users[users["username_user"]][i]=users[i]
                        
                json.dump(update_users, open("%s\\users.json" % directory,'w'))
        
                users={"api_key": None, "api_secret": None, "api_passphrase": None, "balance_trade": None,
                       "username_user": None, "proxy": None, "permission": None}
        
    elif first[str(message.from_id)]=='entry trader':
        if message.text=="see":
            await bot.send_message(message.from_id, str(entry_trader))
        else:
            while 1:
                time.sleep(0.05)
                try:
                    
                    if os.path.isfile("%s\\entry_trader.json"%directory):
                        update_entry_trader=json.load(open("%s\\entry_trader.json" % directory))
                        break
                    else:
                        await bot.send_message(message.from_id, "No exist entry_trader in directory")
                        exit=0
                        break
                except Exception as error:
                    pass

            if exit==None:
                for i in entry_trader:
                    if (entry_trader[i]!=None) and (i in ["st","leverage","sellorbuy","stopPrice_sl","stop_trail",
                                                          "symbol"]):
                        update_entry_trader[i]=entry_trader[i]
                    elif (entry_trader[i]!=None) and (i not in ["st","leverage","sellorbuy","stopPrice_sl",
                                                                "stop_trail","symbol"]):
                        update_entry_trader["propertise"][i]=entry_trader[i]

                while 1:
                    time.sleep(0.05)
                    try:
                        json.dump(update_entry_trader, open("%s\\entry_trader.json" % directory,'w'))
                        if update_entry_trader["get_signal"]==1:
                            break
                        time.sleep(5)
                        get_ok=json.load(open("%s\\get_ok.json" % directory))
                        if get_ok["status"]==1:
                            while 1:
                                time.sleep(0.05)
                                try:
                                    json.dump({"status":0}, open("%s\\get_ok.json" % directory,'w'))
                                    break
                                except Exception as error:
                                    pass
                            break
                    except Exception as error:
                        pass
                    entry_trader={"st": None, "leverage": None, "sl": None, "sellorbuy": None, 
                                  "stopPrice_sl": None,"stop_trail": None,"symbol": None, "number_user": None,
                                  "rond": None,"token_machin": None,"commission": None,
                                  "change_st_leverage": None,"limit_money": None}

@dp.message_handler(lambda message: message.text in ["watch_position"])
async def registration(message: types.Message):
    global directory
    while 1:
        time.sleep(0.05)
        try:

            if os.path.isfile("%s\\watch_position.json" % directory):
                watch_position=json.load(open("%s\\watch_position.json" % directory))
                await bot.send_message(message.from_id, str(watch_position))
                break
            else:
                await bot.send_message(message.from_id,"No exist watch_position in directory")
                break
        except Exception as error:
            pass
        
@dp.message_handler(lambda message: message.text in ["open","close"])
async def registration(message: types.Message):
    global directory
    
    def control_software(type_control,directory=directory):
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        Popen([type_control],
                         stdin=None, stdout=None, stderr=None, shell=True, cwd=directory,
                         creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
                         )
    if message.text=="open":
        control_software("start.bat")
    elif message.text=="close":
        control_software("close.bat")

@dp.message_handler(regexp='[\w|\W]')
async def savefilters(message: types.update):
    global first
    global second
    global entry_trader
    global users
    global username
    
    if len(first)==0:
        first[str(message.from_id)]=None
    if len(second)==0:
        second[str(message.from_id)]=None
    if first[str(message.from_id)]=='entry trader':
        if second[str(message.from_id)] in ["st", "sl", "leverage","sellorbuy", "stopPrice_sl",
                                                     "stop_trail","symbol","rond", "token_machin",
                                                    "commission","change_st_leverage","limit_money"]:

            if second[str(message.from_id)] in ["symbol","token_machin"]:
                entry_trader[second[str(message.from_id)]]=str(message.text)
                
            else:
                if message.text.isdigit():
                    entry_trader[second[str(message.from_id)]]=int(message.text)
                else:
                    entry_trader[second[str(message.from_id)]]= float(message.text)
                
    

    elif first[str(message.from_id)]=='new user':
        if second[str(message.from_id)] in ["api_key", "api_secret", "api_passphrase",
                                            "balance_trade", "username_user", "permission"]:

            t=[x.strip() for x in message.text.split(":")]
            if t[1]!=username:
                await bot.send_message(message.from_id, "new username")
            username=t[1]
            
            if second[str(message.from_id)] in ["balance_trade","permission"]:
                
                if message.text.isdigit():
                    users[second[str(message.from_id)]]=int(t[0])
                else:
                    users[second[str(message.from_id)]]= float(t[0])
            else:
                users[second[str(message.from_id)]]=str(t[0])

if __name__ == '__main__':
   # __import__('IPython').embed()
    executor.start_polling(dp)
