import yfinance as yf
from portfolio.models import Ticker
from datetime import datetime
from yfinance_keys import char_keys, timestamp_keys, int_keys, float_keys




def get_tickers(tickers_list):
    tickers_str = ' '.join(tickers_list)
    return yf.Tickers(tickers_str)


def get_ticker_history(tickers_list, start="", end="", period='1mo', interval='1d', group_by='ticker'):
    tickers = get_tickers(tickers_list)
    history = tickers.download(period=period, interval=interval,group_by=group_by)
    return history


def get_entry(ticker_obj):
    info = ticker_obj.info
    entry = {}

    def try_add_to_entry(entry_key, info_key=''):
        if not info_key:
            info_key=entry_key
        try:
            entry[entry_key] = info[info_key]
        except:
            entry[entry_key] = None

    # char
    for key in char_keys:
        try_add_to_entry(key)
    # int
    for key in int_keys:
        try_add_to_entry(key)
    # float
    for key in float_keys:
        try_add_to_entry(key)
    # timestamp
    for key in timestamp_keys:
        try:
            timestamp = info[key]
            dt_obj = datetime.fromtimestamp(timestamp)
            dt_str = dt_obj.strftime("%Y-%m-%d")
            entry[key] = dt_str
        except:
            entry[key] = None
    # manual
    try_add_to_entry('t_yield','yield')
    try_add_to_entry('fiftyTwoWeekChange', '52WeekChange')
    return entry


def store_ticker_info(tickers_list):
    tickers = get_tickers(tickers_list)
    symbols = tickers.symbols
    for ticker_symbol, ticker_obj in zip(symbols, tickers.tickers):
        db_entries_for_ticker = Ticker.objects.filter(symbol=ticker_symbol)
        entry = get_entry(ticker_obj)
        # create
        if len(db_entries_for_ticker) == 0:
            Ticker.objects.create(**entry)
        # update
        else:
            existing = Ticker.objects.get(symbol=ticker_symbol)
            for field, value in entry.items():
                setattr(existing, field, value)
            existing.save()

