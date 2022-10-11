import requests
from hyper.contrib import HTTP20Adapter
from bs4 import BeautifulSoup as BS
import re
import time
import telebot


# group_id = '-208547998'
# file_name = 'last_text.txt'
PUBLIC_ID = -1001870401279
TOKEN_BOT = '2137380397:AAE5M-KsMuWxMQtJftw1WA4rhYJtWLrPRz4'

bot = telebot.TeleBot(TOKEN_BOT)



while True:
	s = requests.session()
	s.mount('https://', HTTP20Adapter())
	# r = s.get('https://www.avito.ru/')
	# r = s.get('https://www.avito.ru/ekaterinburg/telefony?cd=1&d=1&f=ASgCAQECAUD2vA0UktI0AUXGmgwUeyJmcm9tIjowLCJ0byI6NzAwMH0&p=16&s=104&user=1')
	r = s.get('https://www.avito.ru/volgogradskaya_oblast_volzhskiy/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?cd=1&s=104&user=1')
# 	print(r.status_code)
	r.encoding = 'utf-8'
	# f = open('if.html', 'w')
	# f.write(r.text)
	# f.close()

	html = BS(r.content, 'html.parser')
	items = html.select('.iva-item-titleStep-pdebR > a > h3')
	items_links = html.select('.iva-item-titleStep-pdebR > a')
	items_prices = html.select('.iva-item-priceStep-uq2CQ > span > span > span')

	# print(items)
	# Телефон iPhone 12 pro 128 Silver RU/A
	# for it in items:
	TITLE = str(items[0])[168:-5]
	res = re.search(r'href="\S*"', str(items_links[0]))
	# print(str(items_links[0]))
	LINK = res.group(0)[6:-1]
	# print(LINK)
	PRICE = str(items_prices[0])[65:-59]
	# if ' ' in PRICE:
	# 	PRICE = PRICE.replace(' ', '')


	# print(PRICE+'₽')
	DATA_ID = int(re.search(r'_\d*&', LINK+'&').group(0)[1:-1])
	# print(DATA_ID)

	try:
		f = open('lastid.txt')
		key = f.read()
		lastid = key
		if key == '':
			f.close()
			f = open('lastid.txt', 'w')
			f.write('0')
			lastid = '0'
		f.close()
	except:
		f = open('lastid.txt', 'w')
		f.write('0')
		f.close()
		lastid = '0'


	if DATA_ID != int(lastid):
# 		print(TITLE, PRICE+'₽', 'https://www.avito.ru'+LINK, DATA_ID, sep='\n')
		bot.send_message(PUBLIC_ID, TITLE+'\n✅'+PRICE+'₽\nhttps://www.avito.ru'+LINK+'\n\nid'+str(DATA_ID))

		f = open('lastid.txt', 'w')
		f.write(str(DATA_ID))
		f.close()


	# <span class="price-text-_YGDY text-text-LurtD text-size-s-BxGpL">
	# <!-- --> <span class="price-currency-_FNLV">₽</span></span>
	time.sleep(100)
