from config import api_key, api_secret
from pybit.unified_trading import HTTP
from pybit.unified_trading import WebSocket
from time import sleep



def ws_trade(level):
    ws = WebSocket(testnet=False, channel_type="linear")
    data = None  # Объявляем переменную для хранения данных
    ws.trade_stream(symbol="BTCUSDT",callback=lambda message: process_message(message))
    sum_of_vol = 0

    def process_message(message):
       nonlocal data  # Объявляем переменную из внешней области видимости
       data = message  # Сохраняем данные в переменной

    while True:
       if data is not None:
           inf = data['data']
           price = float(inf[0]['p'])
           volume = float(inf[0]['v'])
           sum_of_vol += volume
           print(f'price= {price} vol= {volume} sum_vol= {sum_of_vol}')
           data = None  # Сбрасываем переменную для следующего сообщения
       sleep(0.5)











def create_order():
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)
    print(session.place_order(
        category="linear",
        symbol="XRPUSDT",
        side="Buy",
        orderType="Limit",
        qty="10",
        price="0.5",
        timeInForce="PostOnly",
        orderLinkId="xrp",
        isLeverage=0,
        orderFilter="Order", ))


def get_position():
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)
    print(session.get_positions(
        category="linear",
        symbol=None,
        settleCoin='USDT'
    ))


def get_open_orders():
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)
    result = (session.get_open_orders(
        category="linear",
        symbol=None,
        settleCoin='USDT',
        limit=50, ))
    print(type(result))
    print(result)


# есть открытый ордер{'retCode': 0, 'retMsg': 'OK', 'result': {'list': [{'orderId': '86266634-7b1c-44de-be92-7aaa5fa6b745', 'orderLinkId': '', 'blockTradeId': '', 'symbol': 'XRPUSDT', 'price': '0.0000', 'qty': '10', 'side': 'Buy', 'isLeverage': '', 'positionIdx': 0, 'orderStatus': 'Untriggered', 'cancelType': 'UNKNOWN', 'rejectReason': 'EC_NoError', 'avgPrice': '0', 'leavesQty': '10', 'leavesValue': '0', 'cumExecQty': '0', 'cumExecValue': '0', 'cumExecFee': '0', 'timeInForce': 'IOC', 'orderType': 'Market', 'stopOrderType': 'Stop', 'orderIv': '', 'triggerPrice': '0.5103', 'takeProfit': '0.5140', 'stopLoss': '0.5080', 'tpTriggerBy': 'LastPrice', 'slTriggerBy': 'LastPrice', 'triggerDirection': 1, 'triggerBy': 'LastPrice', 'lastPriceOnCreated': '0.5069', 'reduceOnly': False, 'closeOnTrigger': False, 'smpType': 'None', 'smpGroup': 0, 'smpOrderId': '', 'tpslMode': '', 'tpLimitPrice': '', 'slLimitPrice': '', 'placeType': '', 'createdTime': '1685649236726', 'updatedTime': '1685649236726'}], 'nextPageCursor': 'page_args%3D86266634-7b1c-44de-be92-7aaa5fa6b745%26', 'category': 'linear'}, 'retExtInfo': {}, 'time': 1685649526896}
# not orders         {'retCode': 0, 'retMsg': 'OK', 'result': {'list': [], 'nextPageCursor': '', 'category': 'linear'}, 'retExtInfo': {}, 'time': 1685649664849}
def get_closet_pnl():
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)
    print(session.get_closed_pnl(
        category="linear",
        limit=50))


def recent_trade():
    session = HTTP(testnet=False)
    print(session.get_public_trade_history(
        category="linear",
        symbol="BTCUSDT",
        limit=1,
    ))


if __name__ == '__main__':
    level = 30000
    # get_position()
    # get_closet_pnl()
    # get_open_orders()
    # recent_trade()
    ws_trade(level)
