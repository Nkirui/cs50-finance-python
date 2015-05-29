from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import csv
import urllib.request

''' Add app-specific data to User'''
class FinanceUser(models.Model):
    user = models.OneToOneField(User)
    cash = models.IntegerField(default=10000)

    # Return a list of all StockHoldings owned by the user
    def get_portfolio(self):
        return self.stockholding_set.all()


''' Represents a stock. Non-persistent object used to encapsulate current stock info, namely price '''
class Stock:

    def __init__(self, symbol):

        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s=" + symbol
        with urllib.request.urlopen(url) as response:
            reader = csv.DictReader(response.read().decode('utf-8').splitlines(), fieldnames=['symbol','name','price'], delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

            total_rows = 0

            for row in reader:
                self.name = row.get("name")
                self.price = row.get("price")
                self.symbol = row.get("symbol")
                total_rows += 1

        if total_rows == 0:
            raise StockLookupError('No stock with symbol ' + symbol)
        elif total_rows > 1:
            raise StockLookupError('Unknown error')

''' Custom exception for notifying the controller of an error when retrieving stock information '''
class StockLookupError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Error looking up current stock data: ' + self.value)


''' Represents a user's holding of a stock, including total shares and transactions for a given symbol '''
class StockHolding(models.Model):

    symbol = models.CharField(max_length=5)
    shares = models.IntegerField()

    # Foreign key to FinanceUser is necessary to fetch portfolio from that class
    owner = models.ForeignKey(FinanceUser)

    # Return a list of all transactions for the given holding
    def get_transactions(self):
        return self.transaction_set.all()

    @staticmethod
    def buy_shares(user, symbol, number_of_shares):

        # Get current information about stock
        stock = Stock(symbol)

        # Make sure user has enough cash
        if user.cash < stock.price * number_of_shares:
            return False

        # Fetch existing stock holding for the symbol, creating a new holding if one doesn't exist
        holding = StockHolding.objects.get_or_create(symbol=symbol, owner=user)
        holding.shares += number_of_shares
        user.cash -= stock.price * number_of_shares
        Transaction.create(holding=holding, type="buy", price=stock.price)
        return True

    @staticmethod
    def sell_shares(user, symbol, number_of_shares):
        stock = Stock(symbol)

        holding = StockHolding.objects.get_or_create(symbol=symbol, owner=user)

        if number_of_shares > holding.shares:
            return False

        holding.shares -= number_of_shares
        Transaction.create(holding=holding, type="sell", price=stock.price)
        return True


# A given buy/sell transaction
class Transaction(models.Model):
    holding = models.ForeignKey(StockHolding)
    date = models.DateField(default=datetime.now)
    # TODO - convert 'type' to an enum
    type = models.CharField(max_length=10) # "buy" or "sell"
    price = models.FloatField
    shares = models.IntegerField
