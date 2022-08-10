import websockets
import asyncio
import json
import time


async def main():
    # url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    url = 'wss://ws.bitmex.com/realtime?subscribe=trade:XBTUSD'
    async with websockets.connect(url) as client:
        while True:
            try:
                data = json.loads(await client.recv())
                data = data['data']
                print(type(data))
                print(len(data))
                print (data)

            except KeyError:
                print('кейеррор')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())