from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import fake_useragent
import os


URL_IP = 'https://2ip.ru/'
GECKO_PATH = 'path to geckodriver'
BINARY_PATH = 'path to firefox'
TOR_PATH = 'path to tor'

print('tor start')
tor = Popen(TOR_PATH, shell=True, stdout=PIPE, bufsize=-1)
if tor.poll() is not None:
    raise Exception('No connection to tor :^(')
result_code = str(tor.stdout.readlines()[-1]).lower()
if 'failed' in result_code:
    print('tor process is already running or port is in use')
if 'done' in result_code:
    print('tor process created')
print('tor works')

options = Options()
options.binary_location = BINARY_PATH
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', '127.0.0.1')
options.set_preference('network.proxy.socks_port', 9050)
options.set_preference("network.proxy.socks_remote_dns", True)

fake_user = fake_useragent.UserAgent().random
options.set_preference('general.useragent.override', fake_user)

service = Service(executable_path=GECKO_PATH)

with Firefox(options=options, service=service) as driver:
    driver.get(url=URL_IP)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.find('div', {'class': 'ip'}).text.strip())
    print(soup.find_all('div', {'class': 'ip-icon-label'}))

tor.kill()
print('tor closed\ntor exit code = ' + str(tor.poll()))
