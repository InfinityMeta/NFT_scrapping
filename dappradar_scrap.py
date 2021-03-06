from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from csv import writer

orders = {
    'k': 3,
    'M': 6,
    'B': 9
}

csv_path = r"C://Users//maksi//OneDrive//Рабочий стол//nft analysis//nft_data.csv"

def string_modify(str):
    order = str[len(str) - 1]
    str = str[1:]
    if order in orders.keys():
        str = str[:len(str) - 1]
        if ',' in str:
            comma_index = str.index(',')
            figures_after_comma = len(str) - comma_index - 1
            str = str[:comma_index] + str[comma_index + 1:]
            mult = orders[order] - figures_after_comma
        else:
            mult = orders[order]
        value = float(str) * pow(10, mult)
    else:
        if ',' in str:
            comma_index = str.index(',')
            str = str[:comma_index] + '.' + str[comma_index + 1:]
        value = float(str)

    return value

def object_to_list(marketplace):
    data = []
    data.append(marketplace.name)
    data.append(marketplace.avg_price)
    data.append(marketplace.volume)
    str = ''
    for token in marketplace.tokens:
        str += token
        str += ','
    str = str[:len(str) - 1]
    if marketplace.name == 'NFTrade':
        str = 'AVALANCHE,BSC,ETH,Polygon'
    if marketplace.name == 'MegaCryptoPolis':
        str = 'ETH,Polygon,TRON'
    data.append(str)
    return data

def add_row_to_csv(row, csv_path):
    with open(csv_path, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()


class Marketplace:
    name = str
    avg_price = str
    volume = str
    traders = str
    tokens = []

    def __init__(self, name, avg_price, volume, traders, tokens):
        self.name = name
        self.avg_price = avg_price
        self.volume = volume
        self.traders = traders
        self.tokens = tokens

    def __repr__(self):
        return str(self.__dict__)

def page_scrapping(url):

    driver = Chrome()

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for element in soup.find_all(class_="sc-hAWBJg hluxYr"):

        name = element.find(class_="sc-eTwdGJ cXNCTf nft-name-link").text.strip()

        avg_price_and_change = element.find(class_="sc-aaqME gSjpiI rankings-column rankings-column__nft-avg-sale")
        avg_price = avg_price_and_change.find(class_="sc-iRFsWr RlZDC").text.strip()
        avg_price = string_modify(avg_price)

        volume_and_change = element.find(class_="sc-aaqME gSjpiI rankings-column rankings-column__nft-volume")
        volume = volume_and_change.find(class_="sc-iRFsWr RlZDC").text.strip()
        volume = string_modify(volume)

        traders_and_change = element.find(class_="sc-aaqME gSjpiI rankings-column rankings-column__nft-traders")
        traders = traders_and_change.find(class_="sc-iRFsWr RlZDC")
        if traders is None:
            traders = 0
        else:
            traders = traders.text.strip()
            if traders.find('') > -1:
                traders = ''.join(traders.split())

        tokens = []
        currency = element.find(class_="sc-hKumaY hakoVN")
        for token_type in currency.find_all(class_="sc-jwQYvw enEXyf"):
            tokens.append(token_type.text.strip())

        marketplace = Marketplace(name, avg_price, volume, traders, tokens)

        add_row_to_csv(object_to_list(marketplace), csv_path)

    driver.quit()

page_scrapping("https://dappradar.com/nft/marketplaces/1")
page_scrapping("https://dappradar.com/nft/marketplaces/2")

