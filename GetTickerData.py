import asyncio
import logging
import gzip
from io import BytesIO
from datetime import datetime
from aiowebsocket.converses import AioWebSocket
import json
import sqlite3
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

conn = sqlite3.connect('btc_tick.db')
cursor = conn.cursor()
cursor.execute('create table if not exists tick (tradeId varchar(20) primary key, price float, amount float, ts bigint, direction varchar(20))')
cursor.close()
conn.commit()

async def startup(uri) :
    async with AioWebSocket(remote) as aws :
        converse = aws.manipulator
        
        reqMsg = json.dumps({'sub':'market.btcusdt.trade.detail', 'id':1})
        await converse.send(reqMsg)
        while True:
            rec = await converse.receive()
            buff = BytesIO(rec)
            f = gzip.GzipFile(fileobj=buff)
            res = f.read().decode('utf-8')
            rj = json.loads(res)
            if 'ping' in rj :
                backmsg = json.dumps({'pong':rj['ping']})
                await converse.send(backmsg)
                print(res, backmsg)
            if 'tick' in rj :
                cursor = conn.cursor()
                for tick in rj['tick']['data'] :
                    try :
                        cursor.execute('insert into tick (tradeId, price, amount, ts, direction) values (?,?,?,?,?)', (tick['tradeId'], tick['price'], tick['amount'], tick['ts'], tick['direction']))
                    except sqlite3.IntegrityError :
                        print(sqlite3.IntegrityError)
                cursor.close()
                conn.commit()
                print(rj['tick']['data'])
            else :
                print(rj)
            
    # async with AioWebSocket(uri) as aws :
    #     converse = aws.manipulator
    #     message =  '{"action":"subscribe","args":["QuoteBin5m:14"]}'
    #     await converse.send(message)
    #     print('{time}-Client send: {message}'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message=message))
    #     while True:
    #         mes = await converse.receive()
    #         print('{time}-Client receive: {rec}'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes))

if __name__ == '__main__' :
    logging.basicConfig(level=logging.DEBUG)
    
    remote = 'wss://api.huobi.pro/ws'

    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc :
        logging.info('Quit.')