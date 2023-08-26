import requests
from datetime import datetime

def unix1(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def unix2(time_str):
    current_date = datetime.now().date()
    hours, minutes = map(int, time_str.split(":"))
    combined_datetime = datetime(current_date.year, current_date.month, current_date.day, hours, minutes)
    return int(combined_datetime.timestamp() * 1000)


input_list = []
input_taker = None

print("Enter trade details:")
while input_taker != "":
    input_taker = input()
    input_list.append(input_taker)

long_short = input_list[0].split("-")[0].replace(" ", "").strip()
coin = input_list[1].split(":")[1].replace(" ", "").strip()
timeframe_minutes = str(input_list[2].split(":")[1].replace(" ", "").strip())
price = float(input_list[3].split(":")[1].replace(" ", "").strip())
take_profit = float(input_list[4].split(":")[1].replace(" ", "").strip())
stop_loss = float(input_list[5].split(":")[1].replace(" ", "").strip())
normal_entry_time = input_list[6].replace(" ", "").strip()
entry_time = unix2(input_list[6].replace(" ", "").strip())

print("Take Profit:", take_profit)
print("Stop Loss:", stop_loss)
print("Entry Time:", normal_entry_time)
print(f"Entry Time (Unix Timestamp): {entry_time}\n////////////////////////////////////////")

def fetch_and_analyze_data(trading_pair, interval, entry_time):
    response = requests.get(f'https://api.binance.com/api/v3/klines',
                            params={'symbol': trading_pair, 'interval': interval, 'limit': 1000})
    historical_data = response.json()

    entry_index = None
    for i, candle in enumerate(historical_data):
        timestamp = int(candle[0])
        if timestamp >= entry_time:
            entry_index = i
            break

    if entry_index is not None:
        entry_candle = historical_data[entry_index]
        print(f"Entry Candle Historical Data: {entry_index}\n////////////////////////////////////////")
        print("Entry Candle Data:")
        print("Time: ", unix1(entry_candle[0]))
        print("Open Price:", format(float(entry_candle[1]), 'g'))
        print("High Price:", format(float(entry_candle[2]), 'g'))
        print("Low Price:", format(float(entry_candle[3]), 'g'))
        print("Close Price:", format(float(entry_candle[4]), 'g'))
        print("Volume:", format(float(entry_candle[5]), 'g'))
        print("Close Time Stamp:", unix1(entry_candle[6]))
        formatted_quote_asset_volume = "{:.2f}".format(float(entry_candle[7]))
        print("Quote Asset Volume:",  formatted_quote_asset_volume)
        print("Number Of Trades:", entry_candle[8])
        print("Taker Buy Base Asset Volume:", format(float(entry_candle[9]), 'g'))
        print("Taker Buy Quote Asset Volume:", format(float(entry_candle[10]), 'g'))
        print(f"Ignore:{entry_candle[11]}\n////////////////////////////////////////")

        close_price = float(entry_candle[4])
        if close_price >= take_profit:
            print("Take Profit Condition Met")
        elif close_price <= stop_loss:
            print("Stop Loss Condition Met")
        elif close_price >= stop_loss and close_price <= take_profit:
            print("Neither Stop Loss Condition or Take Profit condition is met.")
    else:
        print("Entry time not found in historical data")

trading_pair = coin
interval = timeframe_minutes
fetch_and_analyze_data(trading_pair, interval, entry_time)
