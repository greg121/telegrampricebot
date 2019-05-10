import requests 
import json 
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import datetime
import configparser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')
updater = Updater(token=config['DEFAULT']['telegram_token'])
dispatcher = updater.dispatcher

def get_timestamp(days):
	yesterday = datetime.date.today() - datetime.timedelta(days)
	unix_time= yesterday.strftime("%s")	
	return unix_time

def get_hist_price(timestamp):
	url = "https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&tsyms=USD&ts="+timestamp
	r = requests.get(url)
	cryptocompare = json.loads(r.text)
	price_old = cryptocompare['BTC']['USD']
	return price_old

def get_price(market, pair):
	url = "https://api.cryptowat.ch/markets/"+market+"/"+pair+"/price"
	r = requests.get(url)
	cryptowatch = json.loads(r.text)
	price = cryptowatch['result']['price']
	return price

def btc(bot, update):
	price_today = get_price("bitstamp", "btcusd")

	timestamp_yesterday = get_timestamp(1)
	price_yesterday = get_hist_price(timestamp_yesterday)
	change_yesterday = (price_today - price_yesterday) / price_yesterday * 100
	emoji_yesterday = ""
	if (change_yesterday > 0):
		emoji_yesterday = "\U00002600"
	else:
		emoji_yesterday = "\U00002614"

	timestamp_last_week = get_timestamp(7)
	price_last_week = get_hist_price(timestamp_last_week)
	change_last_week = (price_today - price_last_week) / price_last_week * 100
	emoji_last_week = ""
	if (change_last_week > 0):
		emoji_last_week = "\U00002600"
	else:
		emoji_last_week = "\U00002614"

	timestamp_last_year = get_timestamp(365)
	price_last_year = get_hist_price(timestamp_last_year)
	change_last_year = (price_today - price_last_year) / price_last_year * 100
	emoji_last_year = ""
	if (change_last_year > 0):
		emoji_last_year = "\U00002600"
	else:
		emoji_last_year = "\U00002614"
	bot.send_message(chat_id=update.message.chat_id, text="BTC   $"+str(price_today)+"\n24h   "+ format(change_yesterday, '.2f')+ "% "+emoji_yesterday+"\n7d     "+ format(change_last_week, '.2f')+ "% "+emoji_last_week+"\n1y     "+ format(change_last_year, '.2f')+ "% "+emoji_last_year)
	custom_keyboard = [['top-left', 'top-right'], 
                   ['bottom-left', 'bottom-right']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.send_message(chat_id=update.message.chat_id, text="Custom Keyboard Test", reply_markup=reply_markup)
	
	
btc_handler = CommandHandler('btc', btc)
dispatcher.add_handler(btc_handler)

def eth(bot, update):
	url = "https://api.cryptowat.ch/markets/bitstamp/ethusd/price"
	r = requests.get(url)
	cryptowatch = json.loads(r.text)
	price = str(cryptowatch['result']['price'])
	bot.send_message(chat_id=update.message.chat_id, text="$"+price)

eth_handler = CommandHandler('eth', eth)
dispatcher.add_handler(eth_handler)

updater.start_polling()
