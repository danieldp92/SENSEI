from ..controller.TableController import TableController

TABLE_NAME = "product"


class ProductController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

    def insert_platform_bean(self, beans):
        query = f"INSERT INTO `{self.db_name}`.`products_cleaned` (`timestamp`, `market`, `name`, `vendor`, `ships_from`, " \
                f"`ships_to`, `price`, `macro_category`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        values = []
        for bean in beans:
            if isinstance(bean.ships_from, list):
                bean.ships_from = ", ".join(str(elem) for elem in bean.ships_from)

            if isinstance(bean.ships_to, list):
                bean.ships_to = ", ".join(str(elem) for elem in bean.ships_to)

            price = 0
            if isinstance(bean.price_eur, dict):
                for item in bean.price_eur:
                    price += bean.price_eur[item]
                price /= len(bean.price_eur)

                if price:
                    bean.price_eur = price
                else:
                    bean.price_eur = None

            value = (
            bean.timestamp, bean.market, bean.name, bean.vendor, bean.ships_from, bean.ships_to, bean.price_eur,
            bean.category)

            values.append(value)

        self.mysql_db.insert(query, values)

    def insert_beans(self, beans):
        attributes = ["timestamp", "market", "name", "vendor", "ships_from", "ships_to", "price", "price_eur", "info",
                      "feedback"]

        # Preprocessing
        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(str(elem) for elem in val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(ProductController, self).insert_beans(new_beans)

    def retrieve_markets(self):
        query = "SELECT {0}.market from {1}.{0} GROUP BY {0}.market".format(TABLE_NAME, self.db_name)
        header, results = self.mysql_db.search(query)

        markets = []
        for result in results:
            markets.append(result[0].lower())

        return markets

    def retrieve_markets_timestamps(self):
        query = "SELECT DISTINCT {0}.timestamp, {0}.market FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets_timestamps = {}
        for result in results:
            market = result[1]
            timestamp = result[0]

            if market in markets_timestamps:
                markets_timestamps[market].append(timestamp)
            else:
                markets_timestamps[market] = [timestamp]

        return markets_timestamps

    def retrieve_markets_timestamps_products(self):
        query = "SELECT DISTINCT {0}.name, {0}.timestamp, {0}.market FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets_timestamps = {}
        for result in results:
            market = result[2]
            timestamp = result[1]
            name = result[0]

            if market in markets_timestamps:
                if timestamp in markets_timestamps[market]:
                    markets_timestamps[market][timestamp].append(name)
                else:
                    markets_timestamps[market][timestamp] = [name]
            else:
                markets_timestamps[market] = {timestamp: [name]}

        return markets_timestamps

    def retrieve_vendor_products(self, vendor):
        query = "SELECT DISTINCT {0}.name, {0}.vendor, {0}.timestamp, {0}.market from {1}.{0} WHERE {0}.vendor = %s " \
                "ORDER BY {0}.timestamp DESC".format(TABLE_NAME, self.db_name)

        values = (vendor,)
        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            market = product["market"]
            name = product["name"]

            # Check if the market has already been saved in the dict
            if market not in markets:
                markets[market] = {}

            # Check if the timestamp has already been saved in the market value
            if timestamp not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(name)

        return {vendor: markets}

    def retrieve_vendor_product(self, vendor, product_name):
        query = "SELECT * FROM {1}.{0} WHERE {0}.vendor = %s AND {0}.name = %s" \
                "ORDER BY {0}.timestamp DESC".format(TABLE_NAME, self.db_name)

        values = (vendor, product_name)
        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            market = product["market"]
            del product["timestamp"]
            del product["market"]
            del product["vendor"]

            # Check if the market has already been saved in the dict
            if market not in markets:
                markets[market] = {}

            # Check if the timestamp has already been saved in the market value
            if timestamp not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(product)

        return {vendor: markets}

    def get_product(self, market, name, last_timestamp=False):
        query = "SELECT * from {0}.{1} WHERE {1}.market = %s AND {1}.name = %s ORDER BY {1}.timestamp DESC".format(self.db_name, TABLE_NAME)

        values = (market, name)
        header, results = self.mysql_db.search(query, values)

        timestamps = {}
        max_timestamp = 0

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            del product["timestamp"]

            # The first timestamp is the last inserted, because the query has been ordered by timestamp
            if max_timestamp is None:
                max_timestamp = timestamp

            if timestamp in timestamps:
                timestamps[timestamp].append(product)
            else:
                timestamps[timestamp] = [product]

        if last_timestamp and timestamps:
            timestamps = timestamps[max_timestamp]

        products = {market: timestamps}
        return products

    def delete_dumps(self, market, timestamps):
        query = "DELETE FROM `{0}`.`{1}` WHERE (`market` = %s) AND (`timestamp` = %s)".format(self.db_name, TABLE_NAME)

        values = []
        for timestamp in timestamps:
            values.append((market, timestamp))

        self.mysql_db.delete(query, values)

    def get_product_no_fdb(self):
        """
        Get products without feedback
        """

        query = f"SELECT timestamp, market, name, vendor, ships_from, ships_to, category, price " \
                f"FROM {self.db_name}.{TABLE_NAME};"

        header, results = self.mysql_db.search(query)

        json_data = []
        for line in results:
            json_data.append(dict(zip(header, line)))

        return json_data

    def check_table(self):
        sql = "DESCRIBE product;"
        return self._mysql_db.search(sql)