class Product:
    def __init__(self, timestamp=None, market=None, name=None, vendor=None, ships_from=None, ships_to=None, price=None,
                 price_eur=None, info=None, feedback=None):
        self.timestamp = timestamp
        self.market = market
        self.name = name
        self.vendor = vendor
        self.ships_from = ships_from
        self.ships_to = ships_to
        self.price = price
        self.price_eur = price_eur
        self.info = info
        self.feedback = feedback

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, value):
        self._market = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = value

    @property
    def ships_from(self):
        return self._ships_from

    @ships_from.setter
    def ships_from(self, value):
        self._ships_from = value

    @property
    def ships_to(self):
        return self._ships_to

    @ships_to.setter
    def ships_to(self, value):
        self._ships_to = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def price_eur(self):
        return self._price_eur

    @price_eur.setter
    def price_eur(self, value):
        self._price_eur = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value

    @staticmethod
    def __prop__():
        return [key for key in Product.__dict__
                if not key.startswith("_") and "property object at" in str(Product.__dict__[key])]


class Vendor:
    def __init__(self, timestamp, market, name, score, score_normalized, registration, registration_deviation, last_login,
                 last_login_deviation, sales, info, feedback):
        self.timestamp = timestamp
        self.market = market
        self.name = name
        self.score = score
        self.score_normalized = score_normalized
        self.registration = registration
        self.registration_deviation = registration_deviation
        self.last_login = last_login
        self.last_login_deviation = last_login_deviation
        self.sales = sales
        self.info = info
        self.feedback = feedback

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, value):
        self._market = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def score_normalized(self):
        return self._score_normalized

    @score_normalized.setter
    def score_normalized(self, value):
        self._score_normalized = value

    @property
    def registration(self):
        return self._registration

    @registration.setter
    def registration(self, value):
        self._registration = value

    @property
    def registration_deviation(self):
        return self._registration_deviation

    @registration_deviation.setter
    def registration_deviation(self, value):
        self._registration_deviation = value

    @property
    def last_login(self):
        return self._last_login

    @last_login.setter
    def last_login(self, value):
        self._last_login = value

    @property
    def last_login_deviation(self):
        return self._last_login_deviation

    @last_login_deviation.setter
    def last_login_deviation(self, value):
        self._last_login_deviation = value

    @property
    def sales(self):
        return self._sales

    @sales.setter
    def sales(self, value):
        self._sales = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value

    @staticmethod
    def __prop__():
        return [key for key in Vendor.__dict__
                if not key.startswith("_") and "property object at" in str(Vendor.__dict__[key])]


class Feedback:
    def __init__(self, type, timestamp, market, name, feedback):
        self.type = type
        self.timestamp = timestamp
        self.market = market
        self.name = name
        self.feedback = feedback

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, value):
        self._market = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value

    @staticmethod
    def __prop__():
        return [key for key in Vendor.__dict__
                if not key.startswith("_") and "property object at" in str(Vendor.__dict__[key])]