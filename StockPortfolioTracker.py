import requests

API_KEY = 'YOUR_API_KEY'

def get_stock_data(symbol):
    # Get stock price data
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    # Get sector data
    sector_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    sector_response = requests.get(sector_url)
    sector_data = sector_response.json()
    
    if 'Global Quote' in data and 'Sector' in sector_data:
        return {
            'price': data['Global Quote']['05. price'],
            'sector': sector_data['Sector']
        }
    else:
        return None

class Portfolio:

    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] += quantity
        else:
            self.stocks[symbol] = quantity

    def remove_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] -= quantity
            if self.stocks[symbol] <= 0:
                del self.stocks[symbol]

    def get_portfolio_value(self):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            stock_data = get_stock_data(symbol)
            if stock_data:
                price = float(stock_data['price'])
                total_value += price * quantity
        return total_value

def calculate_gain_loss(initial_value, current_value):
    return current_value - initial_value

def calculate_diversification(portfolio):
    sector_weights = {}
    total_value = portfolio.get_portfolio_value()
    
    for symbol, quantity in portfolio.stocks.items():
        stock_data = get_stock_data(symbol)
        if stock_data:
            sector = stock_data['sector']
            price = float(stock_data['price'])
            sector_value = quantity * price
            
            if sector in sector_weights:
                sector_weights[sector] += sector_value
            else:
                sector_weights[sector] = sector_value
    
    diversification = {sector: (value / total_value) * 100 for sector, value in sector_weights.items()}
    return diversification

def main():
    portfolio = Portfolio()
    initial_value = 0  

    while True:
        print("\n1. Add stock to portfolio")
        print("2. Remove stock from portfolio")
        print("3. View portfolio value")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.add_stock(symbol, quantity)
        elif choice == '2':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            portfolio.remove_stock(symbol, quantity)
        elif choice == '3':
            value = portfolio.get_portfolio_value()
            print(f"Portfolio value: ${value:.2f}")
            print("Gains/Losses: ${:.2f}".format(calculate_gain_loss(initial_value, value)))
            print("Diversification:")
            for sector, weight in calculate_diversification(portfolio).items():
                print(f"{sector}: {weight:.2f}%")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()