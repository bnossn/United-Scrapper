# https://www.youtube.com/watch?v=YKennHXZyJU&ab_channel=Codifike
from bs4 import BeautifulSoup
import requests
import smtplib
import email.message

URL = "https://www.brasiltronic.com.br/kit-camera-sony-alpha-a6600-com-lente-sony-e-pz-18-105mm-f-4-g-oss-p1328183"

# Google -> "my browser agent"
headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

site = requests.get(URL, headers=headers)

soup = BeautifulSoup(site.content, 'html.parser')

title = soup.find('h1', class_ = 'col-12 name no-medium').getText().strip()
price = soup.find('strong', class_ = 'sale-price')
price = price.contents[1].getText().strip()

num_price = price[3:]
num_price = num_price.replace('.','')
num_price = num_price.replace(',','.')
num_price = float(num_price)

def send_email():
	email_content = "https://www.brasiltronic.com.br/kit-camera-sony-alpha-a6600-com-lente-sony-e-pz-18-105mm-f-4-g-oss-p1328183"
	msg = email.message.Message()
	msg['Subject'] = "Preço Camera Sony BAIXOU!!!"
	msg['From'] = 'meuemail@gmail.com'
	msg['To'] = 'meuemail@gmail.com'
	password = 'meupassword'
	msg.add_header('Content-Type', 'text/html')
	msg.set_payload(email_content)

	s = smtplib.SMTP('smtp.gmail.com : 587')
	s.startls()
	s.login(msg['From'], password)
	s.sendmail(msg['From'], [msg['To']], msg.as_string())

if (num_price < 15000):
	send_email()

