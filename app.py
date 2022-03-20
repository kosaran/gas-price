from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_prices():
    gas_prices = {}
    html_text = requests.get('https://www.caa.ca/gas-prices/').text
    soup = BeautifulSoup(html_text, 'lxml')
    collectivePrice = soup.find('li', attrs={'data-location': 'PEEL REGION'})
    gasPrice = float(collectivePrice.get('data-today'))
    carTankCapacity = 88.64875
    carRange = 695
    carEfficiency = carTankCapacity / carRange
    travelDistance = 43.6
    burnedGas = travelDistance * carEfficiency
    baseGasCost = round(((2 * (burnedGas * gasPrice)) / 100), 2)

    kipling_distance = 2 * 28.4
    burnedTransitGas = kipling_distance * carEfficiency
    burnedTransitCost = round(((burnedTransitGas * gasPrice) / 100), 2)
    baseTransitCost = round((6.40 + burnedTransitCost),2)

    gas_prices['base_drive'] = baseGasCost
    gas_prices['base_transit'] = baseTransitCost

    return gas_prices


@app.route('/')
def hello_world():  # put application's code here

    return "API for getting average gas price in the Peel Region"

@app.route('/gasprice')
def calculate_price():  # put application's code here
    base_prices = get_prices()

    return base_prices



if __name__ == '__main__':
    app.run()





