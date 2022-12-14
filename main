import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
import time
import uuid
import datetime
import threading
from websocket import create_connection
import os
import sys
import socket
import random
import string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os.path
import linecache

class trader():

    def __init__(self,rond=4,commission=0.001):

        self.detail_accuonts ={}
        self.price =None
        self.rond =rond
        self.runpricetr =None
        self.ws =0
        self.alive_positions ={}
        self.commission =commission
        self.touched_sl =0
        self.sl_tp =None
        self.base_uri = 'https://api-futures.kucoin.com'
        self.id=None
        self.touched_st =0
        self.one_lot=None
        self.api_correct=[]
        self.multiplier={}
        allnumber,entry_trader=self.user_get()
        entry_trader['sellorbuy']=None
        json.dump(entry_trader, open('entry_trader.json', 'w'))

        self.symbol=entry_trader["symbol"]
        self.proxy_user=entry_trader["propertise"]['number_user_proxy']
        com=entry_trader["propertise"]['commission']
        ro=entry_trader["propertise"]['rond']
        if (com!=None) and (ro!=None) and (type(ro)==int) and (type(com)==int):
            self.commission =com
            self.rond =ro
            
        key=entry_trader["propertise"]['token_machin'].split(":")
        key_user=key[0]
        key_second=key[1]
        
        t=[i for i in list(key_second) if i.isdigit()]
        t=(len(t))*2
        key=(key_second[int(-t/2)::] + key_user[int(-t/2)::]).encode()
        
        with open('key.json','rb') as f:
            source = f.read().decode()
        t=self.decrypt(key, source, decode=True)
        t=t.decode()
        self.chek_dic=eval(t)
        
    def creat_accuont(self):
        def accuo():

            self.base_uri = 'https://api-futures.kucoin.com'

            while 1:
                time.sleep(0.05)
                try:
                    if os.path.isfile("users.json"):
                        user=json.load(open('users.json'))
                        break
                    else:
                        user={}
                        json.dump(user, open('users.json', 'w'))
                        break
                except Exception as error:
                    pass


            ind=['availableBalance','calculated_size','type_ballance','api_key','api_passphrase','stop_trail',
                 'api_secret','id','leverage','side','size_position','symbol','status','stopPrice_sl','lastprice',
                 'trailprice','actionprice','sl','st','status_sl','orderId_position','orderId_sl','last_time',"permission",
                 'proxy','PNL','balance_trade']
            column=[]
            for i in [*user]:
                if user[i]["permission"]==1:
                    column.append(i)
            
            if len(column)>0:
                self.set_proxy()
                user=json.load(open('users.json'))
                ind_key = {key: 0 for key in ind}
                self.detail_accuonts = {key: ind_key for key in column}

                for i in column:
                    self.detail_accuonts[i]['api_key']=user[i]['api_key']
                    self.detail_accuonts[i]['api_secret']=user[i]['api_secret']
                    self.detail_accuonts[i]['api_passphrase']=user[i]['api_passphrase']
                    self.detail_accuonts[i]['status']=0
                    self.detail_accuonts[i]['status_sl']=0
                    self.detail_accuonts[i]['type_ballance']=['XBT','USDT','XRP','ETH','DOT']
                    self.detail_accuonts[i]['last_time']=str(datetime.datetime.utcnow())
                    self.detail_accuonts[i]['balance_trade']=user[i]['balance_trade']
                    self.detail_accuonts[i]['proxy']=user[i]['proxy']
                    self.detail_accuonts[i]['permission']=user[i]['permission']
                    
                entry_trader=json.load(open("entry_trader.json"))
                entry_trader["propertise"]['number_user']=len([*self.detail_accuonts])
                json.dump(entry_trader, open('entry_trader.json', 'w'))
            
            return

        if os.path.isfile("detail_accuonts.json"):
            print('exist detail_accuonts.json')
            while 1:
                time.sleep(0.05)
                try:
                    self.detail_accuonts=json.load(open('detail_accuonts.json'))

                    self.multi_threading(func=self.check_exist_alive_position,accuonts=[*self.detail_accuonts])
                    check=0
                    for i in [*self.detail_accuonts]:
                        if self.detail_accuonts[i]['status']>0:
                            check=1
                            break
                    if check==0:
                        accuo()
                    break
                except Exception as error:
                    self.PrintException()
        else:
            accuo()
            self.multi_threading(func=self.check_exist_alive_position,accuonts=[*self.detail_accuonts])
        if len([*self.detail_accuonts])>0:

            json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
        return self.detail_accuonts

    def new_user(self):
        while 1:
            time.sleep(0.05)
            try:
                user=json.load(open('users.json'))
                entry_trader=json.load(open("entry_trader.json"))
                break
            except Exception as error:
                pass

        check_newuser=entry_trader["propertise"]['number_user']
        
        ind=['availableBalance','calculated_size','type_ballance','api_key','api_passphrase','stop_trail',
             'api_secret','id','leverage','side','size_position','symbol','status','stopPrice_sl','lastprice',
             'trailprice','actionprice','sl','st','status_sl','orderId_position','orderId_sl','last_time','permission',
             'proxy','PNL','balance_trade']

        user={k:v for k,v in user.items() if v["permission"]==1}
        if len(user)>check_newuser:
            column=[]
            for i in [*user]:
                if user[i]["permission"]==1:
                    column.append(i)

            if len(column)>0:
                self.set_proxy()
                user=json.load(open('users.json'))
                ind_key = {key: 0 for key in ind}
                new_detail_accuonts = {key: ind_key for key in column}

                self.detail_accuonts.update(new_detail_accuonts)
                for i in column:
                    self.detail_accuonts[i]['api_key']=user[i]['api_key']
                    self.detail_accuonts[i]['api_secret']=user[i]['api_secret']
                    self.detail_accuonts[i]['api_passphrase']=user[i]['api_passphrase']
                    self.detail_accuonts[i]['status']=0
                    self.detail_accuonts[i]['status_sl']=0
                    self.detail_accuonts[i]['type_ballance']=['XBT','USDT','XRP','ETH','DOT']
                    self.detail_accuonts[i]['last_time']=str(datetime.datetime.utcnow())
                    self.detail_accuonts[i]['balance_trade']=user[i]['balance_trade']
                    self.detail_accuonts[i]['proxy']=user[i]['proxy']
                    self.detail_accuonts[i]['permission']=user[i]['permission']
                    
                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                json.dump(user, open('users.json','w'))
                
                entry_trader["propertise"]['number_user']=len([*self.detail_accuonts])
                json.dump(entry_trader, open('entry_trader.json', 'w'))

    def set_proxy(self):
        global used_proxy
        global proxy_list
        while 1:
            try:
                if os.path.isfile("users.json"):
                    user=json.load(open('users.json'))
                    break
            except Exception as error:
                pass
        
        if len(user)>0:
            origin_ip={}
            for i in user:
                if user[i]['proxy']==None:
                    origin_ip[i]=user[i].copy()
                if len(origin_ip)==self.proxy_user:
                    break
            while 1:
                time.sleep(0.05)
                try:
                    if os.path.isfile("proxy_list.json"):
                        proxy_list=json.load(open('proxy_list.json'))
                        break
                    else:
                        proxy_list=[]
                        break
                except Exception as error:
                    pass

            while 1:
                time.sleep(0.05)
                try:
                    if os.path.isfile("used_proxy.json"):
                        used_proxy=json.load(open('used_proxy.json'))
                        break
                    else:
                        used_proxy=[]
                        json.dump(used_proxy, open('used_proxy.json', 'w'))
                        break
                except Exception as error:
                    pass



            maxmin={'now':0 , 'max':self.proxy_user}

            for i in proxy_list:
                if i not in [*used_proxy]:
                    used_proxy[i]=maxmin.copy()

            def find_empty_proxy():
                global used_proxy
                global proxy_list

                pro=0
                n=0
                if len(proxy_list)>0:
                    for i in proxy_list:
                        if used_proxy[i]['now']<used_proxy[i]['max']:
                            n=used_proxy[i]['now']
                            pro=i
                            break
                return pro , n
            pro,n=find_empty_proxy()

            if len(proxy_list)>0:
                for i in [*user]:
                    if (user[i]['proxy']==None) and (i not in origin_ip):
                        n+=1
                        user[i]['proxy']=pro
                        if n==used_proxy[pro]['max']:
                            used_proxy[pro]['now']=n
                            pro,n=find_empty_proxy()
                            if (pro==0) or (n==0):
                                print("you don't have enough proxy")
                                break
                json.dump(used_proxy, open('used_proxy.json', 'w'))
                json.dump(user, open('used_proxy.json', 'w'))

    def runprice(self):
        try:
            url='https://api.kucoin.com/api/v1/bullet-public'
            token=json.loads(requests.post(url).text)['data']['token']
            self.ws=create_connection('wss://ws-api.kucoin.com/endpoint?token=%s&[connectId=%s]' % (token,uuid.uuid1()))

            msg = {"id":"%s" % (uuid.uuid1()),
                "type": "subscribe",
                "topic": "/contractMarket/ticker:%s" %(self.symbol),
                "response": True}
            msg=json.dumps(msg)
            self.ws.send(msg)
            i=0
            while self.runpricetr==1:
                p = json.loads(self.ws.recv())
                if "data" in p:
                    if 'price' in p['data']:
                        self.price=p['data']['price']

                if i==3:
                    msg = {"id":"%s" % (uuid.uuid1()),
                "type":"pong"
                          }
                    msg=json.dumps(msg)
                    self.ws.send(msg)
                    i=0
                i+=1
        except Exception as error:
            thread=threading.Thread(target=self.runprice)
            thread.start()

    def refresh_runprice(self):
        x=1
        while x==1:
            try:
                time.sleep(0.3)
                url = " https://api-futures.kucoin.com/api/v1/contracts/active"
                payload={}
                files={}
                headers = {}
                pairs = requests.request("GET", url, headers=headers, data=payload, files=files)
                pairs=pairs.json()
                pairs=pairs['data']
                pairs=[x for x in pairs if x['quoteCurrency']=='USDT']
                self.price={item['symbol']:item['lastTradePrice'] for item in pairs}[self.symbol]
            except Exception as error:
                pass
        return

    def lot_size(self):
        url = " https://api-futures.kucoin.com/api/v1/contracts/active"
        payload={}
        files={}
        headers = {}
        pairs = requests.request("GET", url, headers=headers, data=payload, files=files)
        pairs=pairs.json()
        pairs=pairs['data']
        pairs=[x for x in pairs if x['quoteCurrency']=='USDT']
        self.multiplier={item['symbol']:item['multiplier'] for item in pairs}

        return 

    def set_param_orders(self,leverage,side,size,stopPrice_sl=None,stopPrice_tp=None,maintrade=True,
                         sl_trade=True,tp_trade=True,close_position=False):
        listparams=[]  #   for main position  listparams=['main position','stop los', 'take profit']
        if maintrade==True:
            params ={'clientOid': str(uuid.uuid1()),
                    'side': side,
                    'symbol': self.symbol,
                    'type': "market",
                    'size': str(size),
                    'leverage': str(leverage),
                    'remark':'maintrade'}
            data_json = json.dumps(params)
            listparams.append(data_json)

        if side=='buy':

            if sl_trade==True:
                params ={'symbol':self.symbol,
                        'side':'sell',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stop':'down',
                        'stopPrice':str(stopPrice_sl),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

            if tp_trade==True:
                params ={'symbol':self.symbol,
                        'side':'sell',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stop':'up',
                        'stopPrice':str(stopPrice_tp),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

            if close_position==True:
                params ={'symbol':self.symbol,
                        'side':'sell',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

        elif side=='sell':

            if sl_trade==True:
                params ={'symbol':self.symbol,
                        'side':'buy',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stop':'up',
                        'stopPrice':str(stopPrice_sl),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

            if tp_trade==True:
                params ={'symbol':self.symbol,
                        'side':'sell',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stop':'down',
                        'stopPrice':str(stopPrice_tp),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

            if close_position==True:
                params ={'symbol':self.symbol,
                        'side':'buy',
                        'leverage':str(leverage),
                        'type': 'market',
                        'clientOid':str(uuid.uuid1()),
                        'size':str(size),
                        'stopPriceType':'MP',
                        'closeOrder':'true'}
                data_json = json.dumps(params)
                listparams.append(data_json)

        return listparams

    def decrypt(self,key, source, decode=True):
        if decode:
            source = base64.b64decode(source.encode("latin-1"))
        key = SHA256.new(key).digest()
        IV = source[:AES.block_size]
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(source[AES.block_size:])
        padding = data[-1]
        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")
        return data[:-padding]

    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print(exc_type)
        print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        
        return

    def get_headers(self,method,endpoint,parameters,user=None):
        api_key=self.detail_accuonts[user]['api_key']
        api_secret=self.detail_accuonts[user]['api_secret']
        api_passphrase=self.detail_accuonts[user]['api_passphrase']
        now = int(time.time() * 1000)
        if parameters=='':
            str_to_sign = str(now) + method + endpoint
        else:
            str_to_sign = str(now) + method + endpoint + parameters
        signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()).decode()
        passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest()).decode()
        return {'KC-API-SIGN': signature,
                'KC-API-TIMESTAMP': str(now),
                'KC-API-KEY': api_key,
                'KC-API-PASSPHRASE': passphrase,
                'KC-API-KEY-VERSION': '2',
                'Content-Type': 'application/json'}

    def request_order(self,meth,num,addendpoint,parameters=None,user=None):
        getmethod={'GET':{'1':'account-overview?currency=','2':'transaction-history','3':'deposit-address','4':'deposit-list',
        '5':'withdrawals/quotas','6':'withdrawal-list','7':'orders?status=done','8':'stopOrders?symbol=','9':'recentDoneOrders',
        '10':'fills','11':'recentFills','12':'openOrderStatistics','13':'positions?symbol=','14':'position?symbol=',
        '15':'contracts/risk-limit/','16':'funding-history?symbol=','method':'GET'},

        'POST':{'1':'orders','2':'position/margin/auto-deposit-status','3':'position/margin/deposit-margin',
        '4':'position/risk-limit-level/change','method':'POST'},

        'DELETE':{'1':'orders/','2':'orders?symbol=','3':'stopOrders?symbol=','method':'DELETE' }}

        method = getmethod[meth]['method']
        if addendpoint=='':
            endpoint = '/api/v1/%s' % (getmethod[method][num])
        else:
            endpoint = '/api/v1/%s' % (getmethod[method][num]) + addendpoint
            print(endpoint)
        re=''
        x=1
        while x==1:
            try:
                if self.detail_accuonts[user]['proxy']==None:
                    response = requests.request(method, self.base_uri+endpoint,
                        headers=self.get_headers(method,endpoint,parameters,user=user), data=parameters)
                else:
                    proxies = {
                               'http': 'http://%s' % (self.detail_accuonts[user]['proxy']),
                               'https': 'http://%s' % (self.detail_accuonts[user]['proxy']),}
                    response = requests.request(method, self.base_uri+endpoint,
                        headers=self.get_headers(method,endpoint,parameters,user=user), data=parameters ,proxies=proxies)
                print(response.status_code)
                if response.status_code==200:
                    if user in self.api_correct:
                        self.api_correct.remove(user)
                    break
                elif response.status_code==300003:
                    print('no enough money')
                    break
                elif response.status_code==429:
                    print('Too Many Requests')
                elif response.status_code==200002:
                    print('time sleep 10')
                    time.sleep(11)
                elif (response.status_code==400001) and (response.status_code==400002) and (response.status_code==400003)\
                and (response.status_code==400004):
                    self.api_correct.append(user)
                    print('self.api_correct=0 for user %s' % (user))
                    break
                 
                elif response.status_code!=429 or response.status_code!=200002 :
                    print(response.status_code ,' : ', response.json()['msg'])
                    break
            except Exception as error:
                re='request_order'
                print(re)
                print(error)
            
        return response.json() , re , response.status_code

    def open_position(self,user,leverage,side,stopPrice_sl):
       
        
        
        cost=leverage*(self.detail_accuonts[user]['availableBalance']*(self.detail_accuonts[user]['balance_trade']/100))
        size=int(cost/(self.one_lot*self.price))
        self.detail_accuonts[user]['calculated_size']=size
        no_enough_money=1
        if size<1:
            no_enough_money=0

        if (self.detail_accuonts[user]['status']==0) and (no_enough_money==1) and (user not in self.api_correct):
            if side=='sell':
                print('sell-open_position')
                listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                stopPrice_sl=stopPrice_sl,tp_trade=False)
                for parameters in listparams:
                    response,re,statusCode=self.request_order(num='1',parameters=parameters,meth='POST',addendpoint='',user=user)
                    if listparams.index(parameters)==0:
                        if statusCode==200:
                            self.detail_accuonts[user]['status']=1
                            self.detail_accuonts[user]['orderId_position']=response['data']['orderId']
                        else:
                            break
                    if listparams.index(parameters)==1:
                        if statusCode==200:
                            self.detail_accuonts[user]['status_sl']=1
                            self.detail_accuonts[user]['orderId_sl']=response['data']['orderId']

            if side=='buy':
                print('buy-open_position')
                listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                stopPrice_sl=stopPrice_sl,tp_trade=False)
                for parameters in listparams:
                    response , re , statusCode=self.request_order(parameters=parameters,meth='POST',num='1',addendpoint='',user=user)
                    if listparams.index(parameters)==0:
                        if statusCode==200:
                            self.detail_accuonts[user]['status']=1
                            self.detail_accuonts[user]['orderId_position']=response['data']['orderId']
                        else:
                            break
                    if listparams.index(parameters)==1:
                        if statusCode==200:
                            self.detail_accuonts[user]['status_sl']=1
                            self.detail_accuonts[user]['orderId_sl']=response['data']['orderId']

        if self.detail_accuonts[user]['status']==1:
            self.detail_accuonts[user]['side']=side
            self.detail_accuonts[user]['size_position']=size
            self.detail_accuonts[user]['leverage']=leverage
            self.detail_accuonts[user]['symbol']=self.symbol
            x=1
            i=0
            while x==1:

                response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)
                if statusCode==200 and len(response['data'])!=0: 
                    entryprice=response['data'][0]['avgEntryPrice']
                    self.detail_accuonts[user]['id']=response['data'][0]['id']
                    self.detail_accuonts[user]['trailprice']=entryprice
                    self.detail_accuonts[user]['actionprice']=entryprice
                    break
                if  len(response['data'])==0:
                    i+=1
                if i==2:
                    entryprice=self.price
                    self.detail_accuonts[user]['trailprice']=entryprice
                    self.detail_accuonts[user]['actionprice']=entryprice
                    break
        json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                    
        return

    def control_sl(self,user,leverage,side):
        

        if self.detail_accuonts[user]['status']==1:
            parameters=''
            x=1
            c=0
            size=self.detail_accuonts[user]['calculated_size']
            if side=='buy':
                print('buy-control_sl')
                while x==1:
                    response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)
                    if c>=1:
                        listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                        maintrade=False,sl_trade=False,tp_trade=False,close_position=True)
                        response,re,statusCode=self.request_order(parameters=listparams[0],meth='POST',num='1',addendpoint='',user=user)
                        print(8)
                        if statusCode==200:
                            print(2)
                            statusCode=0
                            response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)

                            if (statusCode==200) and (len(response['data'])==0):
                                print(1)
                                self.alive_positions.pop(user)
                                response,re,statusCode=self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
                                self.detail_accuonts[user]['status']=0
                                break

                    elif (statusCode==200) and (len(response['data'])==0):
                        print(3)
                        self.alive_positions.pop(user)
                        self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
                        self.detail_accuonts[user]['status']=0
                        break

                    c+=1

            if side=='sell':
                print('sell-control_sl')
                while x==1:
                    response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)
                    if c>=1:
                        listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                        maintrade=False,sl_trade=False,tp_trade=False,close_position=True)
                        response,re,statusCode=self.request_order(parameters=listparams[0],meth='POST',num='1',addendpoint='',user=user)

                        print(7)
                        if statusCode==200:
                            print(5)
                            statusCode=0
                            response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)

                            if (statusCode==200) and (len(response['data'])==0):
                                print(4)
                                self.alive_positions.pop(user)
                                response,re,statusCode=self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
                                self.detail_accuonts[user]['status']=0
                                break

                    elif (statusCode==200) and (len(response['data'])==0):
                        print(6)
                        self.alive_positions.pop(user)
                        self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
                        self.detail_accuonts[user]['status']=0
                        break

                    c+=1

        return 

    def control_stoptrail(self,user,stopPrice_sl):

        size=self.detail_accuonts[user]['calculated_size']
        leverage=self.alive_positions[user]['leverage']
        side=self.alive_positions[user]['side']

        if side=='buy':
            print('buy-control_stoptrail')
            x=1
            while x==1:
                listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                stopPrice_sl=stopPrice_sl,maintrade=False,sl_trade=True,tp_trade=False)

                response,re,statusCode=self.request_order(parameters=listparams[0],meth='POST',num='1',addendpoint='',user=user)
                if statusCode==200:
                    self.detail_accuonts[user]['stopPrice_sl']=stopPrice_sl
                    break

        if side=='sell':
            print('sell-control_stoptrail')
            x=1
            while x==1:
                listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                stopPrice_sl=stopPrice_sl,maintrade=False,sl_trade=True,tp_trade=False)

                response,re,statusCode=self.request_order(parameters=listparams[0],meth='POST',num='1',addendpoint='',user=user)
                if statusCode==200:
                    self.detail_accuonts[user]['stopPrice_sl']=stopPrice_sl
                    break
        self.detail_accuonts[user]['trailprice']=self.price
        return

    def first_control(self,user,kwargs=None):

        if self.detail_accuonts.loc['status',user]==1:
            response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)
            if len(response['data'])!=0:
                response,re,statusCode=self.request_order(parameters='',meth='GET',num='7',addendpoint='',user=user)
                i=1
                while i < len(response['data']['items']):
                    if response['data']['items'][-i]['remark']=='maintrade':
                        side=response['data']['items'][-i]['remark']
                        self.symbol=response['data']['items'][-i]['symbol']
                        size=respons.json()['data']['items'][-i]['size']
                        leverage=response['data']['items'][-i]['leverage']
                        break
                listparams=self.set_param_orders(leverage=leverage,side=side,size=size,
                maintrade=False,sl_trade=False,tp_trade=False,close_position=True)

                self.request_order(parameters=listparams[0],meth='POST',num='1',addendpoint=self.symbol,user=user)
                self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)

            if len(response['data'])==0:
                self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
        return

    def check_exist_alive_position(self,user,kwargs=None):
        
        if len([*self.detail_accuonts])>=0:
            x=1
            while x==1:
                response,re,statusCode=self.request_order(parameters='',meth='GET',num='13',addendpoint=self.symbol,user=user)
                if (len(response['data'])==0) and (statusCode==200):
                    self.multi_threading(func=self.reset_users,accuonts=[*self.detail_accuonts])
                    self.request_order(parameters='',meth='DELETE',num='3',addendpoint=self.symbol,user=user)
                    print('seccful reset detail accuont')
                    break
                elif (len(response['data'])!=0) and (statusCode==200):
                    break

    def multi_threading(self,func,accuonts,**kwargs):

        threads=[]
        if len(kwargs)==0:
            kwargs=None
        for i in accuonts:
            user=i
            thread=threading.Thread(target=func,args=(user,kwargs,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return

    def account_overview(self,user,kwargs=None):
        print(self.detail_accuonts[user]['type_ballance'][1])
        response,re,statusCode=self.request_order(parameters='',meth='GET',num='1',addendpoint=self.detail_accuonts[user]['type_ballance'][1],user=user)
        self.detail_accuonts[user]['availableBalance']=response['data']['availableBalance']
        return

    def reset_users(self,user,kwargs=None):
        print('*****')

        zero=['availableBalance','calculated_size','id','leverage','side','size_position',
              'symbol','status','symbol','stopPrice_sl','stop_trail','trailprice','actionprice','sl','st',
              'status_sl','orderId_position','orderId_sl']
        for i in zero:
            self.detail_accuonts[user][i] = 0
        json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
        return

    def get_signal(self):

        print('enter a signal')
        x=1
        while x==1:
            time.sleep(0.05)
            try:
                detail = json.load(open( "entry_trader.json"))
                if detail["get_signal"]==1:
                    detail["get_signal"]=0
                    json.dump(detail, open('entry_trader.json', 'w'))
                if (type(detail['st'])==float) and (type(detail['leverage'])==int) \
                 and (type(detail["propertise"]['sl'])==float):

                    if (detail["propertise"]['sl']>0) and (detail["propertise"]['sl']<=0.05) and (detail['st']>0):
                        if (detail['sellorbuy']==1) or (detail['sellorbuy']==0) and (detail['leverage']>0) :
                            for i in [*self.detail_accuonts]:
                                self.detail_accuonts[i]['st']=detail['st']
                                self.detail_accuonts[i]['leverage']=detail['leverage']
                                self.detail_accuonts[i]['sl']=detail["propertise"]['sl']
                                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))

                            self.symbol=detail["symbol"]
                            self.one_lot=self.multiplier[self.symbol]

                            detail_copy=detail.copy()
                            detail_copy['leverage']=0
                            detail_copy['st']=0
                            detail_copy["get_signal"]=1
                            detail_copy["propertise"]['sl']=0

                            detail_copy['sellorbuy']=None
                            json.dump(detail_copy, open('entry_trader.json', 'w'))
                            break
            except Exception as error:
                detail['sellorbuy']=None
                json.dump(detail, open('entry_trader.json', 'w'))
                print(error)

        return detail

    def open_order(self):

        detail = self.get_signal()
        print(1)
        x=1
        while x==1:
            time.sleep(0.05)
            if self.price==0:
                time.sleep(5)
            elif self.price!=None:
                break
        print('\n new order\n in ' ,detail,'\n')
        while 1:
            time.sleep(0.05)
            try:
                json.dump({"status":1}, open('get_ok.json','w'))
                break
            except Exception as error:
                pass
        
        for i in [*self.detail_accuonts]:
            self.detail_accuonts[i]['symbol']=self.symbol
        p=self.price
        threads_op=[]
        entry_trader=json.load(open("entry_trader.json"))
        if detail['sellorbuy']==0:
            for i in [*self.detail_accuonts]:
                self.detail_accuonts[i]['side']='sell'
            print('sell position')
            for i in [*self.detail_accuonts]:
                self.detail_accuonts[i]['stopPrice_sl']=(1+(self.detail_accuonts[i]['sl']/self.detail_accuonts[i]['leverage']))\
                *p - p*self.commission
                self.detail_accuonts[i]['stop_trail']=(1-(self.detail_accuonts[i]['st']/self.detail_accuonts[i]['leverage']))\
                *p - p*self.commission

            for i in [*self.detail_accuonts]:
                if (self.detail_accuonts[i]['permission']==1)\
                and (self.detail_accuonts[i]['availableBalance']>=entry_trader["propertise"]['limit_money']):
                
                    thread=threading.Thread(target=self.open_position,args=(i,
                    self.detail_accuonts[i]['leverage'],self.detail_accuonts[i]['side'],round(self.detail_accuonts[i]['stopPrice_sl'],self.rond),))
                    thread.start()
                    threads_op.append(thread)
            for thread in threads_op:
                thread.join()
                threads_op.remove(thread)

        if detail['sellorbuy']==1:
            for i in [*self.detail_accuonts]:
                self.detail_accuonts[i]['side']='buy'
            print('buy position')
            for i in [*self.detail_accuonts]:
                self.detail_accuonts[i]['stopPrice_sl']=(1-(self.detail_accuonts[i]['sl']/self.detail_accuonts[i]['leverage']))\
                *p + p*self.commission
                self.detail_accuonts[i]['stop_trail']=(1+(self.detail_accuonts[i]['st']/self.detail_accuonts[i]['leverage']))\
                *p + p*self.commission

            for i in [*self.detail_accuonts]:
                if (self.detail_accuonts[i]['permission']==1)\
                and (self.detail_accuonts[i]['availableBalance']>=entry_trader["propertise"]['limit_money']):
                    thread=threading.Thread(target=self.open_position,args=(i,
                    self.detail_accuonts[i]['leverage'],self.detail_accuonts[i]['side'],round(self.detail_accuonts[i]['stopPrice_sl'],self.rond),))
                    thread.start()
                    threads_op.append(thread)
            for thread in threads_op:
                thread.join()
                threads_op.remove(thread)
        return

    def control_position_buy(self):
        
        self.touched_st=[]
        self.touched_sl=[]
        self.sl_tp={'stop_trail':0,'stopPrice_sl':0}
        print('control buy')
        cho=[*self.alive_positions][0]
        print('action price: ',self.alive_positions[cho]['trailprice'])
        print("stop_trail: ",self.alive_positions[cho]['stop_trail'])
        print('stopPrice_sl: ',self.alive_positions[cho]['stopPrice_sl'])
        
        while 1:
            time.sleep(0.05)
            try:
                json.dump({"action_price":self.alive_positions[cho]['trailprice'],
                           "stop_trail":self.alive_positions[cho]['stop_trail'],
                           "stopPrice_sl":self.alive_positions[cho]['stopPrice_sl']},
                          open('watch_position.json','w'))
                break
            except Exception as error:
                pass

        x=1
        while x==1:
            time.sleep(0.05)
            while 1:
                time.sleep(0.05)
                try:
                    sp= json.load(open("entry_trader.json"))
                    if sp['st']>0:
                        new_st=sp['st']
                        for i in self.alive_positions:
                            self.alive_positions[i]['st']=new_st
                            
                        for i in self.alive_positions:
                            self.detail_accuonts[i]['st']=new_st
                            
                    if sp["propertise"]['sl']>0:
                        new_sl=sp["propertise"]['sl']
                        
                        for i in self.alive_positions:
                            self.alive_positions[i]['sl']=new_sl
                            
                        for i in self.alive_positions:
                            self.detail_accuonts[i]['sl']=new_sl
                            
                    if (sp["propertise"]['sl']>0) or (sp['st']>0):
                        while 1:
                            try:
                                sp["propertise"]['sl']=0
                                sp['st']=0
                                json.dump(sp, open('entry_trader.json','w'))
                                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                                break
                            except Exception as error:
                                pass
                    break
                    
                except Exception as error:
                    pass
            if (type(sp['stop_trail'])==int) and (type(sp['stopPrice_sl'])==int):
                if (sp['stop_trail']>0) or (sp['stopPrice_sl']>0):
                    while 1:
                        time.sleep(0.05)
                        try:
                            json.dump({"status":1}, open('get_ok.json','w'))
                            break
                        except Exception as error:
                            pass
                    self.sl_tp=sp
            for i in [*self.alive_positions]:
                self.detail_accuonts[i]['last_time']=str(datetime.datetime.utcnow())
            for i in [*self.alive_positions]:
                self.alive_positions[i]['stop_trail']=(1+(self.alive_positions[i]['st']/self.alive_positions[i]['leverage']))\
                *self.alive_positions[i]['trailprice'] + self.alive_positions[i]['actionprice']*self.commission

            self.touched_sl=[*{key:value for key,value in self.alive_positions.items() if value['stopPrice_sl']>=self.price}]
            self.touched_st=[*{key:value for key,value in self.alive_positions.items() if value['stop_trail']<=self.price}]

            if (len(self.touched_sl)>0) or (self.sl_tp['stopPrice_sl']>0):
                
                self.touched_sl=[*self.alive_positions]
                print('touch sl')
                
                for i in self.touched_sl:
                    self.alive_positions[i]['lastprice']=self.price
                    self.alive_positions[i]['PNL']= ((self.alive_positions[i]['lastprice']-self.alive_positions[i]['actionprice'])\
                    /self.alive_positions[i]['actionprice'])*100
                while 1:
                    time.sleep(0.05)
                    try:
                        if os.path.isfile("pnl_traders.json"):
                            pnl_traders=json.load(open("pnl_traders.json"))
                            break
                        else:
                            pnl_traders={}
                            json.dump(pnl_traders, open('pnl_traders.json', 'w'))
                            break
                    except Exception as error:
                        pass


                if len(pnl_traders)!=0:
                    l=len(pnl_traders)
                    pnl_traders['%s'%(l+1)]=self.alive_positions
                else:
                    pnl_traders={}
                    l=len(pnl_traders)
                    pnl_traders['%s'%(l+1)]=self.alive_positions
                json.dump(pnl_traders, open('pnl_traders.json', 'w'))
                
                threads_sl=[]
                for i in self.touched_sl:
                    self.touched_sl.remove(i)
                    user=i
                    thread=threading.Thread(target=self.control_sl,args=(i,
                    self.alive_positions[i]['leverage'],self.alive_positions[i]['side'],))
                    thread.start()
                    threads_sl.append(thread)
                for thread in threads_sl:
                    thread.join()
                while 1:
                    time.sleep(0.05)
                    try:
                        self.sl_tp=json.load(open("entry_trader.json"))
                        break
                    except Exception as error:
                        pass
                    
                
                self.sl_tp['stopPrice_sl']=0
                self.sl_tp['stop_trail']=0
                json.dump(self.sl_tp, open('entry_trader.json', 'w'))
                print(12)

            elif len([*self.alive_positions])==0:
                print(16)
                break

            elif (len(self.touched_st)>0) or (self.sl_tp['stop_trail']>0):

                self.touched_st=[*self.alive_positions]
                print('touch st')
                for i in self.touched_st:
                    self.alive_positions[i]['stopPrice_sl']=(1-(self.alive_positions[i]['sl']/self.alive_positions[i]['leverage']))\
                    *self.price + self.alive_positions[i]['actionprice']*self.commission
                    
                cho=[*self.alive_positions][0]
                print('action price: ',self.alive_positions[cho]['trailprice'])
                print("stop_trail: ",self.alive_positions[cho]['stop_trail'])
                print('stopPrice_sl: ',self.alive_positions[cho]['stopPrice_sl'])
                while 1:
                    time.sleep(0.05)
                    try:
                        json.dump({"action_price":self.alive_positions[cho]['trailprice'],
                                   "stop_trail":self.alive_positions[cho]['stop_trail'],
                                   "stopPrice_sl":self.alive_positions[cho]['stopPrice_sl']},
                                  open('watch_position.json','w'))
                        break
                    except Exception as error:
                        pass
                threads_st=[]
                for i in self.touched_st:
                    self.touched_st.remove(i)
                    user=i
                    thread=threading.Thread(target=self.control_stoptrail,args=(i,
                    round(self.alive_positions[i]['stopPrice_sl'],self.rond),))
                    
                    thread.start()
                    threads_st.append(thread)
                for thread in threads_st:
                    thread.join()
                
                for i in self.alive_positions:
                    self.detail_accuonts[i]['stop_trail']=self.alive_positions[i]['stop_trail']
                    
                self.alive_positions={key:value for key,value in self.detail_accuonts.items() if value['status']==1}
                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                while 1:
                    time.sleep(0.05)
                    try:
                        self.sl_tp=json.load(open("entry_trader.json"))
                        break
                    except Exception as error:
                        pass
                
                self.sl_tp['stopPrice_sl']=0
                self.sl_tp['stop_trail']=0

                json.dump(self.sl_tp, open('entry_trader.json', 'w'))

        return

    def control_position_sell(self):
        
        self.touched_st=[]
        self.touched_sl=[]
        self.sl_tp={'stop_trail':0,'stopPrice_sl':0}
        cho=[*self.alive_positions][0]
        print('action price: ',self.alive_positions[cho]['trailprice'])
        print("stop_trail: ",self.alive_positions[cho]['stop_trail'])
        print('stopPrice_sl: ',self.alive_positions[cho]['stopPrice_sl'])
        while 1:
            time.sleep(0.05)
            try:
                json.dump({"action_price":self.alive_positions[cho]['trailprice'],
                           "stop_trail":self.alive_positions[cho]['stop_trail'],
                           "stopPrice_sl":self.alive_positions[cho]['stopPrice_sl']},
                          open('watch_position.json','w'))
                break
            except Exception as error:
                pass
        print('control sell')
        x=1
        while x==1:
            time.sleep(0.05)
            while 1:
                time.sleep(0.05)
                try:
                    sp= json.load(open("entry_trader.json"))
                    if sp['st']>0:
                        new_st=sp['st']
                        for i in self.alive_positions:
                            self.alive_positions[i]['st']=new_st
                            
                        for i in self.alive_positions:
                            self.detail_accuonts[i]['st']=new_st
                            
                    if sp["propertise"]['sl']>0:
                        new_sl=sp["propertise"]['sl']
                        
                        for i in self.alive_positions:
                            self.alive_positions[i]['sl']=new_sl
                            
                        for i in self.alive_positions:
                            self.detail_accuonts[i]['sl']=new_sl
                            
                    if (sp["propertise"]['sl']>0) or (sp['st']>0):
                        while 1:
                            try:
                                sp["propertise"]['sl']=0
                                sp['st']=0
                                json.dump(sp, open('entry_trader.json','w'))
                                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                                break
                            except Exception as error:
                                pass
                    break
                except Exception as error:
                    pass
            
            if (type(sp['stop_trail'])==int) and (type(sp['stopPrice_sl'])==int):
                if (sp['stop_trail']>0) or (sp['stopPrice_sl']>0):
                    while 1:
                        time.sleep(0.05)
                        try:
                            json.dump({"status":1}, open('get_ok.json','w'))
                            break
                        except Exception as error:
                            pass
                    self.sl_tp=sp
                    
            for i in [*self.alive_positions]:
                self.detail_accuonts[i]['last_time']=str(datetime.datetime.utcnow())
            
            for i in [*self.alive_positions]:
                self.alive_positions[i]['stop_trail']=(1-(self.alive_positions[i]['st']/self.alive_positions[i]['leverage']))\
                *self.alive_positions[i]['trailprice'] - self.alive_positions[i]['actionprice']*self.commission

            self.touched_sl=[*{key:value for key,value in self.alive_positions.items() if value['stopPrice_sl']<=self.price}]
            self.touched_st=[*{key:value for key,value in self.alive_positions.items() if value['stop_trail']>=self.price}]

            if (len(self.touched_sl)>0) or (self.sl_tp['stopPrice_sl']>0):

                print('touch sl')

                self.touched_sl=[*self.alive_positions]

                for i in self.touched_sl:
                    self.alive_positions[i]['lastprice']=self.price
                    self.alive_positions[i]['PNL']= ((self.alive_positions[i]['actionprice']-self.alive_positions[i]['lastprice'])\
                    /self.alive_positions[i]['actionprice'])*100
                while 1:
                    time.sleep(0.05)
                    try:
                        if os.path.isfile("pnl_traders.json"):
                            pnl_traders=json.load(open("pnl_traders.json"))
                            break
                        else:
                            pnl_traders={}
                            json.dump(pnl_traders, open('pnl_traders.json', 'w'))
                            break
                    except Exception as error:
                        pass

                if len(pnl_traders)!=0:
                    l=len(pnl_traders)
                    pnl_traders['%s'%(l+1)]=self.alive_positions
                else:
                    pnl_traders={}
                    l=len(pnl_traders)
                    pnl_traders['%s'%(l+1)]=self.alive_positions
                json.dump(pnl_traders, open('pnl_traders.json', 'w'))

                threads_sl=[]
                for i in self.touched_sl:
                    self.touched_sl.remove(i)
                    user=i
                    thread=threading.Thread(target=self.control_sl,args=(i,
                    self.alive_positions[i]['leverage'],self.alive_positions[i]['side'],))
                    thread.start()
                    threads_sl.append(thread)
                for thread in threads_sl:
                    thread.join()
                print(21)

                while 1:
                    time.sleep(0.05)
                    try:
                        self.sl_tp=json.load(open("entry_trader.json"))
                        break
                    except Exception as error:
                        pass
                self.sl_tp['stopPrice_sl']=0
                self.sl_tp['stop_trail']=0
                json.dump(self.sl_tp, open('entry_trader.json', 'w'))
                print(19)

            elif len([*self.alive_positions])==0:
                print(20)
                break

            elif (len(self.touched_st)>0) or (self.sl_tp['stop_trail']>0):

                print('touch st')
                self.touched_st=[*self.alive_positions]
                for i in self.touched_st:
                    self.alive_positions[i]['stopPrice_sl']=(1+(self.alive_positions[i]['sl']/self.alive_positions[i]['leverage']))\
                    *self.price - self.alive_positions[i]['actionprice']*self.commission
                
                cho=[*self.alive_positions][0]
                print('action price: ',self.alive_positions[cho]['trailprice'])
                print("stop_trail: ",self.alive_positions[cho]['stop_trail'])
                print('stopPrice_sl: ',self.alive_positions[cho]['stopPrice_sl'])
                while 1:
                    time.sleep(0.05)
                    try:
                        json.dump({"action_price":self.alive_positions[cho]['trailprice'],
                                   "stop_trail":self.alive_positions[cho]['stop_trail'],
                                   "stopPrice_sl":self.alive_positions[cho]['stopPrice_sl']},
                                  open('watch_position.json','w'))
                        break
                    except Exception as error:
                        pass
                
                threads_st=[]
                for i in self.touched_st:
                    self.touched_st.remove(i)
                    user=i
                    thread=threading.Thread(target=self.control_stoptrail,args=(i,
                    round(self.alive_positions[i]['stopPrice_sl'],self.rond),))
                    thread.start()
                    threads_st.append(thread)
                for thread in threads_st:
                    thread.join()
                    
                for i in self.alive_positions:
                    self.detail_accuonts[i]['stop_trail']=self.alive_positions[i]['stop_trail']
                    
                self.alive_positions={key:value for key,value in self.detail_accuonts.items() if value['status']==1}
                json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))
                
                while 1:
                    time.sleep(0.05)
                    try:
                        self.sl_tp=json.load(open("entry_trader.json"))
                        break
                    except Exception as error:
                        pass

                self.sl_tp['stopPrice_sl']=0
                self.sl_tp['stop_trail']=0
                

                json.dump(self.sl_tp, open('entry_trader.json', 'w'))
                print(23)
        return

    def user_get(self):
        while 1:
            time.sleep(0.05)
            try:
                if os.path.isfile("entry_trader.json"):
                    entry_trader=json.load(open("entry_trader.json"))
                    break
                else:
                    entry_trader={"st": 0, "leverage": 0, "sl": 0, "sellorbuy": None,'stopPrice_sl':0,'stop_trail':0,
                                  'symbol':'XRPUSDTM',"get_signal":0,
                                  "propertise":{"sl":0.03,"number_user":None,'rond':None,
                                                "token_machin":None,
                                                'commission':None, "number_user_proxy":8 ,'change_st_leverage':0 ,
                                                "limit_money":100}}
                    json.dump(entry_trader, open('entry_trader.json', 'w'))
                    break
            except Exception as error:
                pass

            
        os_type = sys.platform.lower()
        command=None
        if "darwin" in os_type:
            command = "ioreg -l | grep IOPlatformSerialNumber"
        elif "win" in os_type:
            command = "wmic bios get serialnumber"
        elif "linux" in os_type:
            command = "dmidecode -s baseboard-serial-number"
        self.id=list(os.popen(command).read().replace("\n", "").replace("  ", "").replace(" ", ""))

        nu=[int(i) for i in self.id if i.isdigit()]
        plusone=[i+1 for i in nu]
        minuseone=[i-1 for i in nu]
        plustwo=[i+2 for i in nu]
        plusthree=[i+4 for i in nu]
        minusetwo=[i-3 for i in nu]
        minusethree=[i-2 for i in nu]
        allnumber=plusone+minuseone+plustwo+plusthree +minusetwo+minusethree
        allnumber=[i for i in allnumber if (i<10) and (i>0)]
        allnumber=[str(i) for i in allnumber]
        me=0
        while 1:
            time.sleep(0.05)
            try:
                entry_trader=json.load(open("entry_trader.json"))
                if entry_trader["propertise"]['token_machin']!=None:
                    break
                elif me==0:
                    print("enter your key")
                    me=1
            except Exception as error:
                pass

        id_cheke=None
        self.runpricetr=0
        for i in allnumber:
            if i not in entry_trader["propertise"]['token_machin']:
                id_cheke=False
                break
        if id_cheke==False:
            command=None
        else:
            self.runpricetr=1
            
        if (command==None) and (self.id==None):
            json.dump({"st": 0, "leverage": 0, "sl": 0, "sellorbuy": None,'stopPrice_sl':0,'stop_trail':0,
                          'symbol':'XRPUSDTM',"get_signal":0,
                          "propertise":{"sl":0.03,"number_user":None,'rond':None,"token_machin":None,
                                        'commission':None, "number_user_proxy":8 ,'change_st_leverage':0 ,
                                        "limit_money":100}},
                      open('entry_trader.json', 'w'))
        allnumber=allnumber + list(entry_trader["propertise"]['token_machin'][-2::])
        return allnumber,entry_trader

    def control_position(self):
        
        allnumber,entry_trader=self.user_get()
        while 1:
            time.sleep(0.05)
            try:
                entry_trader=json.load(open("entry_trader.json"))
                if entry_trader["propertise"]['token_machin']!=None:
                    break
            except Exception as error:
                pass

        id_cheke=None
        dic=None
        for i in allnumber:
            if i not in entry_trader["propertise"]['token_machin']:
                id_cheke=False
                break

        for k,v in self.chek_dic.items():
            if entry_trader["propertise"]['token_machin'][int(k)]!=self.chek_dic[k]:
                dic=False
                break
                
        numsecond=[int(i) for i in allnumber]
        numsecond=((sum(numsecond))*2-748)**2
        t=entry_trader["propertise"]['token_machin'].split(":")
        t=[i for i in t[1] if i.isdigit()]
        t=int(("".join(t))[0:-2])
        if t!=numsecond:
            dic=False
            print("dic: ",dic)
        x=1
        if (id_cheke==False) or (dic==False):
            print(id_cheke,dic)
            x=0
        else:
            self.detail_accuonts=self.creat_accuont()
        while id_cheke==None:
            time.sleep(0.05)
            try:
                self.lot_size()
                if len(self.multiplier)!=0:
                    print('get_lot_size')
                    break
            except Exception as error:
                print(error)
        
        entry_trader["propertise"]['number_user']=len([*self.detail_accuonts])
        json.dump(entry_trader, open('entry_trader.json', 'w'))

        if (id_cheke!=False) or (dic!=False):
            thread=threading.Thread(target=self.runprice)
            thread.start()
            thread=threading.Thread(target=self.refresh_runprice)
            thread.start()

        print('x=',x)
        while x==1:
            time.sleep(0.05)
            while x==1:
                time.sleep(0.05)
                if self.price==None:
                    time.sleep(5)
                elif self.price!=None:
                    break
            if len([*self.detail_accuonts])>0:

                # -----------------------------------------------------------------------

                if (len([*{key:value for key,value in self.detail_accuonts.items() if value['status']>0}])==0):

                    self.multi_threading(func=self.account_overview,accuonts=[*self.detail_accuonts])
                    json.dump(self.detail_accuonts, open('detail_accuonts.json', 'w'))

                # -----------------------------------------------------------------------

                if (len([*{key:value for key,value in self.detail_accuonts.items() if value['status']>0}])==0):
                    self.open_order()
                # -----------------------------------------------------------------------

                if (len([*{key:value for key,value in self.detail_accuonts.items() if value['status']>0}])>0):
                    print ('start control position')
                    self.alive_positions={key:value for key,value in self.detail_accuonts.items() if value['status']>0}
                    print("open position and control it for %s users"% len(self.alive_positions))

                    for i in [*self.alive_positions]:
                        if self.alive_positions[i]['side']=='buy':
                            side='buy'
                            break
                        elif self.alive_positions[i]['side']=='sell':
                            side='sell'
                            break

                    if side=='buy':
                        self.control_position_buy()

                    elif side=='sell':
                        self.control_position_sell()

            # -----------------------------------------------------------------------
            self.multi_threading(func=self.check_exist_alive_position,accuonts=[*self.detail_accuonts])

            while 1:
                time.sleep(0.05)
                try:
                    user=json.load(open('users.json'))
                    entry_trader=json.load(open("entry_trader.json"))
                    break
                except Exception as error:
                    pass
            
            no_permision={k:v for k,v in user.items() if v["permission"]==0}
            self.detail_accuonts={k:v for k,v in self.detail_accuonts.items() if k not in no_permision}
            entry_trader["propertise"]['number_user']=[*self.detail_accuonts]
            json.dump(entry_trader, open('entry_trader.json', 'w'))
            
            self.new_user()
        return
    
me=0 
while 1:
    time.sleep(0.05)
    try:
        entry_trader=json.load(open("entry_trader.json"))
    except Exception as error:
        pass
    if entry_trader["propertise"]['token_machin']!=None:
        break
    elif me==0:
        print("send below serial number")
        os_type = sys.platform.lower()
        command=None
        if "darwin" in os_type:
            command = "ioreg -l | grep IOPlatformSerialNumber"
        elif "win" in os_type:
            command = "wmic bios get serialnumber"
        elif "linux" in os_type:
            command = "dmidecode -s baseboard-serial-number"
        print(os.popen(command).read().replace("\n", "").replace("  ", "").replace(" ", ""))
        me+=1

g=0
try:
    s = socket.socket()
    host = socket.gethostname()
    port = 12346
    s.bind((host, port))
    trade=trader()
    g=1
    trade.control_position()
except Exception as error:
    print(error)
    if g==0:
        print("more program")
        time.sleep(3)
    if g==1:
        trade.PrintException()
