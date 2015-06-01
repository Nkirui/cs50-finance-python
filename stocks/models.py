from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import csv
import urllib.request

# Add app-specific data to User
class FinanceUser(models.Model):
    user = models.OneToOneField(User)
    cash = models.FloatField(default=10000)

    # Return a list of all StockHoldings owned by the user
    def get_portfolio(self):
        return self.stockholding_set.all()


# Represents a stock. Non-persistent object used to encapsulate current stock info, namely price
class Stock:
    def __init__(self, symbol):

        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s=" + symbol
        with urllib.request.urlopen(url) as response:
            reader = csv.DictReader(response.read().decode('utf-8').splitlines(),
                                    fieldnames=['symbol', 'name', 'price'], delimiter=",", quotechar='"',
                                    quoting=csv.QUOTE_NONNUMERIC)

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


# Represents a user's holding of a stock, including total shares and transactions for a given symbol
class StockHolding(models.Model):
    symbol = models.CharField(max_length=5)
    shares = models.PositiveIntegerField(default=0)

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
        cost = stock.price * number_of_shares
        if user.cash < cost:
            raise StockTransactionError('Not enough cash. Trying to buy $' + str(cost)
                                        + ' of ' + symbol + ', but only $' + str(user.cash) + ' is available')

        # Fetch existing stock holding for the symbol, creating a new holding if one doesn't exist
        results = StockHolding.objects.get_or_create(symbol=symbol, owner=user)
        holding = results[0]
        Transaction.objects.create(holding=holding, shares=number_of_shares, type=Transaction.BUY, price=stock.price)

        # Update model
        holding.shares += number_of_shares
        user.cash -= stock.price * number_of_shares
        user.save()
        holding.save()

        return holding

    @staticmethod
    def sell_shares(user, symbol, number_of_shares):
        stock = Stock(symbol)

        holding = StockHolding.objects.get(symbol=symbol, owner=user)

        # Make sure user owns at least number_of_shares
        if number_of_shares > holding.shares:
            raise StockTransactionError('Not enough shares. Trying to sell ' + str(number_of_shares)
                                        + ' of ' + symbol + ', but only ' + str(holding.shares) + ' shares are owned')

        Transaction.objects.create(holding=holding, shares=number_of_shares, type=Transaction.SELL, price=stock.price)

        # Update model
        holding.shares -= number_of_shares
        user.cash += stock.price * number_of_shares
        user.save()
        holding.save()

        return holding


# A given buy/sell transaction
class Transaction(models.Model):
    # Enumeration tuple for transaction types
    BUY = 1
    SELL = 2
    TRANSACTION_CHOICES = (
        (BUY, 'buy'),
        (SELL, 'sell'),
    )

    holding = models.ForeignKey(StockHolding)
    shares = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=datetime.now)
    price = models.FloatField(default=0)
    type = models.IntegerField(choices=TRANSACTION_CHOICES)


# Custom exception for notifying the controller of an error when retrieving stock information
class StockLookupError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Error looking up current stock data: ' + self.value)


# Custom exception for notifying the controller that a transaction can not be carried out
class StockTransactionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Error completing transaction: ' + self.value)
